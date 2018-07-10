# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2017-09-06 17:47:51
# @Last Modified by:   Alan Lau
# @Last Modified time: 2017-09-06 17:47:51


from canopy import Canopy
import numpy as np


dataset = np.random.rand(500, 2)
gc = Canopy(dataset)
gc.setThreshold(0.6, 0.4)
canopies = gc.clustering()
print(len(canopies))
