# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： statistic
Description :
Author : 'li'
date： 2020/6/5
-------------------------------------------------
Change Activity:
2020/6/5:
-------------------------------------------------
"""


def statistic_torch_model_parameter_size(net):
    """

    :param net:
    :return:
    """
    total_num = sum(p.numel() for p in net.parameters())
    trainable_num = sum(p.numel() for p in net.parameters() if p.requires_grad)
    return {'Total': total_num, 'Trainable': trainable_num}
