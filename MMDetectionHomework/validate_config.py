# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 22:28:44 2023

@author: wxr
"""

from mmdet.registry import DATASETS, VISUALIZERS
from mmengine.config import Config
from mmengine.registry import init_default_scope
import matplotlib.pyplot as plt
import os.path as osp

cfg = Config.fromfile('rtmdet_tiny_ballon.py')
init_default_scope(cfg.get('default_scope','mmdet'))
dataset = DATASETS.build(cfg.train_dataloader.dataset)
visualizer = VISUALIZERS.build(cfg.visualizer)
visualizer.dataset_meta = dataset.metainfo

plt.figure(figsize=(16,5))

for i in range(8):
    item = dataset[i]
    img = item['inputs'].permute(1,2,0).numpy()
    data_sample = item['data_samples'].numpy()
    gt_instances = data_sample.gt_instances
    img_path = osp.basename(item['data_samples'].img_path)
    
    gt_bboxes = gt_instances.get('bboxes',None)
    gt_instances.bboxes = gt_bboxes.tensor
    data_sample.gt_instances = gt_instances
    
    visualizer.add_datasample(
        osp.basename(img_path),
        img,
        data_sample,
        draw_pred=False,
        show=False)
    drawed_image = visualizer.get_image()
    
    plt.subplot(2,4,i+1)
    plt.imshow(drawed_image[...,[2,1,0]])
    plt.title(f"{osp.basename(img_path)}")
    plt.xticks([])
    plt.yticks([])

plt.tight_layout()