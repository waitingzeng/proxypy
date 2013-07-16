#!/user/bin/python
# coding=utf8
import platform
import os
import time

if platform.system() == 'Windows':
    class ADSL(object):
        #==============================================================================
        # __init__ : name: adsl名称
        #=========================================================================

        def __init__(self, name, username, password, **kwargs):
            self.name = name
            self.username = username
            self.password = password

        #==============================================================================
        # connect : 宽带拨号
        #=========================================================================
        def connect(self):
            cmd_str = "rasdial %s %s %s" % (
                self.name, self.username, self.password)
            os.system(cmd_str)

        #==============================================================================
        # disconnect : 断开宽带连接
        #=========================================================================
        def disconnect(self):
            cmd_str = "rasdial %s /disconnect" % self.name
            os.system(cmd_str)

        #==============================================================================
        # reconnect : 重新进行拨号
        #=========================================================================
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

        res = HTTPResponse('HTTP/1.1', 200, 'OK', body="OK")
        return res
    return req
