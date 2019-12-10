import io
import os
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def labels_to_dict(labels):
    # Labels is a 'google.protobuf.pyext._message.RepeatedCompositeCo' variable
    list_labels = []
    for label in labels:
       list_labels.append((label.description, label.score))

    dict_labels = dict(list_labels)

    # Serialization for sending over socket
    serialized_dict = json.dumps(dict_labels)
    return serialized_dict



def image_recognition(image_file_path):
    # Set Credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./CS655FinalKey.json"

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        image_file_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    dict_labels = labels_to_dict(labels)

    return dict_labels