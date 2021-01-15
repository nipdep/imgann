#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC
import xml.etree.ElementTree as ET
import pandas as pd
import os
import re
import logging

# setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from .operator import IOperator


class PascalVOC(IOperator, ABC):

    """ Instance Object for pascal VOC annotation format """

    def __init__(self, dataset):
        super().__init__(dataset)
        self._dataset = dataset

    def extract(self, path: str):
        """ extract annotation data when input the path to .xml files

        :param path: string, relative / absolute path for annotation folder
        :return:
        """
        files_list = self.__extractFiles(path)
        image_id = 0
        img_list = []
        tol_obj_list = []
        for file in files_list:
            
            img_data, obj_list = self.__FileReader(os.path.abspath(path) + "\\" + file)
            image_id += 1
            img_data.append(image_id)
            obj_list = [i+[image_id] for i in obj_list]
            img_list.append(img_data)
            tol_obj_list.extend(obj_list)
        if img_list:
            img_df = pd.DataFrame.from_records(img_list, columns=['name', 'width', 'height','image_id'])
            self.__updateDataset(img_df)
        else:
            logger.error("[var]: img_list is empty.")

        if obj_list and len(obj_list[0]) == 6:
            obj_df = pd.DataFrame.from_records(tol_obj_list,
                                               columns=['x_min', 'y_min', 'x_max', 'y_max', 'class', 'image_id'])
            self.__DFRefiner(obj_df)
        else:
            logger.error(f"obj_list has not many attrs. : {len(obj_list[0])} or obj_list is empty : {len(obj_list)}")

    def archive(self, location: str, data):
        """ save pascalVOC annotation file in the given location

        :param location: .xml file saving location
        :param data: .xml daa bundle
        :return:
        """
        try:
            tree_str = ET.tostring(data)
            with open(location, 'wb') as pf:
                pf.write(tree_str)
        except Exception as error:
            logger.exception(error)
            assert error

    def translate(self):
        """ translate common schema into json compatible format.

        :return: none
        """
        for index, row in self._dataset.iterrows():
            ann_list = self.__filterImgObj(row['image_id'])
            box = self.__xmlFomatter(row, ann_list)
            if box:
                yield box, row['name']
            else:
                yield None

    def __extractFiles(self, path: str):
        """

        :param path: relative or absolute directory to the annotation folder.
        :return: return list of all .xml file names in given directory.
        """
        if os.path.exists(path):
            if not [x[1] for x in os.walk(path) if x[1] != []]:
                path_list = [y[2] for y in os.walk(path) if y[2] != []][0]
                if path_list:
                    xml_list = [n for n in path_list if n.split('.')[-1] == 'xml']
                    if xml_list:
                        return xml_list
                    else:
                        assert Exception("There are no .xml files in the given directory.")
                else:
                    assert Exception("The folder is empty.")
        else:
            assert Exception(f"The entered path <{path}> is not valid.")

    def __DFRefiner(self, ann_df):
        """
        create pd.DataFrame with columns of [ "obj_id", "image_id", "class_id", "x_min", "y_min", "x_max", "y_max" ] and
        define self.annotations and self.classes
        :param ann_df: pd.Dataframe with columns of [ 'x_min', 'y_min', 'x_max', 'y_max', 'class', 'image_id' ]
        :return: None
        """
        ann_df = ann_df.copy()

        cats = list(ann_df.loc[:, "class"].unique())
        n_cats = len(cats)
        cat_series = pd.Series(range(1, n_cats + 1), index=cats)

        ann_df["class_id"] = ann_df["class"].map(cat_series)
        ann_df["obj_id"] = range(1,ann_df.shape[0]+1)
        nw_df = ann_df.loc[:, ["obj_id", "image_id", "class_id", "x_min", "y_min", "x_max", "y_max"]]

        super(PascalVOC, self).set_annotations(nw_df)
        super(PascalVOC, self).set_classes(dict(zip(range(1,n_cats+1),cats)))

    def __FileReader(self, file_path: str):
        """ read individual xml files extract data, create pd.DataFrame files

        :param file_path: absolute path to the single .xml file
        :return: tuple of two list
         img_data = [ filename, width, height ]
         obj_list = [ class, xmin, ymin, xmax, ymax ]
        """
        ann_tree = ET.parse(file_path)
        ann_root = ann_tree.getroot()
        try:
            filename = self.__tagFilter(ann_root.find('filename').text)
            size = ann_root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            img_data = [filename, width, height]

            obj_list = []
            for obj in ann_root.findall('object'):
                obj_list.append(self.__get_coco_annotation_from_obj(obj))
        except Exception as error:
            logger.exception(error)
            assert error

        return [img_data, obj_list]

    def __get_coco_annotation_from_obj(self, obj):
        """ read <object> block in xml file

        :param obj: <object> block in the .xml file
        :return: a list of object attrs. [ class, xmin, ymin, xmax, ymax ]
        """
        try:
            label = self.__tagFilter(obj.find('name').text)
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            ann = [xmin, ymin, xmax, ymax, label]
            return ann
        except Exception as error:
            logger.exception(error)
            assert error

    def __updateDataset(self, image_df):
        """

        :param image_df: image attributes DataFrame
        :return: merge current self.__dataset with image_df.
        """
        partial_df = image_df.copy()
        res_df = pd.merge(self._dataset, partial_df, on="name")
        super(PascalVOC, self).set_dataset(res_df)

    def __filterImgObj(self, img_id):
        """ get row for specific image_id.

        :param img_id: [int] image_id in the self.annotations
        :return: all the row that carry given image_id as a list.
        """
        filtered_list = self.annotations.loc[self.annotations["image_id"] == int(img_id), :].values.tolist()
        return filtered_list

    def __xmlFomatter(self, image_data, ann_data):
        """ build the structure of the .xml file with data.

        :param image_data: dictionary for data in self._dataset
        :param ann_data: return values from self.__filterImgObj
        :return: complete .xml object
        """
        try:
            ann = ET.Element("annotation")
            ET.SubElement(ann, 'folder').text = image_data['folder']
            ET.SubElement(ann, 'filename').text = image_data['name']
            ET.SubElement(ann, 'path').text = image_data['path']
            size = ET.SubElement(ann, 'size')
            ET.SubElement(size, 'width').text = str(image_data['width'])
            ET.SubElement(size, 'height').text = str(image_data['height'])
            ET.SubElement(size, 'depth').text = str(3)
            for line in ann_data:
                obj = ET.SubElement(ann, 'object')
                ET.SubElement(obj, 'name').text = self.classes[line[2]]
                ET.SubElement(obj, 'pose').text = 'Unspecified'
                ET.SubElement(obj, 'truncated').text = str(0)
                ET.SubElement(obj, 'difficult').text = str(0)
                bbox = ET.SubElement(obj, 'bndbox')
                ET.SubElement(bbox, 'xmin').text = str(line[3])
                ET.SubElement(bbox, 'ymin').text = str(line[4])
                ET.SubElement(bbox, 'xmax').text = str(line[5])
                ET.SubElement(bbox, 'ymax').text = str(line[6])
            return ann
        except Exception as error:
            logger.exception(error)
            assert error

    def __tagFilter(self,st: str):
        s = re.sub(r'\t*\n*\r*', '', st)
        return s
