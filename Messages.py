import logging

class Message():
    text = None
    level = None # info or error
    def __init__(self, text, level) -> None:
        self.text = text
        self.level = level


