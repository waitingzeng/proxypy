#!/usr/bin/env python

"""
  Copyright notice
  ================

  Copyright (C) 2011
      Roberto Paleari     <roberto.paleari@gmail.com>
      Alessandro Reina    <alessandro.reina@gmail.com>

  This program is free software: you can redistribute it and/or modify it under
  the terms of the GNU General Public License as published by the Free Software
  Foundation, either version 3 of the License, or (at your option) any later
  version.

  HyperDbg is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along with
  this program. If not, see <http://www.gnu.org/licenses/>.

"""

import sys
from optparse import OptionParser
import getopt

from core import *

parser = OptionParser()
parser.add_option("-v", "--verbosity", dest="verbosity",
                  action="store_true", help="be more verbose")
parser.add_option(
    "-a", "--addr", type="string", dest="addr", default='0.0.0.0',
    help="listen address (default 0.0.0.0)")
parser.add_option("-p", "--port", dest="port", type="int",
                  default=8080, help="listen port  (default 8080)")
parser.add_option("-x", "--plugin", dest="plugin", type="string",
                  help="load a ProxPy plugin")
parser.add_option("-d", "--dump", dest="dumpfile", type="string", 
                  help="on termination, dump requests & responses to file")
parser.add_option("-r", "--redirect", dest="redirect",
                  help="<host:[port]> redirect HTTP traffic to target host (default port: 80)")
parser.add_option("-q", "--auth", dest="auth", help="auth username and password", default='')


def parse_options():
    options, args = parser.parse_args(sys.argv[1:])

    ps = ProxyState()

    if options.verbosity:
        ps.log.verbosity += 1

    if options.dumpfile:
        ps.dumpfile = options.dumpfile

    ps.listenport = options.port

    ps.listenaddr = options.addr

    ps.auth = options.auth
    
    if options.plugin:
        ps.plugin = ProxyPlugin(options.plugin)

    # Check and parse redirection host
    if options.redirect:
        h = options.redirect
        if ':' not in h:
            p = 80
        else:
            h, p = h.split(':')
            p = int(p)
        ps.redirect = (h, p)

    return ps


def main():
    global proxystate
    proxystate = parse_options()
    proxyServer = ProxyServer(proxystate)
    proxyServer.startProxyServer()

if __name__ == "__main__":
    global proxystate
    try:
        main()
    except KeyboardInterrupt, e:
        nreq, nres = proxystate.history.count()
        proxystate.log.info(
            "Terminating... [%d requests, %d responses]" % (nreq, nres))
        if proxystate.dumpfile is not None:
            data = proxystate.history.dumpXML()
            f = open(proxystate.dumpfile, 'w')
            f.write(data)
            f.close()
