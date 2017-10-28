import settings
from utils import import_string


def get_formatter_class():
    return import_string(settings.FORMATTER)


class DefaultFormatter:
    template = '{} -> {}'
    
    def __init__(self, parent_elframe, current_elframe):
        self.parent_elframe = parent_elframe
        self.current_elframe = current_elframe
    
    def __str__(self):
        return self.template.format(self.parent_elframe, self.current_elframe)


class NovelFormatter(DefaultFormatter):
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


class LadderFormatter(DefaultFormatter):
    template = '\n    '
