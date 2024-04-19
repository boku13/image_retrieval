import os
import tarfile
import numpy as np
import pickle
from PIL import Image

class cifar10:
    def __init__(self, tar_file='data/cifar10.tar.gz'):
        self.tar_file = tar_file
        self.classes = []
        self.train_images = []
        self.train_labels = []
        self.images_per_class = {} 

        self.load_dataset()

    def load_dataset(self):
        if not os.path.exists('data/cifar10'):
            with tarfile.open(self.tar_file, "r:gz") as tar:
                tar.extractall('data')

        # Load batches.meta to get label names
        meta_data = self.unpickle('data/cifar10/batches.meta')
        self.classes = [label.decode('utf-8') for label in meta_data[b'label_names']]

        for class_name in self.classes:
            self.images_per_class[class_name] = []

        for i in range(1, 6):  # 5 training batches
            batch_data = self.unpickle(f'data/cifar10/data_batch_{i}')
            if i == 1:
                self.train_images = batch_data[b'data']
                self.train_labels = batch_data[b'labels']
            else:
                self.train_images = np.vstack((self.train_images, batch_data[b'data']))
                self.train_labels += batch_data[b'labels']

        self.train_labels = np.array(self.train_labels)
        self.train_images = self.train_images.reshape((-1, 3, 32, 32)).transpose(0, 2, 3, 1)  # Convert to HWC

        for idx, label in enumerate(self.train_labels):
            class_name = self.classes[label]

            if len(self.images_per_class[class_name]) < 5:
                self.images_per_class[class_name].append(self.train_images[idx])

    def unpickle(self, file):
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict

    def display_images(self, plt):
        plt.figure(figsize=(10, 10))
        for i in range(10):
            ax = plt.subplot(5, 5, i + 1)
            idx = np.where(self.train_labels == i)[0][0]  # Find the first occurrence of each class
            plt.imshow(self.train_images[idx])
            plt.title(self.classes[i])
            plt.axis("off")
        plt.show()
