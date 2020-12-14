# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： exclude_word
Description :
Author : 'li'
date： 2020/12/11
-------------------------------------------------
Change Activity:
2020/12/11:
-------------------------------------------------
"""
EXCLUDE_WORD_SET = {'coding', '__init__', '__main__', 'APP', 'relu',
                    'path', 'forward', 'size', 'shape', 'item', 'data', 'line', 'time', 'run', 'files'}
NET_EXCLUDE = {'layer0', 'layer1', 'layer2', 'layer3', 'layer4',
               'ResNet', 'SeparableConv2d', 'Block', 'conv1', 'bn1', 'bn2', 'DetectionNet', 'output', 'aspp1', 'out',
               'aspp2', 'embedding', 'gru', 'aspp3', 'conv2', 'attn_combine', 'attn', 'hidden_vector', 'layer',
               'LSTMAttentionOCR', 'aspp4', 'avg_pool', 'encoder', 'ASSP', 'decoder'}
EXCLUDE_WORD_SET = EXCLUDE_WORD_SET.union(NET_EXCLUDE)
