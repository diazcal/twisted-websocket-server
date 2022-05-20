import sys

from server import WSFactory, WSProtocol
from handler import WSHandler
from twisted.internet import reactor, endpoints
from twisted.python import log

log.startLogging(sys.stdout)
log.msg("Server started")

server_logic = WSHandler()
factory = WSFactory(WSProtocol, server_logic)
endpoints.TCP4ServerEndpoint(reactor, port=9998, interface="localhost").listen(factory)

reactor.run()
