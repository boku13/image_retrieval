import os
import numpy as np
import pickle
from flask import Flask, request, send_file, jsonify
from PIL import Image
from io import BytesIO
from sklearn.externals import joblib  # Adjust this import depending on your sklearn version and model serialization method
import tarfile

app = Flask(__name__)

# Global objects for the dataset and retriever
dataset = None
retriever = None

class cifar10:
    # Same cifar10 class as provided, with methods like init, load_dataset, unpickle

class simple_retriever:
    # Same simple_retriever class as provided, with methods like init, load_preprocessing, load_model, inference, retrieve_images

@app.before_first_request
def load_resources():
    global dataset, retriever
    dataset = cifar10()
    # Assuming the model and preprocessing are fixed for simplicity
    retriever = simple_retriever(model="AdaBoost", image=None, preprocessing="PCA")
    retriever.load_preprocessing()
    retriever.load_model()

def preprocess_image(image):
    """ Convert an uploaded image file to the format your model expects. """
    image = image.resize((32, 32))  # Adjust to CIFAR-10 size
    image = np.array(image)
    return image.reshape(-1, 32*32*3)  # Flatten and prepare for model

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image = Image.open(file.stream)
    preprocessed_image = preprocess_image(image)
    label = retriever.inference(preprocessed_image)
    images = retriever.retrieve_images(dataset.classes[label])

    # Assuming that you want to send back the images as a response
    response = {}
    for i, img in enumerate(images):
        img_pil = Image.fromarray(img)
        byte_io = BytesIO()
        img_pil.save(byte_io, 'JPEG')
        byte_io.seek(0)
        response[f'image{i}'] = send_file(byte_io, mimetype='image/jpeg')

    return response

if __name__ == '__main__':
    app.run(debug=True)
