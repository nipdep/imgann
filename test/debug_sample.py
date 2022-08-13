#%%
from imgann import Sample
#%%
Sample.show_samples('../data/Hard Hat Sample.v5i.coco/test', '../data/Hard Hat Sample.v5i.coco/test/_annotations.coco.json', 5, 'coco', image_shape=[300, 300], center=False)

# Sample.describe_ann('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data',
#                     'F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\COCO\dataset.json')

# Sample.describe_data('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data')
#%%
Sample.show_samples('../data/Hard Hat Sample.v5i.tensorflow/test', '../data/Hard Hat Sample.v5i.tensorflow/test/_annotations.csv', 5, 'csv', image_shape=[500, 600])
# %%

# %%
