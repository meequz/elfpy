import sys
import time


# FIXME
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
    template = '{} -> {}'
    
    def __init__(self, parent_elframe, current_elframe):
        self.parent_elframe = parent_elframe
        self.current_elframe = current_elframe
    
    def __str__(self):
        return self.template.format(self.parent_elframe, self.current_elframe)


class NovelFormatter(Formatter):
    template = '{} called {}'
    
    def format_parent(self, elframe):
        if elframe.is_module:
            return "module '{}'".format(elframe)
        
        if elframe.is_class:
            elframe_template = "'{}' method of '{}.{}({})'"
            res = elframe_template.format(
                elframe.func_name, elframe.filename, elframe.class_type,
                elframe.class_id)
            return res
        
        return "'{}'".format(elframe)
    
    def format_current(self, elframe):
        if elframe.func_name == '__init__':
            self.template = '{} created instance of {}'
            elframe_template = "'{}.{}' class with ID {}"
            res = elframe_template.format(
                elframe.filename, elframe.class_type_str, elframe.class_id)
            return res
        
        return "'{}'".format(elframe)
    
    def __str__(self):
        parent_str = self.format_parent(self.parent_elframe)
        current_str = self.format_current(self.current_elframe)
        return self.template.format(parent_str, current_str)


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
    # formatter = Formatter(parent_frame, current_frame)
    formatter = NovelFormatter(parent_frame, current_frame)
    line = str(formatter)
    if not check_banned_words(line) and not line == SKIPME:
        print(line)
        time.sleep(0.5)


sys.setprofile(traceit)
