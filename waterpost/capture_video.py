import time

import cv2
import threading
import tempfile
from subprocess import call


VIDEO_CAMERA = 1
class VideoCapture():
    def __init__(self):
        self.maxRecordingTime = 60
        self.cap = None
        self.start_time = None
        self.thread = None
        self.vout = None
        self.largeVideoFile = None
        self.temporaryFile = None
        self.shouldStopRecording = False

    def is_recording(self):
        return self.start_time is not None

    def start_recording(self):
        if self.is_recording():
            print 'already recording a video'
            return -1
        self.cap = cv2.VideoCapture(VIDEO_CAMERA)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.vout = cv2.VideoWriter()
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        self.largeVideoFile = tempfile.NamedTemporaryFile(suffix=".mp4").name
        success = self.vout.open(self.largeVideoFile, fourcc, 30.0, size, True)
        if not success:
            print 'couldn\'t open file'
            return -1
        self.start_time = time.time()
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()

    def stop_recording(self):
        if not self.is_recording():
            print 'not recording a video'
            return
        self.shouldStopRecording = True
        self.thread.join()
        if not self.temporaryFile:
            print 'error compressing video!'
        else:
            print "saved to file to {}".format(self.temporaryFile)

    def run(self):
        while not self.shouldStopRecording:
            ret, frame = self.cap.read()
            if ret:
                self.vout.write(frame)
            else:
                break
            if not (self.cap.isOpened() and time.time() - self.start_time < self.maxRecordingTime):
                self.shouldStopRecording = True
        compressedFile = tempfile.NamedTemporaryFile(suffix=".mp4").name
        self.cap.release()
        self.vout.release()
        cv2.destroyAllWindows()
        call(['ffmpeg', '-i', self.largeVideoFile, '-filter:v', 'scale=420:-1,setpts=0.5*PTS', compressedFile])
        self.temporaryFile = compressedFile

if __name__ == '__main__':
    vid = VideoCapture()
    vid.start_recording()
    if raw_input():
        vid.stop_recording()
