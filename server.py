import json
import uuid

from twisted.python import log
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from error import JSONDecodeErrors


class WSProtocol(WebSocketServerProtocol):
    """
    Serves a client connection to the WebSocket endpoint.
    This class is only managing the server/client communication events, all the logic after the message consumption is managed by the
    message handler.
    Follows Twisted CamelCase style for event methods.
    """

    def __init__(self, message_handler):
        super(WSProtocol, self).__init__()
        self.message_handler = message_handler
        self.client_id = uuid.uuid4()
        self.message_handler.register_client(self)

    def onOpen(self):
        log.msg("Client with IP {ip} connected and has been asigned ID: {id}".format(ip=self.transport.client[0], id=self.client_id))

    def onMessage(self, payload, isBinary):
        """
        This is the old way to do async with Twisted: deferreds and callbacks.
        It works but is much better to use async/await since Python 3.5 and make asycio compabilty easy--> TODO
        """

        decoded_messge = payload.decode("utf-8")

        try:
            message = json.loads(decoded_messge)
            log.msg("Client {id} sent: {x}".format(id=self.client_id, ip=self.transport.client[0], x=message))

            d = self.message_handler.process_message(message)
            d.addCallback(self._build_response)
            d.addCallback(self._sendToClient)

        except ValueError:
            reply = {
                "result": {},
                "error": {
                    "code": JSONDecodeErrors.INVALID_JSON.value,
                    "message": JSONDecodeErrors.INVALID_JSON.name
                }
            }
            response = json.dumps(reply)
            self._sendToClient(response)
            log.err(f"Error processing JSON {message}. Server response: wrong JSON format")

    def _sendToClient(self, message):
        self.sendMessage(message.encode('utf-8'))
        log.msg("Server response to {id}: ".format(id=self.client_id) + message)

    def _build_response(self, defer_response):
        reply = {"result": defer_response[0], "error": {"key": defer_response[1].name, "code": defer_response[1].value}}
        json_response = json.dumps(reply)
        return json_response

    def onClose(self, wasClean, code, reason):
        self.message_handler.unregister_client(self)
        log.msg("Client with ID {id} disconnected".format(id=self.client_id))


class WSFactory(WebSocketServerFactory):
    def __init__(self, ws_protocol, message_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_handler = message_handler
        self.ws_protocol = ws_protocol

    def buildProtocol(self, *args, **kwargs):
        protocol = self.ws_protocol(self.message_handler)      # pass the handler from the factory to every client protocol.
        protocol.factory = self
        return protocol
