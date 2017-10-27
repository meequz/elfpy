import sys


class Elframe:
    
    def __init__(self, frame):
        self.frame = frame
        self.func_name = self.frame.f_code.co_name
        self.is_class = 'self' in frame.f_locals
        self.is_module = frame.f_code.co_name == '<module>'
    
    def __str__(self):
        if not self.frame:
            return 'WTF?!'
        if self.is_module:
            return __name__
        
        func_owner = self.class_type + self.class_id or __name__
        output = '{}.{}()'.format(func_owner, self.func_name)
        return output
    
    @property
    def class_id(self):
        if self.is_class:
            class_id_ = id(self.frame.f_locals['self'])
            return '({})'.format(class_id_)
        return ''
    
    @property
    def class_type(self):
        if self.is_class:
            return self.frame.f_locals['self'].__class__.__name__
        return ''


def traceit(frame, event, arg):
    if event not in ['call', 'c_call']:
        return

    current_frame = Elframe(frame)
    parent_frame = Elframe(frame.f_back)
    line = '{} -> {}'.format(parent_frame, current_frame)
    print(line)


class A(object):
    def __init__(self):
        self.amel()
    
    def amel(self):
        pass
    
    def foo(self, b):
        bar(b)


def bar(*a):
    pass


sys.setprofile(traceit)


if __name__ == '__main__':
    a = A()
    a.foo(1)
