import re

def colorify(statement,pattern='#(?P<colored>.*?)#', ALERT='danger',url=None):
    if url:
        return re.sub(pattern,'<span class="text-{}" > <a href="{}" target="_blank"> \g<colored> </a> </span>'.format(ALERT,url),statement)
    else:
        return re.sub(pattern,'<span class="text-{}" > \g<colored> </span>'.format(ALERT),statement)
