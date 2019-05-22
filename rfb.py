from socket import socket
from struct import pack, unpack
import random


class RFB:
    def __init__(self, conn: socket):
        self.conn = conn
        self._start()
    
    def _start(self):
        # protocol_version handshake
        protocol_version = "RFB 003.008"
        self.conn.send(bytes(protocol_version + "\n", encoding='utf-8'))
        protocol_version = self.conn.recv(12)
        print('protocol-version:', protocol_version)
    
        # security handshake
        number_of_security_types = 1
        security_type = 1
        self.conn.send(pack('!BB', number_of_security_types, security_type))
        security_type = unpack('!b', self.conn.recv(1))[0]
        print('security-type:', security_type)
    
        # security result handshake
        security_result = 0
        self.conn.send(pack('!L', security_result))
    
        # client init
        shared_flag = unpack('!b', self.conn.recv(1))[0]
        print('shared-flag:', shared_flag)
    
        # server init
        framebuffer_width = 800
        framebuffer_height = 600
        self.conn.send(pack('!HH', framebuffer_width, framebuffer_height))
        bits_per_pixel = 32
        depth = 24
        big_endian = 1
        true_color = 1
        red_max = 255
        green_max = 255
        blue_max = 255
        red_shift = 0
        green_shift = 0
        blue_shift = 0
        self.conn.send(pack('!bbbbhhhbbbbbb', bits_per_pixel, depth, big_endian, true_color,
                       red_max, green_max, blue_max,
                       red_shift, green_shift, blue_shift, 0, 0, 0))
    
        server_name = 'KekVNC'
        name_length = len(server_name)
        self.conn.send(pack('!L', name_length))
        self.conn.send(bytes(server_name + '\n', encoding='utf-8'))

        while True:
            message_type = unpack('!b', self.conn.recv(1))[0]
            print('message-type:', message_type)
            if message_type == 0:
                self.set_pixel_format()
            elif message_type == 2:
                self.set_encodings()
            elif message_type == 3:
                self.framebuffer_update_request()
            elif message_type == 4:
                self.key_event()
            elif message_type == 5:
                self.pointer_event()
            elif message_type == 6:
                self.client_cut_text()
            else:
                print('unsupported command')
                break
            print()

    def set_encodings(self):
        padding, number_of_encodings = unpack('!bh', self.conn.recv(3))
        print('padding:', padding)
        print('number-of-encodings:', number_of_encodings)
        encodings = []
        for _ in range(number_of_encodings):
            encodings.append(unpack('!L', self.conn.recv(4))[0])
        print('encodings:', encodings)
    
    def framebuffer_update_request(self):
        inc, x_pos, y_pos, w, h = unpack('!bhhhh', self.conn.recv(9))
        print('incremental:', inc)
        print('x-position:', x_pos)
        print('y-position:', y_pos)
        print('width:', w)
        print('height:', h)
        self.framebuffer_update(x_pos, y_pos, w, h)
    
    def framebuffer_update(self, x, y, width, height):
        number_of_rectangles = 1
        self.conn.send(pack('!bbh', 0, 0, number_of_rectangles))
        for _ in range(number_of_rectangles):
            encoding_type = 0
            self.conn.send(pack('!hhhhi', x, y, width, height, encoding_type))
            pixels = []
            for i in range(width):
                for j in range(height):
                    pixels.append(random.randint(1, 4294967296))
            self.conn.send(pack('!' + ('L' * (width * height)), *pixels))
    
    def set_pixel_format(self):
        padding = self.conn.recv(3)
        print('padding:', padding)
        bits_per_pixel, depth, big_endian, true_color, red_max, green_max, blue_max, red_shift, green_shift, blue_shift = unpack(
            '!bbbbhhhbbb', self.conn.recv(13))
        padding = self.conn.recv(3)
        print('bits_per_pixel:', bits_per_pixel)
        print('depth:', depth)
        print('big-endian-flag:', big_endian)
        print('true-color-flag:', true_color)
        print('red-max:', red_max)
        print('green-max:', green_max)
        print('blue-max:', blue_max)
        print('red-shift:', red_shift)
        print('green-shift:', green_shift)
        print('blue-shift:', blue_shift)
        print('padding:', padding)
    
    def pointer_event(self):
        button_mask, x, y = unpack('!bhh', self.conn.recv(5))
        print('button-mask:', button_mask)
        print('x-position:', x)
        print('y-position:', y)
    
    def key_event(self):
        raise Exception()
    
    def client_cut_text(self):
        raise Exception()
