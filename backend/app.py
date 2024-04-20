import os
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS


from PIL import Image
from io import BytesIO
import base64
from utils.data import cifar10
from utils.retriever import simple_retriever

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Global objects for the dataset and retriever
dataset = None
retriever = None

def load_resources():
    global dataset, retriever
    dataset = cifar10()
    retriever = simple_retriever(model="AdaBoost", image=None, preprocessing="PCA")
    retriever.load_preprocessing()
    retriever.load_model()

with app.app_context():
    load_resources()

def preprocess_image(image):
    """ Convert an uploaded image file to the format your model expects. """
    image = image.resize((32, 32))  # Adjust to CIFAR-10 size
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image_np = np.array(image)
    if not image_np.flags['C_CONTIGUOUS']:
        image_np = np.ascontiguousarray(image_np)
    return image_np.flatten()  # Flatten and prepare for model

@app.route('/infer', methods=['POST'])
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

    images = np.array(images)
    # Convert images to base64 strings
    response = {'images': []}
    for img in images:
        print(img)
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)
        if not img.flags['C_CONTIGUOUS']:
            img = np.ascontiguousarray(img)
        
        img_pil = Image.fromarray(img)
        byte_io = BytesIO()
        img_pil.save(byte_io, 'JPEG')
        byte_io.seek(0)
        base64_image = base64.b64encode(byte_io.getvalue()).decode('utf-8')
        response['images'].append(f"data:image/jpeg;base64,{base64_image}")

    return jsonify(response)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
