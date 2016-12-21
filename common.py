
import binascii
import hashlib
import io
import PIL
import PIL.Image
import re
import requests

def findone(pattern, string, otherwise=None, flags=0):
    match = re.findall(pattern, string, flags)
    if len(match) <= 0:
        return otherwise
    return match[0]

def consq_replace(text, *args):
    for i in range(0, int(len(args) / 2)):
        text = text.replace(args[i*2], args[i*2+1])
    return text

def consq_sub(text, *args):
    for i in range(0, int(len(args) / 2)):
        try:
            text = re.sub(args[i*2], args[i*2+1], text)
        except:
            raise TypeError('Error while subtituting string: "%s" -> "%s" in "%s"' % (args[i*2], args[i*2+1], text))
    return text

def get_string_width(text):
    b = text.encode('utf-8', 'ignore')
    res = 0
    for i in b:
        if int(i) < 128:
            res += 1
        else:
            res += 1
    return res

def sha256(binary_in):
    if type(binary_in) == str:
        binary_in = binary_in.encode('utf-8')
    digest = hashlib.sha256(binary_in).digest()
    asc = binascii.hexlify(digest).decode('utf-8')
    return asc

requests_session = requests.Session()
# requests_session.trust_env = False
requests_timeout = 3.0

def request(function, *args, encoding='utf-8', **kwargs):
    connection_established = True
    if function.lower() == 'get':
        function = requests_session.get
    elif function.lower() == 'post':
        function = requests_session.post
    else:
        raise ValueError('Unsupported HTML operation.')
    try:
        req = function(*args, **kwargs,
            headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0' })
        req.encoding = encoding
    except Exception as err:
        connection_established = False
    if not connection_established:
        raise IOError('Remote server is unreachable.')
    return req

def convert_image(data):
    hfile = io.BytesIO(data)
    himage = PIL.Image.open(hfile)
    hfileout = io.BytesIO()
    himage.save(hfileout, format='png')
    hfileout.seek(0)
    out = hfileout.read()
    return out
