#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
from typing import List

from .operators.imgdata import ImgData
from .operators import coco, csv, pascalvoc, yolo

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
### obj_lis : attributes ###
{
    ["classes" : [int, ..],
    "bbox" : [[(x_min, y_min), (x_max, y_max)], ..],
    "image_id" : int,
    "path: : str], ..
}
"""
""" render set of random images from dataset.

        :param data_path: relative path current folder, or absolute path to the main folder of the image dataset
        :param ann_path: relative path current folder, or absolute path to the main folder of the annotated file
        :param ann_type: one of type from ['coco', 'voc', 'csv']
        :param num_of_samples: number of sample images in integer format.
        :return: render sequence of images.
        """


class Sample:
    """ Data Annotation file sampling interface """

    @staticmethod
    def show_samples(data_path: str,
                     ann_path: str,
                     num_of_samples: int = 5,
                     ann_type: str = 'coco',
                     center: bool = True,
                     image_shape: List[int] = [300, 300],
                     seed: int = 0):
        """render a set of random images from dataset with annotations.

        Args:
            data_path (str): relative path current folder, or absolute path to the main folder of the image dataset
            ann_path (str): relative path current folder, or absolute path to the main folder of the annotated file
            num_of_samples (int, optional): number of samples to show. Defaults to 5.
            ann_type (str, optional): annotation type of the file in 'ann_path', from one of type from ['coco', 'voc', 'csv']. Defaults to 'coco'.
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
            image_shape (List[int], optional): output image size in pixels. Defaults to [300, 300].
            seed (int, optional): set random-state for consintent outputs, else function given different set at each run. Defaults to 0.
        """

        global obj
        imgdataset = ImgData.extract(data_path)
        if ann_type == 'coco':
            obj = coco.COCO(imgdataset.dataset)
        elif ann_type == 'voc':
            obj = pascalvoc.PascalVOC(imgdataset.dataset)
        elif ann_type == 'csv':
            obj = csv.CSV(imgdataset.dataset)
        elif ann_type == 'yolo':
            obj = yolo.Yolo(imgdataset.dataset)
        else:
            logger.error(
                f"\nERROR: '{ann_type}' is not a valid annotation type.")
            sys.exit(1)

        if ann_type == 'coco':
            obj.extract(ann_path, center)
        else:
            obj.extract(ann_path)
        
        obj_list = obj.sample(num_of_samples, seed)
        cat_dict = obj.classes
        for img_obj in obj_list:
            path = img_obj["path"]
            obj_data = img_obj["bbox"]
            cat_name = [cat_dict[j] for j in img_obj["classes"]]
            obj.render(path, obj_data, cat_name, image_shape)
        return

    @staticmethod
    def describe_data(data_path: str):
        """give a summary of a image dataset

        Args:
            data_path (str): absolute or relative path to image dataset main folder
        """
        img_dataset = ImgData.extract(data_path)
        data_dict = img_dataset.describe()
        log_st = Sample.descFormat("image data summary", data_dict)
        logger.info("\n"+log_st)
        return

    @staticmethod
    def describe_ann(data_path: str,
                     ann_path: str, ann_type: str = 'coco', center: bool = True):
        """give summary of annotated dataset

        Args:
            data_path (str): absolute or relative path to image dataset main folder
            ann_path (str): absolute or relative path to image annotation file or folder
            ann_type (str, optional): annotation type of the file in 'ann_path', from one of type from ['coco', 'voc', 'csv']. Defaults to 'coco'.
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        imgdataset = ImgData.extract(data_path)
        if ann_type == 'coco':
            obj = coco.COCO(imgdataset.dataset)
        elif ann_type == 'voc':
            obj = pascalvoc.PascalVOC(imgdataset.dataset)
        elif ann_type == 'csv':
            obj = csv.CSV(imgdataset.dataset)
        elif ann_type == 'yolo':
            obj = yolo.Yolo(imgdataset.dataset)
        else:
            logger.error(
                f"\n ERROR : {ann_type} is not a valid annotation type.")
            sys.exit(1)

        if ann_type == 'coco':
            obj.extract(ann_path, center)
        else:
            obj.extract(ann_path)
        log_data = obj.describe()
        log_st = Sample.descFormat("image annotation summary", log_data)
        logger.info("\n"+log_st)
        return

    @staticmethod
    def descFormat(header, data):
        """give formatted string for data

        Args:
            header (_type_): header name of the summary
            data (_type_): dictionary of data {field : value}

        Returns:
            _type_: formatted string of all data.
        """
        log_string = ""
        log_header = "{0:^80s}\n{1:s}\n".format(header.upper(), '=' * 80)
        log_string += log_header

        wd = Sample.__getMax(data.keys())
        log_data = ""
        for sec in data:
            if type(data[sec]) == str:
                st = "{0:<{1:d}s} : {2:}\n".format(sec, wd, data[sec])
                log_data += st
            elif type(data[sec]) == int:
                st = "{0:<{1:d}s} : {2:d}\n".format(sec, wd, data[sec])
                log_data += st
            elif type(data[sec]) == dict:
                sub_wd = Sample.__getMax(data[sec].keys())
                sub_topic = "{0:<{1:d}s} :\n".format(sec, wd)
                log_data += sub_topic
                for sub_elem in data[sec]:
                    sub_data = "{0:<{1:d}s} > {2:<{3:d}} : {4:}\n".format(
                        " ", wd, sub_elem, sub_wd, data[sec][sub_elem])
                    log_data += sub_data
        log_data += "{0:s}\n".format("="*80)
        log_string += log_data
        return log_string

    @staticmethod
    def __getMax(ls):
        """

        :param ls: list of string
        :return: length of maximum length string in the list
        """
        elem = max(ls, key=len)
        return len(elem)
