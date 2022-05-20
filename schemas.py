ping_schema = {
    "type": "object",
    "properties": {
        "message": {
            "description": "Check if the server is alive",
            "type": "string",
            "pattern": "^ping$"
        }
    },
    "required": ["ping"]
}


message_schema = {
    "type": "object",
    "properties": {
        "message": {
            "description": "Standard message",
            "type": "string"
        }
    },
    "required": ["message"]
}


schemas = [ping_schema, message_schema]
