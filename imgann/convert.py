#!/usr/bin/python
# -*- coding: utf-8 -*-

from .operators.imgdata import ImgData
from .operators import coco, csv, pascalvoc
import logging
import os

# set logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Convertor:

    """ convert method implementation class """

    @classmethod
    def coco2csv(cls, dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str):
        """ convert coco to csv

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param coco_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir)
        df = coco_obj.get_dataset()
        ann, clas = coco_obj.get_annotations()

        csv_obj = csv.CSV(df)
        csv_obj.set_annotations(ann)
        csv_obj.set_classes(clas)
        csv_fomatted = csv_obj.translate()
        csv_obj.archive(save_dir, csv_fomatted)

    @staticmethod
    def coco2voc(dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str):
        """ convert coco to pascal VOC

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param coco_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir)
        df = coco_obj.get_dataset()
        ann, cls = coco_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(df)
        voc_obj.set_annotations(ann)
        voc_obj.set_classes(cls)
        for xml, name in voc_obj.translate():
            file_dir = save_dir + '/' + name.split('.')[0]+'.xml'
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def csv2coco(dataset_dir: str,
                 csv_ann_dir: str,
                 save_dir: str):
        """ convert .csv into coco

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param csv_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        csv_obj = csv.CSV(imagedataset.dataset)
        csv_obj.extract(csv_ann_dir)
        df = csv_obj.get_dataset()
        ann, cls = csv_obj.get_annotations()

        coco_obj = coco.COCO(df)
        coco_obj.set_annotations(ann)
        coco_obj.set_classes(cls)
        data = coco_obj.translate()
        coco_obj.archive(save_dir, data)

    @staticmethod
    def csv2voc(dataset_dir: str,
                csv_ann_dir: str,
                save_dir: str):
        """ convert .csv into pascal VOC

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param csv_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        imagedataset = ImgData.extract(dataset_dir)
        csv_obj = csv.CSV(imagedataset.dataset)
        csv_obj.extract(csv_ann_dir)
        df = csv_obj.get_dataset()
        ann, cls = csv_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(df)
        voc_obj.set_annotations(ann)
        voc_obj.set_classes(cls)
        for xml, name in voc_obj.translate():
            file_dir = save_dir + '/' + name.split('.')[0]+'.xml'
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def voc2coco(dataset_dir: str,
                 voc_ann_dir: str,
                 save_dir: str):
        """ convert pascal VOC into coco

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param voc_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset.dataset)
        voc_obj.extract(voc_ann_dir)
        df = voc_obj.get_dataset()
        ann, cls = voc_obj.get_annotations()

        coco_obj = coco.COCO(df)
        coco_obj.set_annotations(ann)
        coco_obj.set_classes(cls)
        data = coco_obj.translate()
        coco_obj.archive(save_dir, data)

    @staticmethod
    def voc2csv(dataset_dir: str,
                voc_ann_dir: str,
                save_dir: str):
        """ convert pascal VOC into .csv

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param voc_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset.dataset)
        voc_obj.extract(voc_ann_dir)
        df = voc_obj.get_dataset()
        ann, cls = voc_obj.get_annotations()

        csv_obj = csv.CSV(df)
        csv_obj.set_annotations(ann)
        csv_obj.set_classes(cls)
        csv_fomatted = csv_obj.translate()
        csv_obj.archive(save_dir, csv_fomatted)
