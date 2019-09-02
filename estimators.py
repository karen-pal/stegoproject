import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_float
from skimage import measure
from textwrap import wrap
import os
import time
import sys

import stego

SUCCESSFUL_DECODES = 0
MSE = []
SSIM = []
PSNR = []


def image_measurements(img, img_lsb):
    file = io.imread(img)
    file_lsb = io.imread(img_lsb)

    mse = measure.compare_mse(file, file_lsb)
    ssim = measure.compare_ssim(file, file_lsb,
                                data_range=file.max() - file.min(),
                                multichannel=True)
    psnr = measure.compare_psnr(file, file_lsb,
                                data_range=file.max()-file.min())
    return (mse, ssim, psnr)


def image_analysis_graph(img_name, k, msg):
    global SUCCESSFUL_DECODES

    img_lsb_name = stego.lsb_pic(img_name)

    encode_time = time.clock()
    used_k = stego.message_encode(img_name, k, msg)
    encode_time = time.clock() - encode_time

    decode_time = time.clock()
    decoded_msg = stego.message_decode(img_lsb_name, used_k)
    decode_time = time.clock() - decode_time

    if decoded_msg == msg:
        SUCCESSFUL_DECODES += 1

    img = img_as_float(io.imread(img_name))
    img_lsb = img_as_float(io.imread(img_lsb_name))

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6),
                             sharex=True, sharey=True)
    ax = axes.ravel()

    label = 'Text to encode: {}\nDecoded text: {}'
    label_lsb = 'MSE: {:.2f}, SSIM: {:.2f}, PSNR: {:.2f}\nk: {}, Encoding time: {:.2f}, Decoding time: {:.2f}'

    mse, ssim, psnr = image_measurements(img_name, img_lsb_name)
    global MSE, SSIM, PSNR
    MSE.append(mse)
    SSIM.append(ssim)
    PSNR.append(psnr)

    msg = '\n'.join(wrap(msg, 50))
    if len(msg) > 100:
        msg = msg[:100] + "[...]"

    decoded_msg = '\n'.join(wrap(decoded_msg, 50))
    if len(decoded_msg) > 100:
        decoded_msg = decoded_msg[:100] + "[...]"

    ax[0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=1)
    ax[0].set_xlabel(label.format(msg, decoded_msg))
    ax[0].set_title('Original image')

    ax[0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=1)
    ax[0].set_xlabel(label.format(msg, decoded_msg))
    ax[0].set_title('Original image')

    ax[1].imshow(img_lsb, cmap=plt.cm.gray, vmin=0, vmax=1)
    ax[1].set_xlabel(label_lsb.format(
        mse, ssim, psnr, k, encode_time, decode_time))
    ax[1].set_title('Stego image')

    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.splitext(img_name)[0]
                + "_" + msg + '_k' + str(k) + '.png')
    plt.close("all")


PICS = [
    'img/N1.png',
    'img/N2.png',
    'img/N3.png',
    'img/N4.png',
    'img/P1.jpg',
    'img/P2.jpg',
    'img/P3.jpg',
    'img/P4.png',
    'img/S1.jpg',
    'img/S2.png',
    'img/T1.png',
    'img/T2.png',
    'img/T3.png',
    'img/T4.png',
]

i = 0
for img in PICS:
    for k in range(1, 4):
        image_analysis_graph(img, k, "a")
        i += 1
        image_analysis_graph(img, k, "Paris")
        i += 1
        image_analysis_graph(img, k, "steganography is cool and fun")
        i += 1
        image_analysis_graph(img, k, "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." * 100)
        i += 1

print("Successfully decoded", SUCCESSFUL_DECODES, "out of", i, "images")
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4),
                         sharex=True, sharey=False)
axes[0].set_title("Median Square Error")
axes[0].set_ylabel("MSE values")
axes[0].scatter([x for x in range(0, i)], MSE)

axes[1].set_title("Structural Similarity Index")
axes[1].set_ylabel("SSIM values")
axes[1].scatter([x for x in range(0, i)], SSIM)

axes[2].set_title("Peak Signal-to-Noise Ratio")
axes[2].set_ylabel("PSNR values")
axes[2].scatter([x for x in range(0, i)], PSNR)

plt.tight_layout()
plt.savefig("measures.png")
plt.close('all')
