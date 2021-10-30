# -*- Coding: utf-8 -*-
import uuid

class Audio:
    """ Clase Audio. """
    
    def __init__(self, path, filename, uid=None):
        self.path = path
        self.filename = filename
        self.uid = uid or uuid.uuid4()
    
    def to_dict(self):
        return vars(self)

    @staticmethod
    def schema():
        return ['path', 'filename', 'uid']