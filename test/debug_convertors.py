#%%
from imgann import convert

cnv = convert.Convertor()

#%%
image_path = ''
coco_path = ''
csv_path = ''
voc_path = ''

#%%
# cnv.coco2csv('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data',
#              'F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\COCO\dataset.json',
#              '../data/data.csv')

# cnv.coco2voc('E:/JetBrain Project Files/Pycharm/security-point-object-detecton-Torch/data/data',
#              '../data/voc2coco.json',
#              '../data/voc', False)

cnv.csv2voc('../data/Hard Hat Sample.v5i.tensorflow/test/',
              '../data/Hard Hat Sample.v5i.tensorflow/test/_annotations.csv',
              '../data/csv2voc')

# cnv.csv2coco('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data',
#                '../data/data.csv',
#                '../data/csv2coco1.json')

# cnv.voc2coco('C:/Users/deela/Downloads/Hard Hat Sample.v5.voc/train',
#              'C:/Users/deela/Downloads/Hard Hat Sample.v5.voc/train_voc',
#              '../data/voc2cocohatt.json')

# cnv.voc2csv('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data',
#              '../data/voc',
#              '../data/voc2coco.csv')

# %%

# %%
