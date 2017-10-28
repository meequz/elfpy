import settings
from utils import import_string


LADDER_FIRST_LINE = True


def get_formatter_class():
    return import_string(settings.FORMATTER)


class BaseFormatter:
    template = '{} -> {}'
    
    def __init__(self, parent_elframe, current_elframe):
        self.parent_elframe = parent_elframe
        self.current_elframe = current_elframe
    
    def __str__(self):
        return self.template.format(self.parent_elframe, self.current_elframe)


class NovelFormatter(BaseFormatter):
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


class LadderFormatter(BaseFormatter):
    template = '{}{}'
    
    def __init__(self, parent_elframe, current_elframe):
        self.parent_elframe = parent_elframe
        self.current_elframe = current_elframe
        self.nesting = self.get_nesting(current_elframe.frame)
    
    def get_nesting(self, frame):
        nesting = 0
        while getattr(frame, 'f_back'):
            nesting += 1
            frame = frame.f_back
        return nesting
    
    def __str__(self):
        global LADDER_FIRST_LINE
        if LADDER_FIRST_LINE:
            LADDER_FIRST_LINE = False
            line = '{}\n    {}'.format(self.parent_elframe,
                                       self.current_elframe)
        else:
            tabs = '    ' * self.nesting
            line = self.template.format(tabs, self.current_elframe)
        return line
