#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC
import json
import os
import pandas as pd
import logging
import sys


# setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from .operator import IOperator


class COCO(IOperator, ABC):

    """ Instance Object for COCO annotation format """

    def __init__(self, dataset):
        super(COCO, self).__init__(dataset)
        self._dataset = dataset

    def extract(self, path: str, center):
        """
        all the annotations in the file convert into general dataframe object.
        :param path: string, relative / absolute path
        :return: generalize pandas.DataFrame type object.
        """
        if os.path.exists(path):
            with open(path) as fp:
                ann_data = json.load(fp)
            self.__updateDataset(ann_data["images"])
            self.__extractAnnotation(ann_data["annotations"], center)
            self.__extractClasses(ann_data["categories"])
        else:
            logger.error(f"\n ERROR : entered path <{path}> is invalid.")
            sys.exit(1)

        return

    def archive(self, location, data):
        """ save coco annotation file in the given location

        :param location: .json file saving directory
        :param data: dictionary to save as .json
        :return: none
        """
        if os.path.exists(os.path.dirname(location)):
            if data:
                with open(location, 'w') as pf:
                    json.dump(data, pf)
            else:
                logger.error("\n ERROR : The DataFrame file is empty.")
                sys.exit(1)
        else:
            logger.error("\n ERROR : There are no such parent directory to file save.")
            sys.exit(1)

    def translate(self, center):
        """ translate common schema into json compatible format.

        :return:
        """
        data = {}
        data["annotations"] = []
        data["images"] = []
        data["categories"] = []

        filenames = self._dataset["name"].to_list()
        widths = self._dataset["width"].to_list()
        heights = self._dataset["height"].to_list()
        ids = self._dataset["image_id"].to_list()
        compact_image_list = zip(filenames, heights, widths, ids)

        for line in compact_image_list:
            data["images"].append(self.__list2dict(['file_name', 'height', 'width', 'id'], line))

        obj_ids = self.annotations["obj_id"].astype('int32')
        image_ids = self.annotations["image_id"].astype('int32')
        cat_ids = self.annotations["class_id"].astype('int32')
        xmins = self.annotations["x_min"].astype('int32')
        ymins = self.annotations["y_min"].astype('int32')
        xmaxs = self.annotations["x_max"].astype('int32')
        ymaxs = self.annotations["y_max"].astype('int32')
        bboxs = []
        areas = []
        for i in range(len(xmaxs)):
            bboxs.append(self.__KITTI2normilized(xmins[i], ymins[i], xmaxs[i], ymaxs[i], center))
            areas.append((xmaxs[i] - xmins[i]) * (ymaxs[i] - ymins[i]))

        compact_ann_list = zip(obj_ids, image_ids, cat_ids, areas, bboxs)
        for line in compact_ann_list:
            data["annotations"].append(
                self.__list2dict(["id", "image_id", "category_id", "area", "bbox", "ignore", "iscrowd"], line))

        class_ids = list(self.classes.keys())
        class_names = list(self.classes.values())
        compact_class_list = zip(class_ids, class_names)
        for line in compact_class_list:
            data["categories"].append(self.__list2dict(["id", "name", "supercategory"], line, padd='none'))

        return data

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

    def __updateDataset(self, images):
        """

        :param images: image attributes in the .json file
        :return: add id, image width & height columns to self.dataset
        """
        dataset_imgs = list(self._dataset.iloc[:, 0].values)
        ann_imgs = []
        ann_id = {}
        img_width = {}
        img_height = {}
        for obj in images:
            if obj["file_name"] in dataset_imgs:
                try:
                    ann_imgs.append(obj["file_name"])
                    ann_id[obj["file_name"]] = obj["id"]
                    img_width[obj["file_name"]] = obj["width"]
                    img_height[obj["file_name"]] = obj["height"]
                except Exception as error:
                    logger.exception("\n ERROR : annotation file doesn't in accept the format.")
                    pass
        if len(dataset_imgs) > len(ann_imgs):
            self._dataset = self._dataset.loc[self._dataset.loc[:, "name"].isin(ann_imgs), :]
            logger.warning("\nWARNING: all the images had not annotated!")
        self._dataset = self._dataset.copy()
        self._dataset["image_id"] = self._dataset["name"].map(ann_id)
        self._dataset.loc[:, "width"] = self._dataset.loc[:, "name"].map(img_width)
        self._dataset.loc[:, "height"] = self._dataset.loc[:, "name"].map(img_height)
        super(COCO, self).set_dataset(self._dataset)
        return

    def __extractAnnotation(self, anns, center):
        """

        :param anns: annotation attribute in the .json file
        :return: None , add self.annotations attr.
        """
        ann_list = []
        for obj in anns:
            try:
                obj_id = obj["id"]
                img_id = obj["image_id"]
                cls_id = obj["category_id"]
                x_min, y_min, x_max, y_max = self.__normalized2KITTI(obj["bbox"], center)
                #logger.info(print(f'obj_id : {obj_id} | image_id : {img_id} | normalized : {obj["bbox"]} > KITTI : {[x_min, y_min, x_max, y_max]}'))
            except Exception as error:
                logger.exception("\n ERROR : annotation file doesn't in accept the format.")
                sys.exit(1)
            else:
                ann_list.append((obj_id, img_id, cls_id, x_min, y_min, x_max, y_max))

        if ann_list:
            ann_df = pd.DataFrame.from_records(ann_list,
                                               columns=['obj_id', 'image_id', 'class_id', 'x_min', 'y_min', 'x_max',
                                                        'y_max'])
            super(COCO, self).set_annotations(ann_df)
        else:
            super(COCO, self).set_annotations(pd.DataFrame())

    def __extractClasses(self, cats):
        """

        :param cats: categories attribute in the .json file
        :return: dictionary object of type {id : class-name}
        """
        if len(cats) > 0:
            class_dict = {}
            for obj in cats:
                try:
                    class_dict[obj["id"]] = obj["name"]
                except Exception as error:
                    logger.exception("\n ERROR : annotation file doesn't in accept the format.")
                    sys.exit(1)

            super(COCO, self).set_classes(class_dict)
        else:
            logger.error("\n ERROR : There are no distinctive class definition in the annotation.")
            sys.exit(1)
            super(COCO, self).set_classes({})

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

    def __list2dict(self, tags, values, padd='0'):
        nt = len(tags)
        nv = len(values)
        if nt >= nv:
            ret_dict = {}
            for i in range(nt):
                if i < nv:
                    #ret_dict[tags[i]] = str(values[i])
                    if isinstance(values[i], int):
                        ret_dict[tags[i]] = int(values[i])
                    elif isinstance(values[i], list):
                        cl_list = [int(elem) for elem in values[i]]
                        ret_dict[tags[i]] = cl_list
                    else:
                        ret_dict[tags[i]] = str(values[i])
                else:
                    ret_dict[tags[i]] = padd
            else:
                return ret_dict
        else:
            logger.error(f"\n ERROR : There are not enough attributes to create .json file.\n #tags : {nt} & #attrs : {nv}")
            sys.exit(1)
