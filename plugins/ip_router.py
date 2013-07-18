#!/user/bin/python
#coding=utf8
import socket

old_socket = socket.socket

def new_socket(*args, **kwargs):
    from core import proxystate
    sock = old_socket(*args, **kwargs)
    try:
        sock.bind((proxystate.thread_local.server_address[0], 0))
    except AttributeError:
        pass
    return sock

socket.socket = new_socket

