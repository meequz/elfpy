import subprocess
from importlib import import_module

import constants
import settings


def import_string(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def to_yellow(text):
    return '\033[93m' + text + '\033[0m'


def to_green(text):
    return '\033[92m' + text + '\033[0m'


def shell_execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    code = process.wait()
    if code != 0:
        raise RuntimeError('Command failed')
    output = [line.decode() for line in process.stdout]
    return ''.join(output)


def is_banned(line):
    for word in settings.BANNED_WORDS:
        if word in line:
            return True
    if constants.WTF in line:
        return True
    if line == constants.SKIPME:
        return True
    return False
