import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_float
from skimage import measure
from textwrap import wrap

import stego


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


k = 3
msg = "uwu" * 100000
used_k = stego.message_encode('img/T1.png', k, msg)
decoded_msg = stego.message_decode('img/T1_lsb.png', used_k)

img = img_as_float(io.imread('img/T1.png'))
img_lsb = img_as_float(io.imread('img/T1_lsb.png'))

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                         sharex=True, sharey=True)
ax = axes.ravel()

label = 'Text to encode: {}\nDecoded text: {}'
label_lsb = 'MSE: {:.2f}, SSIM: {:.2f}, PSNR: {:.2f}, k: {}'

mse, ssim, psnr = image_measurements('img/T1.png', 'img/T1_lsb.png')

msg = '\n'.join(wrap(msg, 50))
if len(msg) > 100:
    msg = msg[:100]

decoded_msg = '\n'.join(wrap(decoded_msg, 50))
if len(decoded_msg) > 100:
    decoded_msg = decoded_msg[:100]

ax[0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=1)
ax[0].set_xlabel(label.format(msg, decoded_msg))
ax[0].set_title('Original image')

ax[1].imshow(img_lsb, cmap=plt.cm.gray, vmin=0, vmax=1)
ax[1].set_xlabel(label_lsb.format(mse, ssim, psnr, k))
ax[1].set_title('Stego image')

plt.tight_layout()
plt.show()
plt.savefig('test' + image_name + 'k:' + k + '.png')
