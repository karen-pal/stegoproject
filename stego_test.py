import base64
import bitarray
import random
import unittest

import stego

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


class TestStego(unittest.TestCase):
    def test_set_pixel(self):
        msg = "test"
        color = 0
        i = 0
        k = 1

        encoded_msg = base64.b64decode(msg.encode('ascii'))
        bit_array = bitarray.bitarray()
        bit_array.frombytes(encoded_msg)
        bit_array = [int(b) for b in bit_array]

        self.assertEqual(stego.set_pixel(color, bit_array, i, k), 1,
                         "\ncolor: {}, bit to set: {}, k: {}".
                         format(color, bit_array[i], k))

        i = 1
        self.assertEqual(stego.set_pixel(color, bit_array, i, k), 0,
                         "\ncolor: {}, bit to set: {}, k: {}".
                         format(color, bit_array[i], k))

    def test_message_encode(self):
        long_msg = "long message" * 100000

        for pic in PICS:
            # Expected K
            self.assertEqual(stego.message_encode(pic, 1, "nice"), 1)
            self.assertEqual(stego.message_encode(pic, 2, "nice"), 1)
            self.assertEqual(stego.message_encode(pic, 3, "nice"), 1)

            # Big messages
            self.assertLessEqual(stego.message_encode(pic, 1, long_msg), 1)
            self.assertLessEqual(stego.message_encode(pic, 2, long_msg), 2)
            self.assertLessEqual(stego.message_encode(pic, 3, long_msg), 3)

    def test_message_decode(self):
        msgs = ["u", "test", "steganography is cool and fun"]

        for pic in PICS:
            for msg in msgs:
                k = stego.message_encode(pic, 1, msg)
                self.assertEqual(stego.message_decode(stego.lsb_pic(pic), k),
                                 msg, "\nk: {}, image: {}".format(k, pic))


if __name__ == '__main__':
    unittest.main()
