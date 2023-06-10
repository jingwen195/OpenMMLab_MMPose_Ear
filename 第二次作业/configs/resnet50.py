model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='ResNet',
        depth=50,  #
        num_stages=4,
        out_indices=(3, ),
        style='pytorch'),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        num_classes=30,  # 这里是后添加的：分类数目修改为2，猫和狗
        in_channels=2048, # resnet是2048，resnet是512
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=1,
    ),
    init_cfg=dict(type='Pretrained', checkpoint='F:/Code_ZJW/MMPretrain_zjw/mmpretrain/checkpoint/resnet50_8xb32_in1k_20210831-ea4938fc.pth')  # 这里是后添加的：加载预训练模型
    )#https://download.openmmlab.com/mmclassification/v0/resnet/resnet50_8xb32_in1k_20210831-ea4938fc.pth
# dataset settings
dataset_type = 'CustomDataset'  # 这里是后添加的：数据集类型修改为MMPretrain中提供的自定义数据类型
data_preprocessor = dict(
    num_classes=30,  # 这里是后添加的：分类数目修改为30
    # RGB format normalization parameters
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    # convert image from BGR to RGB
    to_rgb=True,
)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', scale=224),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='PackInputs'),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]

train_dataloader = dict(
    batch_size=2,
    num_workers=5,
    dataset=dict(
        type=dataset_type,
        data_root='F:/Code_ZJW/MMPretrain_zjw/mmpretrain/data/train',  # 这里是后添加的：修改数据集路径
        # ann_file='meta/train.txt',  # 这里是后添加的：删除无关参数
        # data_prefix='train',
        pipeline=train_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=True),
)

val_dataloader = dict(
    batch_size=2,
    num_workers=5,
    dataset=dict(
        type=dataset_type,
        data_root='F:/Code_ZJW/MMPretrain_zjw/mmpretrain/data/test',
        pipeline=test_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=False),
)
val_evaluator = dict(type='Accuracy', topk=1)  # 这里是后添加的：修改评估指标tok为1
# If you want standard test, please manually configure the test dataset
test_dataloader = val_dataloader
test_evaluator = val_evaluator

# optimizer
optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001))  # 这里是后添加的：修改学习率为0.01

# learning policy
param_scheduler = dict(
    type='MultiStepLR', by_epoch=True, milestones=[30, 60, 90], gamma=0.1)

# train, val, test setting
train_cfg = dict(by_epoch=True, max_epochs=5, val_interval=1)  # 这里是后添加的：修改训练轮数为5
val_cfg = dict()
test_cfg = dict()


# defaults to use registries in mmpretrain
default_scope = 'mmpretrain'

# configure default hooks
default_hooks = dict(
    # record the time of every iteration.
    timer=dict(type='IterTimerHook'),

    # print log every 100 iterations.
    logger=dict(type='LoggerHook', interval=100),

    # enable the parameter scheduler.
    param_scheduler=dict(type='ParamSchedulerHook'),

    # save checkpoint per epoch.
    checkpoint=dict(type='CheckpointHook', interval=1),

    # set sampler seed in distributed evrionment.
    sampler_seed=dict(type='DistSamplerSeedHook'),

    # validation results visualization, set True to enable it.
    visualization=dict(type='VisualizationHook', enable=False),
)

# configure environment
env_cfg = dict(
    # whether to enable cudnn benchmark
    cudnn_benchmark=False,

    # set multi process parameters
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),

    # set distributed parameters
    dist_cfg=dict(backend='nccl'),
)

# set visualizer
vis_backends = [dict(type='LocalVisBackend')]
visualizer = dict(type='UniversalVisualizer', vis_backends=vis_backends)

# set log level
log_level = 'INFO'

# load from which checkpoint
load_from = None

# whether to resume training from the loaded checkpoint
resume = False

# Defaults to use random seed and disable `deterministic`
randomness = dict(seed=None, deterministic=False)