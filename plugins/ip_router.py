#!/user/bin/python
#coding=utf8
import socket

old_socket = socket.socket

def new_socket(*args, **kwargs):
    from core import proxystate
    sock = old_socket(*args, **kwargs)
    sock.bind((proxystate.server_address, 0))
    return sock

socket.socket = new_socket

