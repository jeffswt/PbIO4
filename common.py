
import binascii
import hashlib
import re
import requests

def findone(pattern, string, otherwise=None, flags=0):
    match = re.findall(pattern, string, flags)
    if len(match) <= 0:
        return otherwise
    return match[0]

def sha256(binary_in):
    digest = hashlib.sha256(binary_in).digest()
    asc = binascii.hexlify(digest).encode('utf-8')
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
