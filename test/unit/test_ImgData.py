import unittest
from unittest.mock import Mock
from unittest.mock import patch, sentinel
import pathlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from ImgAnn.operators.imgdata import ImgData


class TestImgData(unittest.TestCase):

    def setUp(self):
        self.here = str(pathlib.Path(__file__).parent.parent.parent.resolve())

    @patch('ImgAnn.operators.imgdata.os')
    def test_ext_folders(self, mock_os):

        with patch('ImgAnn.operators.imgdata.os.walk') as mock_walk_1:
            mock_os.path.exists.return_value = True
            mock_walk_1.return_value = [
                ('./a/s/', ['d', 'e', 't'], ()),
                ('./a/s/d/', [], []),
                ('./a/s/e/', [], []),
                ('./a/s/t/', [], [])
            ]
            assert ImgData.ext_folders(sentinel.path) == ['d', 'e', 't']

        with patch('ImgAnn.operators.imgdata.os.walk') as mock_walk_2:
            path_val = Mock('./a/s')
            path_val.exists.return_value = True
            mock_walk_2.return_value = [
                ('./a/s/', [], ['re','ts'])]
            assert ImgData.ext_folders(path_val) == ['s']

    def test_ext_files(self):
        self.assertEqual(['log_coco.txt', 'log_ImgData.txt'], ImgData.ext_files(self.here + '/logs/ImgAnn/operators'))
        self.assertEqual('log_coco.txt', ImgData.ext_files(self.here + '/logs/ImgAnn/operators/log_coco.txt'))


if __name__ == "__main__":
    unittest.main()
