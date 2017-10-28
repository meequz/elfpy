from importlib import import_module


def import_string(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)
