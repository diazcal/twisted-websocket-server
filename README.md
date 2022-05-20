# twisted-websocket-server
A websocket server PoC built with Twisted and Autobahn. 

Run the main.py and connect a client via Simple Web Socket Client or similar to localhost:9998

## Schemas
A client can send:


Ping:
```json
{
  "message": "ping"
}
```

Return reply immediately:
```json
{
  "message": "now!"
}
```

Simulate long message processing (5 secs. by default)
```json
{
  "message": <you can put whatever you want here>
}
```

The response follows this schema:
```json
{
  "result": "",
  "error": ""
}
```
## References
- [How do Twisted python Factory and Protocol interfaces work?](https://stackoverflow.com/questions/31888037/how-do-twisted-python-factory-and-protocol-interfaces-work/31889487#31889487)
- [Autobahn websocket programming](https://autobahn.readthedocs.io/en/latest/websocket/programming.html)
- [Twisted task scheduler](https://docs.twistedmatrix.com/en/twisted-17.9.0/core/howto/time.html)
- [Twisted deferreds (check for async/await)](https://twistedmatrix.com/documents/current/core/howto/defer-intro.html)
- [Migrate deferred to async/await](https://patrick.cloke.us/posts/2021/06/11/converting-twisteds-inlinecallbacks-to-async/)