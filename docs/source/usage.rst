Usage
*****

.. _installation:

Installation
============

To use imgann, you could install using `PyPi <https://pypi.org/project/imgann/>`_ :

.. code-block:: console

   (.venv) $ pip install imgann

Another option is to directly build the library from codebase :

.. code-block:: console
   % clone codebase
   $ git clone https://github.com/nipdep/imgann.git
   % for usual usage
   $ pip install -e .
   % for development 
   $ pip install -e .[dev]



Functionalities
===============

Annotated Dataset Preview
--------------------------

It's import to make sure downloaded dataset image annotations are in proper / precise manner, And after all it's good to check the resulting annotations after custom annotation type conversion or 
annotation conversion provided by this library.

The following view function work in both *python* and *IPython* kernels. but ew encourage you to use in interactive python environment such as Jupyter notebooks.
Also, dataset and annotation file paths could be in either relative or absolute formats. This function generates set or pseudo random images with their
bounding + label on. Also, you could define resulting image shape and the seed to get consistent image outputs.

.. note::
   The `image-shape` does not change the aspect ratio of the images in the dataset at any point.
   More explicitly, For example let say the images shape of original dataset is (246, 246); means the aspect ration of 1:1.
   So, even you have input image_shape=(400, 500) the resulting image in the shape (400,400) to preserve original aspect ratio. 

.. autofunction:: imgann.show_samples

Code Example:

.. code-block:: python

   from imgann import Sample
   Sample.show_samples(data_path='../data/Hard Hat Sample.v5.voc/test', 
                       ann_path='../data/Hard Hat Sample.v5.voc/test', 
                       num_of_samples=5, 
                       ann_type='voc', 
                       seed=123, 
                       image_shape=[500, 500])

*Sample Output*

.. image:: ../static/show_sample1.png
   :width: 500


.. note::
   For further instruction follow to API page.

Convert Annotation Format
-------------------------

The library support converting between PascalVOC, COCO and CSV. In General, all the functions take parameter as image dataset directory and annotation file directory.

**COCO to PascalVOC**

.. note:: 
   the parameter 'center' defines the bounding box define formats;
   [X_center, Y_center, Width, Heigth] < if center=True 
   [X_min, Y_min, Width, Heigth] < if center=False. i.e. `roboflow <https://app.roboflow.com/>`_ annotated .json files saved in this format.

.. autofunction:: imgann.coco2voc

Code Example:

.. code-block:: python

   from imgann import Convertor
   Convertor.coco2voc(dataset_dir='../data/Hard Hat Sample.v5i.coco/test',
                      coco_ann_dir='../data/Hard Hat Sample.v5i.coco/test/_annotations.coco.json',
                      save_dir='../data/coco2voc)

