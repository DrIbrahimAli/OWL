import re

def colorify(statement,pattern='#(?P<colored>.*?)#', ALERT='danger'):
    return re.sub(pattern,'<span class="text-{}";>\g<colored></span>'.format(ALERT),statement)
