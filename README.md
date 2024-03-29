<h1 align='center'>
    <img src='/docs/static/logo.png' />
</h1>
<p align='center'>
    Python library for annotation file conversion and preview.
</p>

![Total Downloads](https://static.pepy.tech/personalized-badge/imgann?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads) &nbsp; &nbsp;
![Build Status](https://travis-ci.com/nipdep/img-ann.svg?branch=main) &nbsp; &nbsp;
![Version](https://img.shields.io/pypi/v/imgann) 

## Installation
1. From PiPy 
You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/imgann/):
```
$ pip install imgann
```
The package is support Python 3.7 and above.

2. From github
clone the codebase from GitHub
```
$ git clone https://github.com/nipdep/imgann.git
```
build the library
```
$ python setup.py bdist_wheel sdist
```
install built library
```
% for usual usage
$ pip install -e .
% for development 
$ pip install -e .[dev]
```

## Official Documentation
ReadTheDocs link : https://imgann.readthedocs.io/en/latest/index.html
 
## Usage

 For functional usages in detail refer the [documentation](https://imgann.readthedocs.io/en/latest/index.html)

 - To get N number of annotated images randomly.
    you can use coco format, pascalVOC format or csv format as annotation format.
    <annotation type> keywords can be from \['coco', 'csv', 'voc'] \
    `from imgann import Sample` \
    `Sample.show_samples( <image dataset dir> : string, <annotation file dit> : string, <number of images> : int, <annotation type> : string= 'coco', <center COCO> : bool= True )`
 
      _example :_ 
      ```
      Sample.show_samples('./data/test','./annotations/test',5,'voc')
      ```
    
 - To convert annotation file format.
    - coco to pascal VOC format converting\
    `from imgann import Convertor` \
    `Convertor.coco2voc( <image dataset dir> : string, <coco annotated .json file dir> : string, <voc formatted .xml file saving folder dir> : string, <center COCO> : bool= True)` \
 
        __note : if `<center COCO> = True` the generating bouding box format is [X_center, Y_center, Width, Heigth] \
                    `<center COCO> = False` then 'bbox' format of .json file is [X_min, Y_min, Width, Heigth]  < [roboflow](https://app.roboflow.com/) annotated .json files                         saved in this format.__
                   
        _example :_  
        ```                                                                                                                                             
        Convertor.coco2voc('../data/train', '../data/annotations/dataset.json', '../data/annotations/voc_dataset')
        ```                                                                                                                                              
    
    - coco to csv format converting\
    `from imgann import Convertor` \
    `Convertor.coco2csv( <image dataset dir> : string, <coco annotated .json file dir> : string, <voc formatted .csv file dir> : string, <center COCO> : bool= True)` 
         
        _example :_ 
        ```
        Convertor.coco2csv('../data/train', '../data/annotations/dataset.json', '../data/annotations/dataset.csv')
        ```
    
 
    - csv to coco format converting\
    `from imgann import Convertor` \
    `Convertor.coco2csv( <image dataset dir> : string, <csv annotated .csv file dir> : string, <coco formatted .json file dir> : string, <center COCO> : bool= True)` 

        _example :_ 
        ```
        Convertor.csv2coco('../data/train', '../data/annotations/dataset.csv', '../data/annotations/dataset.json')
        ```
         
    - csv to pascal VOC format converting\
    `from imgann import Convertor` \
    `Convertor.csv2voc( <image dataset dir> : string, <csv annotated .csv file dir> : string, <pascal VOC formatted .xml file saving folder dir> : string)` 

        _example :_ 
        ```
        Convertor.coco2csv('../data/train', '../data/annotations/dataset.csv', '../data/annotations/voc_dataset')
        ```
       
    - pascal VOC to coco format converting\
    `from imgann import Convertor` \
    `Convertor.voc2coco( <image dataset dir> : string, <pascal VOC annotated file included folder dir> : string, <coco formatted .json file dir> : string, <center COCO> : bool= True)`
    
        _example :_ 
        ```
        Convertor.voc2coco('../data/train', '../data/annotations/voc_dataset', '../data/annotations/dataset.json)
        ```
        
    - pascal VOC to csv format converting\
    `from imgann import Convertor` \
    `Convertor.voc2csv( <image dataset dir> : string, <pascal VOC annotated file included folder dir> : string, <csv formatted .csv file dir> : string)`
    
        _example :_ 
        ```
        Convertor.voc2coco('../data/train', '../data/annotations/voc_dataset', '../data/annotations/dataset.csv)
        ```
    
    - csv to TF multi-label converting\
    `from imgann import Convertor` \
    `Convertor.csv2multilabel( <csv dataset dir> : string, <save dir> : string)`
    
        _example :_ 
        ```
        Convertor.csv2multilabel('../data/train/annotation.csv', '../data/annotations/dataset.csv)
        ```

  - To get summary of image dataset\
  `from imgann import Sample`\
  `Sample.describe_data( <path to image dataset main folder> )`
  
      _example :_
      ```
      Sample.describe_data('../data/train')
      ```
   
  - To get summary of complete data annotation\
  `from imgann import Sample`\
  `Sample.describe_ann( <path to image dataset main folder> , <path to image annotation file/folder> , <image annotation type>['coco', 'yolo', 'csv', 'voc'], <center COCO> : bool= True)`
  
     _example :_
     ```
     Sample.describe_ann('../data/train', '../data/annotations/dataset.json', 'coco')
     ```
* * *
ImgAnn \
Copyright &copy; 2022 @nipdep
