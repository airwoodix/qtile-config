import os
import subprocess


def get_alternatives(alternatives):
    """
    Parses $PATH and searchs for best match with given list.

    Returns False or if search wasn't successful.
    Returns False if given isn't a list.
    """

    if type(alternatives) is not list:
        return False

    results = []
    for dir in os.environ['PATH'].split(':'):
        for proc in os.listdir(dir):
            if proc in alternatives:
                results.append(proc)

    for i in alternatives:
        if i in results:
            return i

    return False


def execute(command):
    """
    Opens subprocess using subprocess.Popen.

    Takes string or list.
    Returns the return of subprocess.Popen.
    """

    if not type(command) == list:
        command = command.split(' ')

    return subprocess.Popen(command)
