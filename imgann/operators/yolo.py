#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC
import os
import pathlib 
import sys 
import logging
from unicodedata import name 
import pandas as pd 
from pathlib import Path
import PIL 

# setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from .operator import IOperator

class Yolo(IOperator, ABC):
    """ Instance Objec for YOLO annotation format"""
    
    def __init__(self, dataset):
        super().__init__(dataset)
        self._dataset = dataset 

    def extract(self, path:str):
        """extract data from .txt annotation files and update super attributes

        Args:
            path (str): root path for the all annotation & image files
        """
        image_paths, image_files = self.__getAllPaths(path, ['png', 'jpg', 'jpeg'])
        image_df = self.__getImageData(image_paths)
        self.__updateDataset(image_df)

        ann_paths, ann_files = self.__getAllPaths(path, '*.txt')
        name_dict = dict(zip(['.'.join(i.split('.')[:-1]) for i in image_df['name'].values], image_df.loc[:, ['image_id', 'width', 'height']].values))
        ann_df = self.__getAnnData(ann_paths, name_dict)
        self.__DFRefiner(ann_df)

    def archive(self, location: str, data):
        """save Yolo Annotated .txt file in the given location

        Args:
            location (str): .txt saving path
            data (str): string of data
        """
        try:
            with open(location, 'w') as pf:
                pf.write(data)
        except Exception as error:
            logger.exception(error)
            sys.exit(1)

    def translate(self):
        """translate from common format to .txt compatible bbox format

        Yields:
            List[List, str]: list of all a image related bounding boxes data and image name
        """
        for _, r in self._dataset.iterrows():
            ann_list = self.__filterImgObj(r['image_id'])
            data = self.__txtFormatter(ann_list, r['width'], r['height'])
            if data:
                yield data, r['name']
            else:
                yield None

    def __txtFormatter(self, ann_data, iw, ih):
        """convert bbox-list to string to save in .txt file

        Args:
            ann_data (List[List]): bbox data related to the image
            iw (int): image width
            ih (int): image height

        Returns:
            str: a string of all annotation data
        """
        ann_str_list = []
        for bbox in ann_data:
            _, _, l, xmin, ymin, xmax, ymax = bbox 
            x_o, y_o, bw, bh = self.__KITTI2normilized(xmin, ymin, xmax, ymax)
            x_o, y_o, bw, bh = x_o/iw, y_o/ih, bw/iw, bh/ih 
            bbox_str = f'{l} {x_o} {y_o} {bw} {bh}\n'
            ann_str_list.append(bbox_str)
        ann_str = ''.join(ann_str_list)
        return ann_str 

    def __filterImgObj(self, img_id):
        """ get row for specific image_id.

        :param img_id: [int] image_id in the self.annotations
        :return: all the row that carry given image_id as a list.
        """
        filtered_list = self.annotations.loc[self.annotations["image_id"] == img_id, :].values.tolist()
        return filtered_list

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

        super(Yolo, self).set_annotations(nw_df)
        super(Yolo, self).set_classes(dict(zip(range(1,n_cats+1),cats)))

    def __getAnnData(self, ann_paths, name_dict):
        """build annotation data for the dataset

        Args:
            ann_paths (List[str]): all annotation file paths
            name_dict (Dict): dictionary object in format {image_name: [image_id, width, height]}

        Returns:
            pd.DataFrame: data-frame with columns of ['x_min', 'y_min', 'x_max', 'y_max', 'class', 'image_id']
        """
        image_anns = []
        for p in ann_paths:
            fname = '.'.join(p.split('\\')[-1].split('.')[:-1])
            image_id, iw, ih = name_dict[fname]
            obj_list = self.__extractAnn(p, iw, ih)
            obj_list = [i+[image_id] for i in obj_list]
            image_anns.extend(obj_list)
        ann_df = pd.DataFrame.from_records(image_anns,columns=['x_min', 'y_min', 'x_max', 'y_max', 'class', 'image_id'])
        return ann_df

    def __extractAnn(self, fpath, w, h):
        """extract image annotation data from the .txt file

        Args:
            fpath (str): .txt file relative path
            w (int): image original width
            h (int): image original height

        Returns:
            List[List]: image annotation data list with [x_min, y_min, x_max, y_max, label]
        """
        obj_list = []
        with open(fpath, 'r') as pf:
            for l in pf.readlines():
                label, x_o, y_o, bw, bh = [float(i) for i in l.rstrip('\n').split(' ')]
                bbox_val = self.__normalized2KITTI([int(w*x_o), int(h*y_o), int(w*bw), int(h*bh)])+[str(label)]
                obj_list.append(bbox_val)
        return obj_list


    def __normalized2KITTI(self, box, center=True):
        """

        :param box: [X, Y, width, height]
        :return: [(xmin, ymin), (xmax, ymax)]
        """
        o_x, o_y, o_width, o_height = box
        if center:  
            xmin = int(o_x - o_width / 2)
            ymin = int(o_y - o_height / 2)
            xmax = int(o_x + o_width / 2)
            ymax = int(o_y + o_height / 2)
        else:
            xmin = o_x
            ymin = o_y
            xmax = int(o_x + o_width)
            ymax = int(o_y + o_height)
        return [xmin, ymin, xmax, ymax]

    def __KITTI2normilized(self, xmin, ymin, xmax, ymax, center=True):
        """

        :param xmin:
        :param ymin:
        :param xmax:
        :param ymax:
        :return: [X, Y, width, height]
        """
        if center:
            width = xmax - xmin
            height = ymax - ymin
            x0 = (xmax + xmin) // 2
            y0 = (ymin + ymax) // 2
        else:
            width = xmax - xmin
            height = ymax - ymin
            x0 = xmin
            y0 = ymin
        return [x0, y0, width, height]

    def __updateDataset(self, image_df):
        """

        :param image_df: image attributes DataFrame
        :return: merge current self.__dataset with image_df.
        """
        partial_df = image_df.copy()
        res_df = pd.merge(self._dataset, partial_df, on="name")
        super(Yolo, self).set_dataset(res_df)
        
    def __getImageData(self, image_plist):
        """extract image size data

        Args:
            image_plist (str): relative path to image files

        Returns:
            pd.DataFrame: data-frame with columns of [name, width, height, image_id]
        """
        image_name, image_width, image_height = [], [], []
        for p in image_plist:
            image_name.append(p.split('\\')[-1])
            im = PIL.Image.open(p)
            w, h = im.size
            image_height.append(h)
            image_width.append(w)
        image_df = pd.DataFrame({'name': image_name, 'width': image_width, 'height': image_height, 'image_id': list(range(len(image_height)))})
        return image_df


    def __getAllPaths(self, root_path, extensions):
        if isinstance(extensions, str):
            file_list = [path.name for path in Path(root_path).rglob(extensions)]
            path_list = [str(path) for path in Path(root_path).rglob(extensions)]
        else:
            file_list, path_list = [], []
            for e in extensions:
                file_list.extend([path.name for path in Path(root_path).rglob(f'*.{e}')])
                path_list.extend([str(path) for path in Path(root_path).rglob(f'*.{e}')])

        return path_list, file_list