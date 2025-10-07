from enum import Enum

class Menu(Enum):
    FILE = 1
    FILE_OPEN_XML = 2

class Action:
    # Action Message fields
    action = "action"
    message = "message"
    
    # Action types
    EXPORT_ONE_EXCEL = "EXPORT_ONE_EXCEL"
    EXPORT_ALL_EXCEL = "EXPORT_ALL_EXCEL"
    OPEN_XML_FILE = "OPEN_XML_FILE"
    PREV_PAGE = "PREV_PAGE"
    NEXT_PAGE = "NEXT_PAGE"

    # Message type
    file = "file"

class ActionMessage(object):
    def __new__(self, action, message=dict()):
        message = {
            "action": action,
            "message": message
        }
        return message

class Data:
    General = "General"
    Table = "Table"
