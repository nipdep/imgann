#!/usr/bin/python
# -*- coding: utf-8 -*-

from .operators.imgdata import ImgData
from .operators import coco, csv, pascalvoc, yolo
import logging
import os

# set logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Convertor:

    """ convert method implementation class """

    @staticmethod
    def coco2csv(dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str,
                 center: bool = True,
                 is_multilabel: bool = False):
        """convert coco to csv format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            coco_ann_dir (str):  relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .csv file saving location
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
            is_multilabel (bool, optional): directly convert to TF multi-label One-Hot encoded version without bbox data. Defaults to False.
        """
        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir, center)
        df = coco_obj.get_dataset()
        ann, clas = coco_obj.get_annotations()

        csv_obj = csv.CSV(df)
        csv_obj.set_annotations(ann)
        csv_obj.set_classes(clas)
        csv_fomatted = csv_obj.translate(is_multilabel)
        csv_obj.archive(save_dir, csv_fomatted)

    @staticmethod
    def coco2voc(dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str,
                 center: bool = True):
        """convert coco to pascal VOC format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            coco_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str):  .xml files saving location
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir, center)
        df = coco_obj.get_dataset()
        ann, cls = coco_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(df)
        voc_obj.set_annotations(ann)
        voc_obj.set_classes(cls)
        for xml, name in voc_obj.translate():
            file_dir = save_dir + '/' + '.'.join(name.split('.')[:-1])+'.xml'
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def coco2yolo(dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str,
                 center: bool = True):
        """convert coco to yolo format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            coco_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .txt files saving location
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir, center)
        df = coco_obj.get_dataset()
        ann, cls = coco_obj.get_annotations()

        yolo_obj = yolo.Yolo(df)
        yolo_obj.set_annotations(ann)
        yolo_obj.set_classes(cls)
        for data, name in yolo_obj.translate():
            file_dir = save_dir + '/' + '.'.join(name.split('.')[:-1])+'.txt'
            yolo_obj.archive(file_dir, data)

    @staticmethod
    def csv2coco(dataset_dir: str,
                 csv_ann_dir: str,
                 save_dir: str,
                 center: bool = True):
        """convert .csv into coco format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .json file saving location
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        imagedataset = ImgData.extract(dataset_dir)
        csv_obj = csv.CSV(imagedataset.dataset)
        csv_obj.extract(csv_ann_dir)
        df = csv_obj.get_dataset()
        ann, cls = csv_obj.get_annotations()

        coco_obj = coco.COCO(df)
        coco_obj.set_annotations(ann)
        coco_obj.set_classes(cls)
        data = coco_obj.translate(center)
        coco_obj.archive(save_dir, data)

    @staticmethod
    def csv2voc(dataset_dir: str,
                csv_ann_dir: str,
                save_dir: str):
        """convert .csv into pascal VOC format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .xml files saving location
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
            file_dir = save_dir + '/' + '.'.join(name.split('.')[:-1])+'.xml'
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def csv2yolo(dataset_dir: str,
                csv_ann_dir: str,
                save_dir: str):
        """convert .csv into pascal yolo format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .txt files saving location
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        imagedataset = ImgData.extract(dataset_dir)
        csv_obj = csv.CSV(imagedataset.dataset)
        csv_obj.extract(csv_ann_dir)
        df = csv_obj.get_dataset()
        ann, cls = csv_obj.get_annotations()

        yolo_obj = yolo.Yolo(df)
        yolo_obj.set_annotations(ann)
        yolo_obj.set_classes(cls)
        for data, name in yolo_obj.translate():
            file_dir = save_dir + '/' + '.'.join(name.split('.')[:-1])+'.txt'
            yolo_obj.archive(file_dir, data)

    @staticmethod
    def voc2coco(dataset_dir: str,
                 voc_ann_dir: str,
                 save_dir: str,
                 center: bool = True):
        """convert Pascal-VOC to COCO format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .json file saving location,
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset.dataset)
        voc_obj.extract(voc_ann_dir)
        df = voc_obj.get_dataset()
        ann, cls = voc_obj.get_annotations()

        coco_obj = coco.COCO(df)
        coco_obj.set_annotations(ann)
        coco_obj.set_classes(cls)
        data = coco_obj.translate(center)
        coco_obj.archive(save_dir, data)

    @staticmethod
    def voc2csv(dataset_dir: str,
                voc_ann_dir: str,
                save_dir: str,
                is_multilabel: bool = False):
        """convert Pascal-VOC to csv format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .csv file saving location,
            is_multilabel (bool, optional): directly convert to TF multi-label One-Hot encoded version without bbox data. Defaults to False.
        """
        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset.dataset)
        voc_obj.extract(voc_ann_dir)
        df = voc_obj.get_dataset()
        ann, cls = voc_obj.get_annotations()

        csv_obj = csv.CSV(df)
        csv_obj.set_annotations(ann)
        csv_obj.set_classes(cls)
        csv_fomatted = csv_obj.translate(is_multilabel)
        csv_obj.archive(save_dir, csv_fomatted)

    @staticmethod
    def voc2yolo(dataset_dir: str,
                voc_ann_dir: str,
                save_dir: str):
        """convert Pascal-VOC to yolo format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .txt files saving location,
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset.dataset)
        voc_obj.extract(voc_ann_dir)
        df = voc_obj.get_dataset()
        ann, cls = voc_obj.get_annotations()

        yolo_obj = yolo.Yolo(df)
        yolo_obj.set_annotations(ann)
        yolo_obj.set_classes(cls)
        for data, name in yolo_obj.translate():
            file_dir = save_dir + '/' + '.'.join(name.split('.')[:-1])+'.txt'
            yolo_obj.archive(file_dir, data)

    @staticmethod
    def csv2multilabel(csv_dir: str,
                       save_dir: str):
        """Convert Object detection related annotation formatted .csv file into classification related .csv file

        Args:
            csv_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .csv file saving location

        Returns:
            None | save .csv file in <save_dir> location
        """
        csv_obj = csv.CSV(csv_dir)
        df = csv_obj.to_multilabel(csv_dir)
        csv_obj.archive(save_dir, df)

    @staticmethod
    def yolo2coco(dataset_dir: str,
                  yolo_ann_dir: str,
                  save_dir: str,
                  center: bool = True):

        """convert yolo to coco format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .json file saving location
            center (bool, optional): wether in KITTI bbox contains (X_center, Y_center, ...) or (X_min, Y_min, ...). Defaults to True.
        """
        imagedataset = ImgData.extract(dataset_dir)
        yolo_obj = yolo.Yolo(imagedataset.dataset)
        yolo_obj.extract(yolo_ann_dir)
        df = yolo_obj.get_dataset()
        ann, cls = yolo_obj.get_annotations()

        coco_obj = coco.COCO(df)
        coco_obj.set_annotations(ann)
        coco_obj.set_classes(cls)
        data = coco_obj.translate(center)
        coco_obj.archive(save_dir, data)

    @staticmethod
    def yolo2voc(dataset_dir: str,
                 yolo_ann_dir: str,
                 save_dir: str):
        """convert yolo to Pascal-VOC format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .xml files saving location
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        imagedataset = ImgData.extract(dataset_dir)
        yolo_obj = yolo.Yolo(imagedataset.dataset)
        yolo_obj.extract(yolo_ann_dir)
        df = yolo_obj.get_dataset()
        ann, cls = yolo_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(df)
        voc_obj.set_annotations(ann)
        voc_obj.set_classes(cls)
        for xml, name in voc_obj.translate():
            file_dir = save_dir + '/' + '.'.join(name.split('.')[:-1])+'.xml'
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def yolo2csv(dataset_dir: str,
                 yolo_ann_dir: str,
                 save_dir: str,
                 is_multilabel: bool = False):
        """convert yolo to csv format

        Args:
            dataset_dir (str): relative path current folder, or absolute path to the main folder of the image dataset
            csv_ann_dir (str): relative path current folder, or absolute path to the main folder of the annotated file
            save_dir (str): .csv file saving location
            is_multilabel (bool, optional): directly convert to TF multi-label One-Hot encoded version without bbox data. Defaults to False.
        """
        imagedataset = ImgData.extract(dataset_dir)
        yolo_obj = yolo.Yolo(imagedataset.dataset)
        yolo_obj.extract(yolo_ann_dir)
        df = yolo_obj.get_dataset()
        ann, cls = yolo_obj.get_annotations()

        csv_obj = csv.CSV(df)
        csv_obj.set_annotations(ann)
        csv_obj.set_classes(cls)
        csv_fomatted = csv_obj.translate(is_multilabel)
        csv_obj.archive(save_dir, csv_fomatted)