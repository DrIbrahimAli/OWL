import re

def colorify(statement,pattern='#(?P<colored>.*?)#', ALERT='danger',url=None):
    if url:
        return re.sub(pattern,'<a href="{}" target="_blank"><span class="text-{}" >\g<colored></span></a>'.format(url,ALERT),statement)
    else:
        return re.sub(pattern,'<span class="text-{}" >\g<colored></span>'.format(ALERT),statement)

def is_int(x):
    try:
        int(x)
        return True
    except:
        return False
