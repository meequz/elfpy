import sys
import time

import settings
from formatters import get_formatter_class

WTF = 'WTF?!'
SKIPME = 'SKIPME!!'
BANNED_WORDS = ['importlib._bootstr', WTF]


class Elframe:
    
    def __init__(self, frame):
        self.frame = frame
    
    def __str__(self):
        if not self.frame:
            return WTF
        if self.is_module:
            return self.filename
        
        func_owner = self.class_type_str + self.class_id_str or self.filename
        if self.is_class:
            func_owner = '{}.{}'.format(self.filename, func_owner)
        output = '{}.{}()'.format(func_owner, self.func_name)
        return output
    
    @property
    def is_module(self):
        return self.frame and self.frame.f_code.co_name == '<module>'
    
    @property
    def is_class(self):
        return self.frame and 'self' in self.frame.f_locals
    
    @property
    def is_func(self):
        return not self.is_class and not self.is_module
    
    @property
    def filename(self):
        if self.frame:
            return self.frame.f_code.co_filename[:-3]
    
    @property
    def func_name(self):
        if self.frame:
            return self.frame.f_code.co_name
    
    @property
    def class_id(self):
        if self.is_class:
            return id(self.frame.f_locals['self'])
    
    @property
    def class_id_str(self):
        if self.class_id:
            return '({})'.format(self.class_id)
        return ''
    
    @property
    def class_type(self):
        if self.is_class:
            return self.frame.f_locals['self'].__class__.__name__
    
    @property
    def class_type_str(self):
        if self.class_type:
            return self.class_type
        return ''


def check_banned_words(line):
    for word in BANNED_WORDS:
        if word in line:
            return True
    return False


def traceit(frame, event, arg):
    if event not in ['call', 'c_call']:
        return
    
    current_frame = Elframe(frame)
    parent_frame = Elframe(frame.f_back)
    formatter = get_formatter_class()(parent_frame, current_frame)
    line = str(formatter)
    if not check_banned_words(line) and not line == SKIPME:
        print(line)
        time.sleep(settings.DELAY)


sys.setprofile(traceit)
