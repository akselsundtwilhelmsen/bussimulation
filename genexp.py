import numpy as np
import matplotlib.pyplot as plt
import random

lambda_param = 0.5

def neg_exp_inv(U):
    return -np.log(1-U)/lambda_param

def gen_samplesX(scale, size):
    U = np.random.rand(1000)
    return neg_exp_inv(U)

samplesX = gen_samplesX(scale=1/lambda_param, size=1000)
samplesX.sort()
samplesY = np.random.exponential(scale=1/lambda_param, size=1000)
samplesY.sort()

plt.figure(figsize=(6, 4))
plt.plot(samplesX, samplesY)
plt.xlabel('Xi')
plt.ylabel('Yi')
plt.savefig('XY.png', dpi=300, bbox_inches='tight')
plt.show()
