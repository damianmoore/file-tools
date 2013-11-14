import os


def get_console_width():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)

def format_output(msg, columns):                                                
    return '%s%s' % (msg, ' ' * (columns - len(msg)))
