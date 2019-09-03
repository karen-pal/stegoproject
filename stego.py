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

    :image: string
    :k: int

    """
    im = Image.open(image)
    pixels = im.load()

    # Extract length of message
    msg_len = ""

    for x in range(0, 12):
        red, green, blue = pixels[x, 0]

        msg_len += bin(red)[-1]
        msg_len += bin(green)[-1]

        if x == 11:
            break

        msg_len += bin(blue)[-1]

    msg_len = int(msg_len, 2)

    # Extract the message
    extracted = ''

    i = 0
    for x in range(12, im.width):
        for y in range(0, im.height):
            if i == msg_len:
                break

            red, green, blue = pixels[x, y]

            # Store LSB of each color channel of each pixel
            extracted += bin(red)[-k:]
            extracted += bin(green)[-k:]
            extracted += bin(blue)[-k:]

            i += 1

    chars = []
    for i in range(int(len(extracted) / 8)):
        byte = extracted[i*8: (i+1)*8]
        str_byte = ''.join([str(bit) for bit in byte])
        str_byte = ''.join(str_byte.replace('0b', 'b').split('b'))
        chars.append(chr(int(str_byte, 2)))

    msg = ''.join(chars).encode('ascii', 'ignore')

    # Don't forget that the message was base64-encoded
    decoded_msg = base64.b64decode(msg)

    return decoded_msg.decode('ascii', 'ignore')


def message_encode(image, max_k, hidden_text):
    """ Encode the given message in the image, up to max_k bits per channel.

        image: string
        max_k: positive int
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

    msg_len = bin(len(bit_array)).replace("0b", "")

    # Padding to fit into 32 bits
    msg_len = "0" * (32 - len(msg_len)) + msg_len
    msg_len_ba = bitarray.bitarray()
    msg_len_ba.frombytes(msg_len.encode())
    msg_len_ba = [int(i) for i in msg_len_ba]

    # Encode message length into the first 11 pixels
    i = 0
    for x in range(0, 12):
        red, green, blue = pixels[x, 0]

        new_red = set_pixel(red, msg_len_ba, i, 1)
        i += 1

        new_green = set_pixel(green, msg_len_ba, i, 1)
        i += 1

        if x == 11 or i == 32:
            break

        new_blue = set_pixel(blue, msg_len_ba, i, 1)
        i += 1

        pixels[x, 0] = (new_red, new_green, new_blue)

    # Calculate a proper k value
    if len(bit_array) <= total_pixels * 3:
        k = 1
    elif len(bit_array) <= total_pixels * 6:
        k = 2
    elif len(bit_array) <= total_pixels * 9:
        k = 3
    else:
        print("Message way too long for given image.")
        return 0

    # Truncate the message to max_k
    if k > max_k:
        k = max_k
        bit_array = bit_array[:k*total_pixels]

    # padding
    pad = len(bit_array) % k
    if pad != 0:
        bit_array = bit_array + list('0' * pad)

    i = 0
    for x in range(12, width):
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

    im.save(stego_im)

    return k


def main():
    """ Main function """
    message = input("Enter SECRET message to hid in image:  ")
    filepath = input("Enter path to file:  ")

    k = message_encode(filepath, 2, message)
    print("jajajaj ahora DECODIFICQAMOS1!!!!!!11")
    msg = message_decode(filepath, k)
    print(msg)


def lsb_pic(path):
    return os.path.splitext(path)[0] + "_lsb.png"


if __name__ == "__main__":
    main()
