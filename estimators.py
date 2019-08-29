import os
from skimage import io
import numpy

from skimage import data, img_as_float, measure


def mse(x, y):
    return numpy.linalg.norm(x - y)


filename = 'wall.png'
filename_lsb = 'wall_lsb.png'

file1 = io.imread(filename)
file1_lsb = io.imread(filename_lsb)

mse1 = measure.compare_mse(file1, file1_lsb)
ssim1 = measure.compare_ssim(file1, file1_lsb,
                             data_range=file1.max() - file1.min(),
                             multichannel=True)
psnr1 = measure.compare_psnr(file1, file1_lsb,
                             data_range=file1.max()-file1.min())

print("mse:", mse1)
print("ssim1:", ssim1)
print("psnr:", psnr1)
