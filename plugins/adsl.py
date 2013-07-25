#!/user/bin/python
# coding=utf8
import platform
import os
import time
import urllib2
import sys

if platform.system() == 'Windows':
    class ADSL(object):
        #==============================================================================
        # __init__ : name: adsl名称
        #======================================================================

        def __init__(self, name, username, password, **kwargs):
            self.name = name
            self.username = username
            self.password = password

        #==============================================================================
        # connect : 宽带拨号
        #======================================================================
        def connect(self):
            from core import proxystate
            cmd_str = "rasdial %s %s %s" % (
                self.name, self.username, self.password)
            proxystate.log.info(cmd_str)
            os.system(cmd_str)

        #==============================================================================
        # disconnect : 断开宽带连接
        #======================================================================
        def disconnect(self):
            cmd_str = "rasdial %s /DISCONNECT" % self.name
            from core import proxystate
            proxystate.log.info(cmd_str)
            os.system(cmd_str)

        #==============================================================================
        # reconnect : 重新进行拨号
        #======================================================================
        def reconnect(self):
            self.disconnect()
            time.sleep(1)
            self.connect()
else:
    class ADSL(object):

        def __init__(self, *args, **kwargs):
            pass

        def connect(self):
            pass

        def disconnect(self):
            pass

        def reconnect(self):
            pass


from random import randrange


def gen_ip():
    not_valid = [10, 127, 169, 172, 192]

    first = randrange(1, 256)
    while first in not_valid:
        first = randrange(1, 256)

    ip = ".".join([str(first), str(randrange(1, 256)),
                   str(randrange(1, 256)), str(randrange(1, 256))])
    return ip


def proxy_mangle_request(req):
    from http import HTTPResponse
    from core import proxystate
    host, port = req.getHost()
    if host in ['proxy.disconnect', 'proxy.connect', 'proxy.reconnect']:
        params = req.getParams()
        proxystate.log.info("adsl action: %s, params: %s]" % (host, params))
        adsl = ADSL(**params)
        if host == 'proxy.disconnect':
            adsl.disconnect()
        elif host == 'proxy.connect':
            adsl.connect()
        elif host == 'proxy.reconnect':
            adsl.reconnect()
        try:
            ip = urllib2.urlopen(
                'http://sphone.speedy-custom.com/update_ip/%s' % params['name']).read()
        except:
            ip = ''
        res = HTTPResponse('HTTP/1.1', 200, 'OK', body="OK %s" % ip)
        return res

    #req.setHeader("X-Forwarded-For", gen_ip())
    return req


def main():
    while True:
        try:
            print urllib2.urlopen('http://sphone.speedy-custom.com/update_ip/%s' % sys.argv[1]).read()
        except:
            print 'error'
        time.sleep(1)


if __name__ == '__main__':
    main()
