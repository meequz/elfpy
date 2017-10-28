import sys
import time


# FIXME
WTF = 'WTF?!'
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


class Formatter:
    
    def __init__(self, parent_elframe, current_elframe):
        self.parent_elframe = parent_elframe
        self.current_elframe = current_elframe
    
    def __str__(self):
        return '{} -> {}'.format(self.parent_elframe, self.current_elframe)


class NovelFormatter(Formatter):
    
    def format_elframe(self, elframe):
        return str(elframe)
    
    def __str__(self):
        parent_str = self.format_elframe(self.parent_elframe)
        current_str = self.format_elframe(self.current_elframe)
        return '{} called {}'.format(parent_str, current_str)


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
    formatter = Formatter(parent_frame, current_frame)
    line = str(formatter)
    if not check_banned_words(line):
        print(line)
        time.sleep(0.5)


sys.setprofile(traceit)
