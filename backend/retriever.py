import pickle
import os
import numpy as np
import sklearn
from data import cifar10

class simple_retriever():
    def __init__(self, model, image, preprocessing):
        self.model = model
        self.transform = preprocessing
        self.model_path = "models/default/" + model + ".pkl"
        self.feature_transform_path = "models/default/" + preprocessing + ".pkl"
        self.image = image
        self.loaded_model = None
        self.loaded_transform = None

    def load_preprocessing(self):
        print(self.model_path)
        print(self.feature_transform_path)
        if os.path.exists(self.feature_transform_path):
            with open(self.feature_transform_path, 'rb') as file:
                self.loaded_transform = pickle.load(file)
        else:
            print("Preprocessing file does not exist.")

    def load_model(self):
        print(self.model_path)
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as file:
                self.loaded_model = pickle.load(file)
        else:
            print("Model file does not exist.")

    def inference(self, image):
        if self.loaded_transform is not None:
            image = self.loaded_transform.transform([image])
            print(image.shape)
        if self.loaded_model is not None:
            # check later
            print(image.shape)
            label = self.loaded_model.predict(image)
            return label[0]
        else:
            return None

    def retrieve_images(self, label):
        data = cifar10()
        if label in data.classes:
            # Use the label to retrieve images from the images_per_class dictionary
            images = data.images_per_class[label]
            return images
        else:
            print(f"Label '{label}' not found in the dataset.")
            return []
