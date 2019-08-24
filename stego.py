# Your algorithm should take as input the bitmap (type N, S, P, or T),
# a positive int k,
# and the hidden text t.

# TODO:
# agregar al principio cuanto leer para poder decodificar
# ver encriptar el mensaje

import base64
import os
import bitarray
from PIL import Image, ImageFile

# Load truncated images too
ImageFile.LOAD_TRUNCATED_IMAGES = True


def set_pixel(old_color, bit_array, i, k):
    old_color = bin(old_color)
    old_bits = old_color[:-k]
    new_chunk = bit_array[i:i+k].copy()

    new_color = old_bits + ''.join(str(b) for b in new_chunk)
    return int(new_color, 2)


def message_decode(image, k):
    """ Decode a hidden message from the image.

    :arg1: TODO
    :returns: TODO

    """
    im = Image.open(image)

    extracted = ''

    pixels = im.load()

    for x in range(0, im.width):
        for y in range(0, im.height):
            r, g, b = pixels[x, y]

            # Store LSB of each color channel of each pixel
            extracted += bin(r)[-k:]
            extracted += bin(g)[-k:]
            extracted += bin(b)[-k:]

    chars = []
    for i in range(int(len(extracted) / 8)):
        byte = extracted[i*8: (i+1)*8]
        str_byte = ''.join([str(bit) for bit in byte])
        str_byte = ''.join(str_byte.replace('0b', 'b').split('b'))
        chars.append(chr(int(str_byte, 2)))

    # Don't forget that the message was base64-encoded
    flag = base64.b64decode(''.join(chars).encode('ascii', 'ignore'))
    return flag


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
    total_pixels = width * height
    pixels = im.load()

    if len(bit_array) <= total_pixels * 3:
        k = 1
    elif len(bit_array) <= total_pixels * 6:
        k = 2
    elif len(bit_array) <= total_pixels * 9:
        k = 3
    else:
        print("Message way too long for given image.")
        return 0
    print("mensaje:", len(bit_array))
    print("k:", k)
    print("total pixels:", total_pixels)

    # padding
    pad = len(bit_array) % k
    if pad != 0:
        bit_array = bit_array + list('0' * pad)

    i = 0
    for x in range(0, width):
        for y in range(0, height):
            if i >= len(bit_array):
                break

            red, green, blue = pixels[x, y]

            # Default values in case no bit has to be modified
            new_bit_red_pixel = red
            new_bit_green_pixel = green
            new_bit_blue_pixel = blue

            if i < len(bit_array):
                # Red pixel
                new_bit_red_pixel = set_pixel(red, bit_array, i, k)
                i += k

            if i < len(bit_array):
                # Green pixel
                new_bit_green_pixel = set_pixel(green, bit_array, i, k)
                i += k

            if i < len(bit_array):
                # Blue pixel
                new_bit_blue_pixel = set_pixel(blue, bit_array, i, k)
                i += k

            pixels[x, y] = (new_bit_red_pixel, new_bit_green_pixel,
                            new_bit_blue_pixel)
            # print("[+] \tAfter: (%d,%d,%d)" %
            # (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))

    im.save(stego_im)

    return k


def main():
    """ Main function """
    message = input("Enter SECRET message to hid in image:  ")
    filepath = input("Enter path to file:  ")

    k = message_encode(filepath, 2, message)
    print("jajajaj ahora DECODIFICQAMOS1!!!!!!11")
    msg = message_decode((os.path.splitext(filepath)[0] + "_lsb.png"), k)
    print(msg)


if __name__ == "__main__":
    main()
