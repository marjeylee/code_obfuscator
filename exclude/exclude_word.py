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
EXCLUDE_WORD_SET = {'coding', '__init__', '__main__', '__name__', 'APP', 'relu', 'str', 'int', '__file__',
                    'path', 'forward', 'socket', 'lower', 'upper', 'and', 'dumps', 'started', 'with', 'open', 'now',
                    'size', 'shape', 'item', 'data', 'line', 'class', 're', 'range', 'uint8', 'int16', 'int32',
                    'time', 'run', 'files', 'uuid', 'float32', 'float64', 'join', 'realpath', 'copy', 'set', 'INFO',
                    'moves', 'xrange', 'dict', 'zip', 'set_verbosity', 'DEBUG', 'ERROR', 'move', 'imread', 'imwrite',
                    'makedirs', 'restore', 'keys', 'identity', 'setter', 'load', 'exp', 'concatenate', 'dot', 'extend',
                    'arcsin', 'sin', 'cos', 'shuffle'}
NET_EXCLUDE = {'layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'Session', 'slim', 'Counter', 'framework',
               'ResNet', 'SeparableConv2d', 'Block', 'conv1', 'bn1', 'bn2', 'DetectionNet', 'output', 'aspp1', 'out',
               'aspp2', 'embedding', 'gru', 'aspp3', 'conv2', 'attn_combine', 'attn', 'hidden_vector', 'layer',
               'LSTMAttentionOCR', 'aspp4', 'avg_pool', 'encoder', 'ASSP', 'decoder', 'Variable', 'concat', 'add',
               'conv2d', 'max_pool', 'squeeze', 'get_shape', 'batch_norm', 'dropout', 'stack', 'softmax',
               'per_process_gpu_memory_fraction'}
EXCLUDE_WORD_SET = EXCLUDE_WORD_SET.union(NET_EXCLUDE)
