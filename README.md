Assignment E.318-C: LSB Steganography
======
###### ECI-33 - Karen Araceli Palacio Pastor, Lucas Leonardo Ciancaglini

This respository consists of the implementation of a coding and decoding
steganographic algorithm using the Least Significant Bit (LSB) method. It
has been implemented in Python 3, and it consists of two files: `stego.py`,
which includes the functions `message_encode` and `message_decode`,
and `estimators.py`, which contains the functions necessary to calculate
the MSE, SSIM, and PSNR measurements, as well as the performance of the
encoding and decoding algorithm. It also generates the plots shown in the
report.

The `stego_test.py` file is for internal testing purposes.

`img` contains both the cover images used, and generated graphs. `fail`
includes the corner cases in which the algorithm doesn't properly
decode the steganographic message.

## Installation
The dependencies can be installed with `pip` or `pip3` in case Python 2
is the default in your system:

```console
$ pip install --user Pillow bitarray numpy matplotlib scikit-image
```

## Usage
`stego.py` is meant to be used as a module, but it can be called directly
in order to manually test the algorithms with k = 1, for example:

```console
$ python3 stego.py
Enter SECRET message to hid in image:  secret message
Enter path to file:  img/N1.png
Encoding message secret message with k = 1...
Decoding message...
Decoded message: secret message
```

Run `estimators.py` in order to generate the graphs shown in the report.
