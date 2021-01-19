![Build Status](https://travis-ci.com/nipdep/img-ann.svg?branch=main)\
![Version](https://img.shields.io/pypi/v/imgann)

# img-ann

The __imgann__ is a package for a simplify operations in image annotated files.
such as, annotation type converting \[coco format, pascalVOC format, csv format], image dataset sampling], etc.


## Installation
You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/imgann/):

$`pip install imgann`

The package is support Python 3.6 and above.
 
## Usage

 
 - To get N number of annotated images randomly.
    you can use coco format, pascalVOC format or csv format as annotation format.
    <annotation type> keywords can be from \['coco', 'csv', 'voc'] \
    `from imgann import Sample` \
    `Sample.show_samples( <image dataset dir> : string, <annotation file dit> : string, <number of images> : int, <annotation type> : string= 'coco' )` 
 
        _example :_ \
        `Sample.show_samples('./data/test','./annotations/test',5,'voc')` 

 - To convert annotation file format.
    - coco to pascal VOC format converting
    ```
    `from imgann import Convertor` \
    `Convertor.coco2voc( <image dataset dir> : string, <coco annotated .json file dir> : string, <voc formatted .xml file saving folder dir> : string)` 
    
        _example :_ \
        `Convertor.coco2voc('../data/train', '../data/annotations/dataset.json', '../data/annotations/voc_dataset')`
    ```
    - coco to csv format converting
    ```
    `from imgann import Convertor` \
    `Convertor.coco2csv( <image dataset dir> : string, <coco annotated .json file dir> : string, <voc formatted .csv file dir> : string)` 
     
        _example :_ \
        `Convertor.coco2csv('../data/train', '../data/annotations/dataset.json', '../data/annotations/dataset.csv')`
    
    ```
    - csv to coco format converting
    ```
    `from imgann import Convertor` \
    `Convertor.coco2csv( <image dataset dir> : string, <csv annotated .csv file dir> : string, <coco formatted .json file dir> : string)` 

        _example :_ \
        `Convertor.csv2coco('../data/train', '../data/annotations/dataset.csv', '../data/annotations/dataset.json')` 
    ```     
    - csv to pascal VOC format converting
    ```
    `from imgann import Convertor` \
    `Convertor.csv2voc( <image dataset dir> : string, <csv annotated .csv file dir> : string, <pascal VOC formatted .xml file saving folder dir> : string)` 

        _example :_ \
        `Convertor.coco2csv('../data/train', '../data/annotations/dataset.csv', '../data/annotations/voc_dataset')` 
    ```   
    - pascal VOC to coco format converting
    ```
    `from imgann import Convertor` \
    `Convertor.voc2coc( <image dataset dir> : string, <pascal VOC annotated file included folder dir> : string, <coco formatted .json file dir> : string)`
    
        _example :_ \
        `Convertor.voc2coco('../data/train', '../data/annotations/voc_dataset', '../data/annotations/dataset.json)`
     ```   
     - pascal VOC to csv format converting
     ```
    `from imgann import Convertor` \
    `Convertor.voc2csv( <image dataset dir> : string, <pascal VOC annotated file included folder dir> : string, <csv formatted .csv file dir> : string)`
    
        _example :_ \
        `Convertor.voc2coco('../data/train', '../data/annotations/voc_dataset', '../data/annotations/dataset.csv)`
     ```
### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
