# -*- encoding: utf-8 -*-

class MalformedImageException(Exception):
    def __init__(self, message):
        super().__init__(message)
