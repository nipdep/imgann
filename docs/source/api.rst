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
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file
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

**Function Description**

convert COCO annotation into CSV.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - dataset_dir
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - coco_ann_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations.json'
   * - save_dir
     - None
     - annotation file saving location. Ex. '../data/annotations.csv'
   * - center
     - True
     - defined in the above 'Note'
   * - is_multilabel
     - False
     - if 'True' output will be in `CSV (Multi-label)` format, else in `CSV (Object Detection)` format

.. data:: coco2voc

**Function Description**

convert COCO annotation into PascalVOC.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - dataset_dir
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - coco_ann_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations.json'
   * - save_dir
     - None
     - annotation file saving location. Ex. '../data/annotations/'
   * - center
     - True
     - defined in the above 'Note'

.. data:: voc2coco

**Function Description**

convert PascalVOC annotation into COCO.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - dataset_dir
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - coco_ann_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations/'
   * - save_dir
     - None
     - annotation file saving location. Ex. '../data/annotations.json'
   * - center
     - True
     - defined in the above 'Note'

.. data:: voc2csv

**Function Description**

convert PascalVOC annotation into CSV.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - dataset_dir
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - coco_ann_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations/'
   * - save_dir
     - None
     - annotation file saving location. Ex. '../data/annotations.csv'
   * - is_multilabel
     - False
     - if 'True' output will be in `CSV (Multi-label)` format, else in `CSV (Object Detection)` format


.. data:: csv2coco

**Function Description**

convert CSV annotation into COCO.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - dataset_dir
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - coco_ann_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations.csv'
   * - save_dir
     - None
     - annotation file saving location. Ex. '../data/annotations.json'
   * - center
     - True
     - defined in the above 'Note'

.. data:: csv2voc

**Function Description**

convert CSV annotation into PascalVOC.

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - dataset_dir
     - None
     - relative path current folder, or absolute path to the main folder of the image dataset
   * - coco_ann_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations.csv'
   * - save_dir
     - None
     - annotation file saving location. Ex. '../data/annotations/'

.. data:: csv2multilabel

**Function Description**

convert CSV (Object Detection)annotation into CSV (Multi-label).

.. list-table:: Parameter Description
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - csv_dir
     - None
     - relative path current folder, or absolute path to the main folder of the annotated file. Ex. '..data/annotations.csv'
   * - save_dir
     - None
     - annotation file saving location. Ex. '..data/annotations_m.csv'



Supporting Annotation File Examples
===================================

.. data:: COCO

.. code-block:: JSON

   {
      "annotations": [
         {
               "id": "1",
               "image_id": "1",
               "category_id": 1,
               "area": 22165,
               "bbox": [170, 114, 313, 269],
               "ignore": "0",
               "iscrowd": "0"
         },
         .
         .
         ],
      "images": [
         {
               "file_name": "1.jpg",
               "height": 413,
               "width": 413,
               "id": "1"
         },
         .
         .
         ],
      "categories": [
         {
               "id": 1,
               "name": 1,
               "supercategory": "none"
         },
         .
         ],
   }

.. data:: PascalVOC

.. code-block:: XML

   <annotation>
      <folder></folder>
      <filename>000008_jpg.rf.d00174cb69229a352e8677a640ec2d86.jpg</filename>
      <path>000008_jpg.rf.d00174cb69229a352e8677a640ec2d86.jpg</path>
      <source>
         <database>roboflow.ai</database>
      </source>
      <size>
         <width>416</width>
         <height>416</height>
         <depth>3</depth>
      </size>
      <segmented>0</segmented>
      <object>
         <name>helmet</name>
         <pose>Unspecified</pose>
         <truncated>0</truncated>
         <difficult>0</difficult>
         <occluded>0</occluded>
         <bndbox>
            <xmin>201</xmin>
            <xmax>241</xmax>
            <ymin>115</ymin>
            <ymax>142</ymax>
         </bndbox>
      </object>
      <object>
         <name>head</name>
         <pose>Unspecified</pose>
         <truncated>0</truncated>
         <difficult>0</difficult>
         <occluded>0</occluded>
         <bndbox>
            <xmin>128</xmin>
            <xmax>164</xmax>
            <ymin>151</ymin>
            <ymax>180</ymax>
         </bndbox>
      </object>
   </annotation>

.. data:: CSV (Object Detection)

.. list-table:: train.csv
   :widths: 25 25 25 25 25 25 25 25
   :header-rows: 1

   * - filename
     - width
     - height
     - class
     - xmin
     - ymin
     - xmax
     - ymax
   * - 1.png
     - 416
     - 416
     - helmet
     - 234
     - 136
     - 265
     - 197
   * - 1.png
     - 416
     - 416
     - head
     - 109
     - 135
     - 145
     - 164

.. data:: CSV (Multi-label)

**Description** : one-hot encoded format of the all the classes presents in the annotation

.. list-table:: train.csv
   :widths: 25 25 25
   :header-rows: 1

   * - filename
     - head
     - helmet
   * - 1.png
     - 1
     - 0
   * - 2.png
     - 0
     - 1
