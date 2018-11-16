import datetime
import pdb
import tempfile
import time

import json
import firebase_admin
import requests
from firebase_admin import credentials, db, storage, messaging

import capture_video
import draw_artwork
import draw_signature
import write_address
import write_message

class PostcardState:
    START = 0
    PRINTING_BACK = 1
    UPLOADED_BACK_VID = 2
    PRINTING_FRONT = 3
    FINISH = 4

class PostcardData:
    postcardId = None
    postcardData = None
    axiInstructionFile = None
    artworkData = None
    postcardState = PostcardState.START

    def __init__(self, card_id):
        self.postcardId = card_id
        self.postcardData = self.get_db_reference().get()  # type: dict
        if not self.postcardData or 'instructions' not in self.postcardData:
            raise Exception('postcard data is not available for card {}'.format(self.postcardId))
        self.axiInstructionFile = tempfile.NamedTemporaryFile(suffix=".axi", delete=False)
        print 'saved into {}'.format(self.axiInstructionFile.name)
        instructions = requests.get(self.postcardData['instructions']).content
        self.artworkData = json.loads(instructions)
        self.axiInstructionFile.write(instructions)
        self.axiInstructionFile.close()
        self.postcardState = int(self.postcardData['status'])


    @classmethod
    def upload_blob_for_video_with_name(cls, cardId, name):
        return storage.bucket(name='waterposts', app=None).blob('videos/{}/{}.mp4'.format(cardId, name))

    def upload_blob_for_back(self):
        return PostcardData.upload_blob_for_video_with_name(self.postcardId, 'back')

    def make_sure_status_gets_set(self):
        queueRef = db.reference().child("queue").child(self.postcardId)
        queueRef.set(self.postcardState)
        ref = self.get_db_reference().child('status')
        ref.set(self.postcardState)
        time.sleep(1)
        while ref.get() != self.postcardState or queueRef.get() != self.postcardState:
            time.sleep(1)

    def set_back_of_card_video_finished(self, signed_url):
        self.postcardState = PostcardState.UPLOADED_BACK_VID
        self.get_db_reference().child('back_video').set(signed_url)
        self.make_sure_status_gets_set()

    def set_front_of_card_video_finished(self, signed_url):
        self.postcardState = PostcardState.FINISH
        self.get_db_reference().child('front_video').set(signed_url)
        self.make_sure_status_gets_set()

    def upload_blob_for_front(self):
        return PostcardData.upload_blob_for_video_with_name(self.postcardId, 'front')

    def get_db_reference(self):
        return db.reference().child('posts').child(self.postcardId)

    def needs_front_printed(self):
        arr = [PostcardState.START, PostcardState.PRINTING_BACK, PostcardState.UPLOADED_BACK_VID]
        return self.postcardState in arr

    def needs_back_printed(self):
        return self.postcardState == PostcardState.START

    def ready_to_print_back(self):
        return self.postcardState == PostcardState.START

    def ready_to_print_front(self):
        return self.postcardState == PostcardState.UPLOADED_BACK_VID


class PrinterState:
    IDLE = 0
    WAITING_FOR_BACK_READY = 1
    READY_FOR_BACK = 2
    WRITING_BACK = 3
    READY_FOR_FRONT = 4
    WRITING_FRONT = 5
    WAITING_FOR_FRONT_READY = 6

