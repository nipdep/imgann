API
***

ImgAnn.Sample
=============

.. data:: show_samples

**Function Description**

show set of random images from the dataset with annotations.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - data_path
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - ann_path
     - relative path current folder, or absolute path to the main folder of the annotated file
     - None
   * - num_of_samples
     - 5
     - number of sample images to view in integer format
   * - ann_type
     - 'coco'
     - annotation type of the file that given in the 'ann_path'. supported names : ['coco', 'voc', 'csv']
   * - center
     - True
     - Only applicable in 'coco' annotation format. define in following note.
   * - image_shape
     - [300, 300]
     - image size in pixels for resulting images.
   * - seed
     - 0
     - if seed=0; resulting images will be always random. if seed>0, the resulting images will be same at each execution.

.. note:: 

   | the parameter 'center' defines the bounding box define formats;
   | [X_center, Y_center, Width, Heigth] < if center=True 
   | [X_min, Y_min, Width, Heigth] < if center=False. i.e. `roboflow <https://app.roboflow.com/>`_ annotated .json files saved in this format.

.. data:: describe_data

**Function Description**

show the summary of image dataset.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - data_path
     - None
     - absolute or relative path to image dataset directory. effect of directory illustrated in the :doc:`usage` section

.. data:: describe_ann

**Function Description**

show the summary of image dataset with annotations.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - data_path
     - None
     - absolute or relative path to image dataset main folder
   * - ann_path
     - None
     - absolute or relative path to image annotation file or folder
   * - ann_type
     - 'coco'
     - annotation format [coco, voc, csv, yolo]
   * - center
     - True
     - Only applicable in 'coco' annotation format

ImgAnn.Convertor
================

.. data:: coco2csv

.. data:: coco2voc

.. data:: voc2coco

.. data:: voc2csv

.. data:: csv2coco

.. data:: csv2voc

.. data:: csv2multilabel

Supporting Annotation File Examples
-----------------------------------

.. data:: COCO

.. data:: PascalVOC

.. data:: CSV (Object Detection)

.. data:: CSV (Multi-label)
