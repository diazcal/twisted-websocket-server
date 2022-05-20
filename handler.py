from twisted.internet import reactor, defer
from jsonschema import validate, exceptions

from error import JSONDecodeErrors
from schemas import schemas


class WSHandler:
	"""
	Manages the logic of the Websocket server itself.
	Once a new client is registered with register_client() the handler keeps a register of clients and callback functions opening
	the door to different implementations using obeserver patternt, filtering messages by client id, etc.
	"""
	def __init__(self):
		self.clients = {}

	# Interfaces to the connection protocol
	def register_client(self, protocol):
		self.clients[protocol.client_id] = protocol

	def process_message(self, message):
		d = defer.Deferred()
		error_code = self._check_message_schema(message)
		if message["message"] == "ping":
			reactor.callLater(0, d.callback, ["pong!", error_code])

		elif message["message"] == "now!":
			reactor.callLater(0, d.callback, ["returning now!", error_code])

		else:
			# Simulate long run execution
			print("We are simulating a long execution without blocking the main loop")
			reactor.callLater(5, d.callback, ["We are done executing a long task", error_code])

		return d

	@staticmethod
	def _check_message_schema(message):
		for schema in schemas:
			try:
				validate(instance=message, schema=schema)
				return JSONDecodeErrors.ALL_OK
			except exceptions.ValidationError:
				pass
		return JSONDecodeErrors.NO_SCHEMA

	def unregister_client(self, protocol):
		del self.clients[protocol.client_id]
