#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import logging
import random

# set logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

""":param
ann_df attributes:
    - obj_id : int
    - image_id : int
    - class_id : int
    - x_min : int
    - y_min : int
    - x_max : int
    - y_max : int
"""
""":param
render format
    - image path
    - box : [[(x_min, y_min), (x_max, y_max)], ...]
    - classes : [str, ...]
"""

""":param
classes
{class_id[int] : class_name[str], ... }
"""


class IOperator(object):
    """ Operator Abstract class """

    def __init__(self, dataset):
        self._dataset = dataset

    def set_dataset(self, df):
        """
        :param df: pandas.DataFrame type object with attr. defined in the ImgData.py file

        save new dataset into the objects' private variable.
        """
        if type(df) is pd.DataFrame:
            self._dataset = df
        else:
            logger.error(f"Data type of df : {type(df)} not compatible with database object.")

    def get_dataset(self):
        """
        :return pandas.DataFrame
        """
        return self._dataset

    def get_annotations(self):
        """
        :return: data in annotation file [pd.Dataframe] & classes in a dictionary
        """
        try:
            if self.annotations.shape[0] and self.classes:
                return self.annotations, self.classes
            else:
                return
        except Exception as error:
            logger.exception(error)
            assert error

    def set_annotations(self, ann):
        """

        :param ann: data in annotation file [pd.Dataframe]
        :return:
        """
        self.annotations = ann

    def set_classes(self, classes):
        """

        :param classes: classes in a dictionary
        :return:
        """
        self.classes = classes

    @abstractmethod
    def extract(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def translator(self):
        raise NotImplementedError

    @abstractmethod
    def archive(self, location, data):
        raise NotImplementedError

    def descFormat(self):
        # TODO: make nice format to show descibe result.
        pass

    def describe(self):
        # TODO: annotation file description
        pass

    def sample(self, numOfSamples):
        """
        choose set of images randomly and get bounding boxes of them
        :return: dictionary list of [{"image_id" : "name", "classes" : [], "categories" : []}]
        """
        numOfrecords, _ = self._dataset.shape
        rnd_numbers = sorted(random.sample(range(0, numOfrecords), numOfSamples))
        sample_df = self._dataset.iloc[rnd_numbers, :]
        image_list = list(sample_df.loc[:, "image_id"].values)
        image_paths = list(sample_df.loc[:, "path"].values)
        sampled_anns = self.annotations.loc[self.annotations.loc[:, "image_id"].isin(image_list), :]
        final_list = []
        for image_id, image_path in zip(image_list, image_paths):
            ann_for_image = sampled_anns.loc[sampled_anns.loc[:, "image_id"] == image_id, :]
            spares_list = ann_for_image.values.tolist()
            ordered_dict = self.__listGen(spares_list)
            ordered_dict["image_id"] = image_id
            ordered_dict["path"] = image_path
            final_list.append(ordered_dict)
        return final_list

    def render(self, path: str, boxes: list, cls: list, rect_th=1, text_size=0.5, text_th=1):
        """ show annotated image

        :param path: directory to image
        :param boxes: all the bounding boxes in [[(),()], ...]
        :param cls: list of class names
        :param rect_th: thickness of he box :int
        :param text_size: font size
        :param text_th: thickness of the text :int
        :return: matplotlib.pyplot.plt object / a image.
        """
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for i in range(len(boxes)):
            # print(boxes[i][0], boxes[i][1])
            cv2.rectangle(img, boxes[i][0], boxes[i][1], color=(14, 14, 14), thickness=rect_th)
            cv2.putText(img, cls[i],
                        boxes[i][0], cv2.FONT_HERSHEY_COMPLEX,
                        text_size, color=(1, 1, 1), thickness=text_th)
        plt.figure(figsize=(30, 30))
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.show()
        return

    def __listGen(self, data_list):
        """

        :param data_list: [obj_id, class_id, class_id , x_min, y_min, x_max, y_max]
        :return: two list {"classes" : [classes, ..] , "bbox" : [[(x_min, y_min), (x_max, y_max)], ..]}
        """
        bounding_boxes = []
        classes = []
        for obj in data_list:
            classes.append(obj[2])
            bounding_boxes.append([(obj[3], obj[4]), (obj[5], obj[6])])
        final_dict = {"classes": classes, "bbox": bounding_boxes}
        return final_dict
