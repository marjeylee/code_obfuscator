import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt

import seaborn as sns

from llib.cv_utility.plot_utility.dsa import datadd

sns.set(color_codes=True)
# 从高斯分布随中，机产生100个样本数据
# 绘制直方图.kde即kernel density estimate，用于控制是否绘制核密度估计
a = datadd * 5
sns.lineplot(a, bins=100, kde=True)
plt.show()
