![Build Status](https://travis-ci.com/nipdep/img-ann.svg?branch=main)\
![Version](https://img.shields.io/pypi/v/imgann)

# img-ann

The imgann is a package for a simplify operations in image annotated files.
such as, annotation type converting \[coco format, pascalVOC format, csv format], image dataset sampling], etc.


## Installation
You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/imgann/):

$`pip install imgann`

The package is support Python 3.6 and above.
 
## Usage

 
 - To get N number of annotated images randomly.
    you can use coco format, pascalVOC format or csv format as annotation format.
    <annotation type> keywords can be from \['coco', 'csv', 'voc'] \
    `from imgann import Sample`\
    `Sample.show_samples( <image dataset dir> : string, <annotation file dit> : string, <number of images> : int, <annotation type> : string= 'coco' )`
 
      _example :_ \
      `Sample.show_samples('./data/test','./annotations/test',5,'voc')` 
    
 - To convert annotation file format.
    - coco to pascal VOC format converting
    `from imgann import Convertor` \
    `Convertor.coco2voc( <image dataset dir> : string, <coco annotated .json file dir> : string, <voc formatted .xml file saving folder dir> : string)` 
    
        _example :_ \
        `Convertor.coco2voc('../data/train', '../data/annotations/dataset.json', '../data/annotations/voc_dataset')`
    
    - coco to csv format converting
    `from imgann import Convertor` \
    `Convertor.coco2csv( <image dataset dir> : string, <coco annotated .json file dir> : string, <voc formatted .csv file dir> : string)` 
     
        _example :_ \
        `Convertor.coco2csv('../data/train', '../data/annotations/dataset.json', '../data/annotations/dataset.csv')`
    
 
    - csv to coco format converting
    `from imgann import Convertor` \
    `Convertor.coco2csv( <image dataset dir> : string, <csv annotated .csv file dir> : string, <coco formatted .json file dir> : string)` 

        _example :_ \
        `Convertor.csv2coco('../data/train', '../data/annotations/dataset.csv', '../data/annotations/dataset.json')` 
         
    - csv to pascal VOC format converting
    `from imgann import Convertor` \
    `Convertor.csv2voc( <image dataset dir> : string, <csv annotated .csv file dir> : string, <pascal VOC formatted .xml file saving folder dir> : string)` 

        _example :_ \
        `Convertor.coco2csv('../data/train', '../data/annotations/dataset.csv', '../data/annotations/voc_dataset')` 
       
    - pascal VOC to coco format converting
    `from imgann import Convertor` \
    `Convertor.voc2coc( <image dataset dir> : string, <pascal VOC annotated file included folder dir> : string, <coco formatted .json file dir> : string)`
    
        _example :_ \
        `Convertor.voc2coco('../data/train', '../data/annotations/voc_dataset', '../data/annotations/dataset.json)`
        
     - pascal VOC to csv format converting
    `from imgann import Convertor` \
    `Convertor.voc2csv( <image dataset dir> : string, <pascal VOC annotated file included folder dir> : string, <csv formatted .csv file dir> : string)`
    
        _example :_ \
        `Convertor.voc2coco('../data/train', '../data/annotations/voc_dataset', '../data/annotations/dataset.csv)`
    
    
  - To get summary of image dataset\
  `from imgann import Sample`\
  `Sample.describe_data( <path to image dataset main folder> )`
  
      _example :_\
      `Sample.describe_data('../data/train')`
   
  - To get summary of complete data annotation\
  `from imgann import Sample`\
  `Sample.describe_ann( <path to image dataset main folder> , <path to image annotation file/folder> , <image annotation type>['coco', 'yolo', 'csv', 'voc'] )`
  
     _example :_\
     `Sample.describe_ann('../data/train', '../data/annotations/dataset.json', 'coco')`
