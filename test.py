import elfpy


class A(object):
    def __init__(self):
        self.amel()
    
    def amel(self):
        pass
    
    def foo(self, b):
        bar(b)


def bar(*a):
    pass


if __name__ == '__main__':
    a = A()
    a.foo(1)
