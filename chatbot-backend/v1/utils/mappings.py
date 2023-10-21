from v1.src.handler import *

NODE_MAPPINGS ={
    "textNode": {"user": "AI", "handler": TextHandler.from_data},
    "startNode": {"user": "AI", "handler": TextHandler.from_data},
    "listenerNode": {"user": "USER", "handler": ListenHandler.from_data},
    "endNode": {"user": "AI", "handler": EndHandler.from_data},
    "deciderNode": {"user": "AI", "handler": DeciderHandler.from_data},
    "intentNode": {"user": "AI", "handler": IntentHandler.from_data},
    "qaNode": {"user": "AI", "handler": QaHandler.from_data},
    "aiNode": {"user": "AI", "handler": AIHandler.from_data},
    "validatorNode": {"user": "AI", "handler": ValidatorHandler.from_data},
    "setValueNode": {"user": "AI", "handler": SetValueHandler.from_data},
    "counterNode": {"user": "AI", "handler": CounterHandler.from_data},
    "ifNode": {"user": "AI", "handler": IfHandler.from_data},
    "ticketNode": {"user": "AI", "handler": TicketHandler.from_data},
}

