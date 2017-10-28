from importlib import import_module


def import_string(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def to_yellow(text):
    return '\033[93m' + text + '\033[0m'


def to_green(text):
    return '\033[92m' + text + '\033[0m'
