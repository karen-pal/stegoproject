# Your algorithm should take as input the bitmap (type N, S, P, or T),
# a positive int k,
# and the hidden text t.

# TODO:
# agregar al principio cuanto leer para poder decodificar
# ver encriptar el mensaje
# parametro k del enunciado

import base64
import os
import bitarray
from PIL import Image


def set_pixel(old_color, bit_array, i):
    color_bit = bin(old_color)
    color_new_last_bit = bit_array[i]
    new_color = int(color_bit[:-1] + str(color_new_last_bit), 2)

    return new_color


def message_decode(image, k):
    """ Decode a hidden message from the image.

    :arg1: TODO
    :returns: TODO

    """
    im = Image.open(image)

    extracted = ''

    pixels = im.load()

    for x in range(0, im.width):
        r, g, b = pixels[x, 0]

        # Store LSB of each color channel of each pixel
        extracted += bin(r)[-1]
        extracted += bin(g)[-1]
        extracted += bin(b)[-1]

    chars = []
    for i in range(int(len(extracted) / 8)):
        byte = extracted[i*8: (i+1)*8]
        chars.append(
            chr(int(''.join([str(bit) for bit in byte]), 2)))

    # Don't forget that the message was base64-encoded
    flag = base64.b64decode(''.join(chars).encode('ascii', 'ignore'))
    print(flag)


def message_encode(image, k, hidden_text):
    """ Encode the given message in the image, up to k bits (?).

        image: string
        k: positive int
        hidden_text: string
    """
    encoded_message = base64.b64encode(hidden_text.encode('ascii'))

    # Converts the message into an array of bits
    ba = bitarray.bitarray()
    ba.frombytes(encoded_message)
    bit_array = [int(i) for i in ba]

    try:
        im = Image.open(image)
        stego_im = (os.path.splitext(image)[0] + "_lsb.png")
        im.save(stego_im)
    except (OSError, IOError) as e:
        print("Non existent file")
        print(e)
        return

    im = Image.open(stego_im)
    width, height = im.size
    pixels = im.load()

    i = 0
    for x in range(0, width):
        red, green, blue = pixels[x, 0]

        print("[+] Pixel : [%d,%d]" % (x, 0))
        print("[+] \tBefore : (%d,%d,%d)" % (red, green, blue))

        # Default values in case no bit has to be modified
        new_bit_red_pixel = red
        new_bit_green_pixel = green
        new_bit_blue_pixel = blue

        if i < len(bit_array):
            # Red pixel
            new_bit_red_pixel = set_pixel(red, bit_array, i)
            i += 1

        if i < len(bit_array):
            # Green pixel
            new_bit_green_pixel = set_pixel(green, bit_array, i)
            i += 1

        if i < len(bit_array):
            # Blue pixel
            new_bit_blue_pixel = set_pixel(blue, bit_array, i)
            i += 1

        pixels[x, 0] = (new_bit_red_pixel, new_bit_green_pixel,
                        new_bit_blue_pixel)
        print("[+] \tAfter: (%d,%d,%d)" %
              (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))

    im.save(stego_im)


def main():
    """ Main function """
    message = input("Enter SECRET message to hid in image:  ")
    filepath = input("Enter path to file:  ")

    message_encode(filepath, 666, message)
    print("jajajaj ahora DECODIFICQAMOS1!!!!!!11")
    message_decode((os.path.splitext(filepath)[0] + "_lsb.png"), 666)


if __name__ == "__main__":
    main()
