import re

def colorify(statement,pattern='\<strong style="color:#e74c3c"\>(?P<colored>.*?)\</strong\>', ALERT='danger',url=None):
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


normalising_map = str.maketrans(
                 'أإآؤئىة',
                 'اااءءيه')

def normalizeArabic(text):
     text = text.translate(normalising_map)
     return(text)