class PostcardPrinter:
    status = PrinterState.IDLE

    def set_printer_state(self, newStatus):
        self.status = newStatus
        ref = db.reference().child("printer").child("state")
        ref.set(self.status)
        time.sleep(1)
        while ref.get() != self.status:
            time.sleep(1)

    def update_printer_state(self):
        ref = db.reference().child("printer").child("state")
        self.status = ref.get()

    def print_card(self, currentPostcard):
        print 'printing card {} of status {}'.format(currentPostcard.postcardId, currentPostcard.postcardState)
        """

        :type currentPostcard: PostcardData
        """
        if currentPostcard.needs_back_printed():
            print 'printing back of card'
            self.set_printer_state(PrinterState.WAITING_FOR_BACK_READY)
            while not self.ready_to_print_back() or not currentPostcard.ready_to_print_back():
                print 'waiting for ready...'
                time.sleep(5)
            try:
                self.print_back(currentPostcard)
                self.set_printer_state(PrinterState.IDLE)
            except Exception, e:
                raise e
        if currentPostcard.needs_front_printed():
            print 'printing front of card'
            self.set_printer_state(PrinterState.WAITING_FOR_FRONT_READY)
            while not self.ready_to_print_front() or not currentPostcard.ready_to_print_front():
                print 'waiting for ready...'
                time.sleep(5)
            try:
                self.print_front(currentPostcard)
                self.set_printer_state(PrinterState.IDLE)
            except Exception, e:
                raise e

    def ready_to_print_back(self):
        self.update_printer_state()
        return self.status == PrinterState.READY_FOR_BACK

    def print_back(self, currentPostcard):
        """

        :type currentPostcard: PostcardData
        """
        pdb.set_trace()
        self.set_printer_state(PrinterState.WRITING_BACK)
        videoCapture = capture_video.VideoCapture()
        videoCapture.start_recording()
        try:
            write_message.write_message(currentPostcard.artworkData)
            draw_signature.draw_signature(currentPostcard.artworkData)
            write_address.write_address(currentPostcard.artworkData)
        except Exception, e:
            videoCapture.stop_recording()
            self.set_printer_state(PrinterState.IDLE)
            raise e
        videoCapture.stop_recording()
        self.set_printer_state(PrinterState.IDLE)
        uploadBlob = currentPostcard.upload_blob_for_back()
        uploadBlob.upload_from_filename(videoCapture.temporaryFile)
        signed_url = uploadBlob.generate_signed_url(datetime.timedelta(days=365 * 100))
        currentPostcard.set_back_of_card_video_finished(signed_url)
        return 0


    def ready_to_print_front(self):
        self.update_printer_state()
        return self.status == PrinterState.READY_FOR_FRONT


    def print_front(self, currentPostcard):
        self.set_printer_state(PrinterState.WRITING_FRONT)
        videoCapture = capture_video.VideoCapture()
        videoCapture.start_recording()
        try:
            draw_artwork.draw_artwork(currentPostcard.artworkData)
        except Exception, e:
            videoCapture.stop_recording()
            self.set_printer_state(PrinterState.IDLE)
            raise e
        videoCapture.stop_recording()
        self.set_printer_state(PrinterState.IDLE)
        uploadBlob = currentPostcard.upload_blob_for_front()
        uploadBlob.upload_from_filename(videoCapture.temporaryFile)
        signed_url = uploadBlob.generate_signed_url(datetime.timedelta(days=365 * 100))
        currentPostcard.set_front_of_card_video_finished(signed_url)
        return 0


class PostcardProcessor:
    def __init__(self, operatorData):
        self.currentPostcard = None
        self.postcardPrinter = PostcardPrinter()
        self.operatorData = operatorData

    def run(self):
        queue = []
        while True:
            print 'updating queue'
            while queue == None or len(queue) == 0:
                queueMap = db.reference().child("queue").order_by_value().end_at(PostcardState.UPLOADED_BACK_VID).get()  # type: dict
                queue = queueMap.keys()
                # check to be sure
                for key in queue:
                    assert queueMap[key] != PostcardState.FINISH

                if not queue:
                    time.sleep(10)
                    continue
            card_id = queue[0]  # type: str
            card = PostcardData(card_id)
            self.send_operator_message('Get your pen ready!', 'Card ready to print')
            self.postcardPrinter.print_card(card)
            if card.postcardState == PostcardState.FINISH:
                card.make_sure_status_gets_set()
                queue.remove(card_id)
            if len(queue) == 0:
                time.sleep(10)

    def send_operator_message(self, title, body):
        registration_token = self.operatorData['token']

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=registration_token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)


if __name__ == '__main__':
    # Initialize the default app
    operatorData = json.loads(open('operator.json','r').read())
    cred = credentials.Certificate('credentials.json')
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://beaming-surfer-222116.firebaseio.com'})

    processor = PostcardProcessor(operatorData)
    processor.run()