import tempfile

import firebase_admin
from firebase_admin import credentials, storage, db
import requests
import draw_artwork
import json

from WaterpostOptions import WaterpostOptions
import draw_signature, write_message, write_address


def generate_artwork_from_json(json_file):
    front_of_card = tempfile.NamedTemporaryFile(suffix=".png").name
    options = WaterpostOptions(renderPath=front_of_card, shouldExecuteInstructions=False, debug=False)
    draw_artwork.draw_artwork(json_file, opts=options)

    back_of_card = tempfile.NamedTemporaryFile(suffix=".png").name
    options = WaterpostOptions(renderPath=None, shouldExecuteInstructions=False, debug=False)
    options.surface = draw_signature.draw_signature(json_file, options)
    options.surface = write_message.write_message(json_file, options)
    options.renderPath = back_of_card
    write_address.write_address(json_file, options)
    print 'saved in {}, {}'.format(front_of_card, back_of_card)


def process_post(post_key):
    ref = root.child('posts').child(post_key)
    post_data = ref.get()  # type: dict
    data_file = post_data['instructions']
    json_file = json.loads(requests.get(data_file).content)
    generate_artwork_from_json(json_file)


if __name__ == '__main__':
    # Initialize the default app

    cred = credentials.Certificate('credentials.json')
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://beaming-surfer-222116.firebaseio.com'})
    print default_app.name

    root = db.reference()
    posts = root.child("queue").get()  # type: dict
    posts_to_process = posts.keys()
    for post_key in posts_to_process:
        process_post(post_key)

    # bucket = storage.bucket(name="waterposts", app=None)
    # for b in bucket.list_blobs():
    #     # type google.cloud.storage.blob.Blob
    #     if 'axi' in b.name:
    #         b.download_to_filename('current.axi')
    #         pdb.set_trace()

    # vid = VideoCapture()
    # vid.start_recording()
    # draw_artwork.main('')
    # vid.stop_recording()
