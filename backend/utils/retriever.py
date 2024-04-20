import pickle
import os
import numpy as np
import sklearn
from .data import cifar10
from PIL import Image

class simple_retriever():
    def __init__(self, model, image, preprocessing):
        self.model = model
        self.transform = preprocessing
        # self.model_path = "models/default/" + model + ".pkl"
        # self.feature_transform_path = "models/default/" + preprocessing + ".pkl"
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory where this script is located
        self.model_path = os.path.join(base_dir, "models", "default", model + ".pkl")
        self.feature_transform_path = os.path.join(base_dir, "models", "default", preprocessing + ".pkl")
        self.image = image
        self.image = image
        self.loaded_model = None
        self.loaded_transform = None
        self.classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    def load_preprocessing(self):
        print("Model path:", self.model_path)
        print("Feature transform path:", self.feature_transform_path)
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
            print("Predicted Label :", label[0])
        else:
            return None

    def retrieve_images(self, label):
        data = cifar10()
        print(label)
        key = self.classes.index(label)
        if label in self.classes:
            # Use the label to retrieve images from the images_per_class dictionary
            print(data.images_per_class)
            images = data.images_per_class[key]
            return images
        else:
            print(f"Label '{label}' not found in the dataset.")
            return []

# if __name__ == "__main__":
#     def preprocess_image(image):
#         """ Convert an uploaded image file to the format your model expects. """
#         image = image.resize((32, 32))  # Adjust to CIFAR-10 size
#         if image.mode != 'RGB':
#             image = image.convert('RGB')
#         image_np = np.array(image)
#         if not image_np.flags['C_CONTIGUOUS']:
#             image_np = np.ascontiguousarray(image_np)
#         return image_np.flatten()  # Flatten and prepare for model


#     # Example usage
#     # model_name = 'example_model'
#     # preprocessing_name = 'example_preprocessing'
#     image_path = '/home/boku/acads/prml/image_retrieval/backend/utils/data/cifar10/deer/deer.png'
#     # base_dir = os.path.dirname(os.path.abspath(__file__))
#     # print(base_dir)
#     # image_path = os.path.join(base_dir, image_path)
#     retriever = simple_retriever(model="AdaBoost", image=image_path, preprocessing="PCA")
#     retriever.load_preprocessing()
#     retriever.load_model()
#     image = Image.open(image_path)
#     print(image)
#     image = preprocess_image(image)
#     label = retriever.inference(image)
#     if label:
#         images = retriever.retrieve_images(label)
#         for img in images:
#             img.show()  # Display the images