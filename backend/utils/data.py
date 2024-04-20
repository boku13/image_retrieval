# import os
# from PIL import Image

# class cifar10:
#     def __init__(self, root_dir='data/cifar10', images_per_label=10):
#         self.root_dir = root_dir
#         self.images_per_label = images_per_label
#         self.classes = []  # To store all labels
#         self.images_per_class = {}  # Dictionary to store lists of images per label
#         self.class_labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
#         self.images_per_class = {i: [] for i in range(len(self.class_labels))} 
#         self.initialize_dataset()

#     def initialize_dataset(self):
#         """
#         Initialize the dataset by loading a specified number of images from each subfolder.
#         Each subfolder corresponds to a class/label.
#         """
#         if os.path.exists(self.root_dir):
#             self.classes = [d for d in os.listdir(self.root_dir) if os.path.isdir(os.path.join(self.root_dir, d))]
#             for label in self.classes:
#                 label_dir = os.path.join(self.root_dir, label)
#                 all_images = [img for img in os.listdir(label_dir) if img.endswith(('png', 'jpg', 'jpeg'))]
#                 selected_images = all_images[:self.images_per_label]  # Select the specified number of images

#                 self.images_per_class[label] = []
#                 for image_file in selected_images:
#                     image_path = os.path.join(label_dir, image_file)
#                     try:
#                         with Image.open(image_path) as img:
#                             self.images_per_class[label].append(img.copy())
#                     except IOError:
#                         print(f"Error opening image {image_path}")

#     def retrieve_images(self, label):
#         """
#         Retrieve images for a given label from the images_per_class dictionary.
#         """
#         if label in self.classes:
#             return self.images_per_class[label]
#         else:
#             print(f"Label '{label}' not found in the dataset.")
#             return []
    
# # if __name__ == "__main__":
# #     data = cifar10()
# #     print(data.images_per_class)
# #     images = data.retrieve_images('dog')  # Replace 'dog' with the actual label name you are interested in
# #     for img in images:
# #         img.show()  # Display the images

import os
from PIL import Image

class cifar10:
    def __init__(self, root_dir='utils/data/cifar10', images_per_label=10):
        self.root_dir = root_dir
        self.images_per_label = images_per_label
        self.classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']  # Predefined class order
        self.images_per_class = {}  # Dictionary to store lists of images per label
        self.initialize_dataset()

    def initialize_dataset(self):
        """
        Initialize the dataset by loading a specified number of images from each subfolder.
        Each subfolder corresponds to a class/label. Classes are mapped directly to their indices.
        """
        for idx, label in enumerate(self.classes):
            label_dir = os.path.join(self.root_dir, label)
            if os.path.exists(label_dir):
                all_images = [img for img in os.listdir(label_dir) if img.endswith(('png', 'jpg', 'jpeg'))]
                selected_images = all_images[:self.images_per_label]  # Select the specified number of images

                self.images_per_class[idx] = []  # Use the index as the key for the dictionary
                
                for image_file in selected_images:
                    image_path = os.path.join(label_dir, image_file)
                    try:
                        with Image.open(image_path) as img:
                            self.images_per_class[idx].append(img.copy())
                    except IOError:
                        print(f"Error opening image {image_path}")

    def retrieve_images(self, label_index):
        """
        Retrieve images for a given label index from the images_per_class dictionary.
        """
        if label_index in self.images_per_class:
            return self.images_per_class[label_index]
        else:
            print(f"Label index '{label_index}' not found in the dataset.")
            return []

# Example usage:
if __name__ == "__main__":
    dataset = cifar10()
    # Retrieve images for the class index 0 (which is 'airplane')
    images = dataset.retrieve_images(9)
    for img in images:
        img.show()  # This will display the images if you're running this locally
