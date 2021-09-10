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
                    'path', 'forward', 'socket', 'count', 'norm', 'lower', 'upper', 'and', 'dumps', 'started', 'with',
                    'open', 'cv2', 'pool', 'yaml', 'DataLoader', 'dataloader', 'cuda', 'Focus', 'SiLU', 'print', 'Conv',
                    'now', 'C3', 'SPP', 'Concat', 'Detect', 'log', 'forward', 'aspp2', 'corner', 'canvas',
                    'size', 'shape', 'item', 'data', 'line', 'aspp3', 'update', 'cpu', 'array',
                    'class', 're', 'range',
                    'uint8', 'int16', 'int32',
                    'time', 'run', 'files', 'uuid', 'float32', 'float64', 'join', 'realpath', 'copy', 'set', 'INFO',
                    'moves', 'xrange', 'dict', 'zip', 'set_verbosity', 'DEBUG', 'ERROR', 'move', 'imread', 'imwrite',
                    'makedirs', 'restore', 'keys', 'identity', 'setter', 'load', 'exp', 'concatenate', 'dot', 'extend',
                    'arcsin', 'sin', 'cos', 'shuffle', 'request', 'argv', 'close', 'exists', 'cluster', 'graph', 'i',
                    'N1', 'form', 'asarray', 'cast', 'type', 'resize', 'blur', 'filter2D', 'decay', 'normalize', 'size',
                    'move', 'angle', 'self', 'flip', 'long'}

NET_EXCLUDE = {'layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'Session', 'slim', 'Counter', 'framework', 'scopes',
               'ResNet', 'SeparableConv2d', 'Block', 'conv1', 'bn1', 'bn2', 'DetectionNet', 'output', 'aspp1', 'out',
               'aspp2', 'embedding', 'gru', 'aspp3', 'conv2', 'attn_combine', 'attn', 'hidden_vector', 'layer',
               'LSTMAttentionOCR', 'aspp4', 'avg_pool', 'encoder', 'ASSP', 'decoder', 'Variable', 'concat', 'add',
               'conv2d', 'max_pool', 'squeeze', 'get_shape', 'batch_norm', 'dropout', 'stack', 'softmax', 'sigmoid',
               'per_process_gpu_memory_fraction'}
EXCLUDE_WORD_SET = EXCLUDE_WORD_SET.union(NET_EXCLUDE)
