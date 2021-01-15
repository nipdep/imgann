#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from .operators.imgdata import ImgData
from .operators import coco, csv, pascalvoc

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


class Sample:

    """ Data Annotation file sampling interface """

    @classmethod
    def show_samples(cls, data_path: str,
                     ann_path: str,
                     num_of_samples: int = 5,
                     ann_type: str = 'coco'):
        """ render set of random images from dataset.

        :param data_path: relative path current folder, or absolute path to the main folder of the image dataset
        :param ann_path: relative path current folder, or absolute path to the main folder of the annotated file
        :param ann_type: one of type from ['coco', 'voc', 'csv', 'yolo']
        :param num_of_samples: number of sample images in integer format.
        :return: render sequence of images.
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
            obj = csv.IOperator(imgdataset.dataset)
        else:
            assert Exception(f"ERROR: {ann_type} is not a valid annotation type.")

        obj.extract(ann_path)
        obj_list = obj.sample(num_of_samples)
        cat_dict = obj.classes
        for img_obj in obj_list:
            path = img_obj["path"]
            obj_data = img_obj["bbox"]
            cat_name = [cat_dict[j] for j in img_obj["classes"]]
            obj.render(path, obj_data, cat_name)
        return
