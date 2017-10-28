import settings
import utils


LADDER_FIRST_LINE = True


def get_formatter_class():
    return utils.import_string(settings.FORMATTER)


class BaseFormatter:
    template = '{} -> {}'
    
    def __init__(self, parent_elframe, current_elframe):
        self.parent_elframe = parent_elframe
        self.current_elframe = current_elframe
    
    def colorize(sefl, elframe):
        if elframe.is_func:
            elframe_str = utils.to_green(str(elframe))
        elif elframe.is_class:
            elframe_str = utils.to_yellow(str(elframe))
        else:
            elframe_str = str(elframe)
        return elframe_str
    
    def __str__(self):
        parent = self.colorize(self.parent_elframe)
        current = self.colorize(self.current_elframe)
        return self.template.format(parent, current)


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
        
        return "'{}'".format(self.colorize(elframe))
    
    def format_current(self, elframe):
        if elframe.func_name == '__init__':
            self.template = '{} created instance of {}'
            elframe_template = "'{}.{}' class with ID {}"
            res = elframe_template.format(
                elframe.filename, elframe.class_type_str, elframe.class_id)
            return res
        
        return "'{}'".format(self.colorize(elframe))
    
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
        parent = self.colorize(self.parent_elframe)
        current = self.colorize(self.current_elframe)
        
        if LADDER_FIRST_LINE:
            LADDER_FIRST_LINE = False
            line = '{}\n    {}'.format(parent, current)
        else:
            tabs = '    ' * self.nesting
            line = self.template.format(tabs, current)
        return line
