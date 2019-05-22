#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
from rfb import RFB

HOST = '127.0.0.1'
PORT = 65432


def main():
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(0)
        conn, addr = s.accept()
        print('connected by', addr)
        RFB(conn)


if __name__ == '__main__':
    main()
