import PIL
import tensorflow as tf
import albumentations
import pandas as pd
import os
import torch
import numpy as np
from fastai.vision import nn, models, create_head, AdaptiveConcatPool2d
from imageai.Detection.Custom import CustomObjectDetection
from .patterns.singleton import Singleton


class SiameseBannerRecognitionModelResNet50(nn.Module):
    model_path = os.path.join("models", "learn_res50_contrastive_loss2.pt")

    def __init__(self):
        super().__init__()
        self.cnn = nn.Sequential(*list(models.resnet50(True).children())[:-2])
        self.head = create_head(4096, 185, [2048])
        self.ada_concat = AdaptiveConcatPool2d(1)

    def forward(self, ims_a, ims_b):
        cnn_out_a = self.cnn(ims_a)
        out_a = self.head(cnn_out_a)

        cnn_out_b = self.cnn(ims_b)
        out_b = self.head(cnn_out_b)

        return out_a, out_b, self.ada_concat(cnn_out_a).squeeze(), self.ada_concat(cnn_out_b).squeeze()


class SiameseBannerRecognitionModelResNet18(nn.Module):
    model_path = os.path.join("models", "learn_res18.pt")

    def __init__(self):
        super().__init__()
        self.cnn = nn.Sequential(*list(models.resnet18(True).children())[:-2])
        self.head = create_head(1024, 87, [4000])
        self.ada_concat = AdaptiveConcatPool2d(1)

    def forward(self, ims_a, ims_b):
        cnn_out_a = self.cnn(ims_a)
        out_a = self.head(cnn_out_a)

        cnn_out_b = self.cnn(ims_b)
        out_b = self.head(cnn_out_b)

        return out_a, out_b, self.ada_concat(cnn_out_a).squeeze(), self.ada_concat(cnn_out_b).squeeze()


class ObjectRecognitionController(metaclass=Singleton):

    BASE_IMAGES = pd.DataFrame()

    def __init__(self):
        # Model class must be defined somewhere
        self.model = SiameseBannerRecognitionModelResNet50()
        # Load model from file - set path inside configs (maybe inside settings.py)
        print(self.model.model_path)
        self.model.load_state_dict(torch.load(self.model.model_path, map_location=torch.device('cpu')))
        # Inference preprocessed
        self.model.eval()
        # resize image configuration
        self.resize_aug = albumentations.Compose([albumentations.Resize(224, 224)])

    @staticmethod
    def ary2tensor(image_array, d_type=np.float32):
        """ Helper Function - Convert from numpy array into tensor
        :param image_array: numpy.ndarray
        :param d_type: np - Datatype
        :return: <class 'torch.Tensor'>
        """
        return torch.from_numpy(image_array.astype(d_type, copy=False))

    @staticmethod
    def open_image(path):
        """ Helper Function - Load file in PIL format
        :param path: string
        :return: <class 'PIL.Image.Image'>
        """
        return PIL.Image.open(path).convert('RGB')

    @staticmethod
    def image_net_normalize(image_tensor):
        """ Normalization image tensor using image net statistics parameters
        :param image_tensor: <class 'torch.Tensor'>
        :return: <class 'torch.Tensor'>
        """
        image_net_mean = [0.485, 0.456, 0.406]
        image_net_std = [0.229, 0.224, 0.225]
        mean = torch.from_numpy(np.array(image_net_mean).astype(np.float32))
        std = torch.from_numpy(np.array(image_net_std).astype(np.float32))
        zero_centered = image_tensor - mean[:, None, None]
        return zero_centered / std[:, None, None]

    @staticmethod
    def load_descriptors(self):
        self.BASE_IMAGES['Image'] = 0
        self.BASE_IMAGES['Id'] = 0

    def augment_resize(self, image_array):
        """ Resize with different types of augmentations
        :param image_array: numpy.ndarray
        :return: numpy.ndarray
        """
        return self.resize_aug(image=image_array)['image']

    def image2tensor(self, image, augment_fn=None):
        """ Base Function - Convert from numpy array into torch Tensor
        :param image: <class 'PIL.Image.Image'>
        :param augment_fn: method()
        :return: <class 'torch.Tensor'>
        """
        image_array = np.asarray(image)
        if augment_fn:
            image_array = augment_fn(image_array)
        image_array = image_array.transpose(2, 0, 1)
        image_tensor = self.ary2tensor(image_array)
        return image_tensor.div_(255)

    def get_descriptor(self, image):
        with torch.no_grad():
            tensor = self.image2tensor(image, augment_fn=self.augment_resize)
            image_tensor = self.image_net_normalize(tensor)
            image_tensor = image_tensor[np.newaxis, :]
            cnn_out = self.model.cnn(image_tensor)
            descriptor = self.model.ada_concat(cnn_out).squeeze().detach().cpu()
            return descriptor


class ObjectDetectionController(metaclass=Singleton):

    def __init__(self):
        """

        """
        self.detection_graph = tf.get_default_graph()
        self.detector = CustomObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("models/detection_model-ex-029--loss-0009.447.h5")
        self.detector.setJsonPath("models/detection_config_2.json")
        self.detector.loadModel()

    @staticmethod
    def crop_image(image, upper_left_corner, bottom_right_corner):
        """ Method which crop frame from base image using bounding box coordinates,
        bottom_right_corner coordinates and upper_left_coordinates
        :param image: numpy.ndarray
        :param upper_left_corner: tuple(int, int)
        :param bottom_right_corner: tuple(int, int)
        :return:
        """
        crop = image[upper_left_corner[1]:bottom_right_corner[1],
                     upper_left_corner[0]:bottom_right_corner[0]]
        return crop

    def banner_detection(self, billboard):
        """ Detect banners on billboard photo,
        return detected coordinates, name, image_path,
        :param billboard: BillboardImage object
        :return: dict()
        """
        with self.detection_graph.as_default():
            detections = self.detector.detectObjectsFromImage(
                input_image=os.path.join("media", billboard.image.name),
                output_image_path=os.path.join("media/detected_banners", billboard.image.name),
                minimum_percentage_probability=20,
                extract_detected_objects=True,
                nms_treshold=0.2,
            )
            return detections
