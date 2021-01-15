#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import unittest
from ImgAnn.operators.coco import COCO
from ImgAnn.operators.ImgData import ImgData
from unittest.mock import patch
import logging

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TestCOCO(unittest.TestCase):

    @mock.patch('os')
    def test_normalized2KITTI(self):

        # initialize ImgData object
        imgdata = ImgData.extract("any path")

        coco = COCO(imgdata.dataset)




