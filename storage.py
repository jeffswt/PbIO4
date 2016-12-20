
import pickle
import copy
import lzma

__storage_index = None

def load_storage(file_name='pbio4.context'):
    """ load_storage() -- Load storage from local file. Default to file name
    "pbio4.context". """
    global __storage_index
    # Reading file.
    store = {}
    try:
        f = open(file_name, 'rb')
        d = f.read()
        f.close()
        # De-compressing data.
        d = lzma.decompress(d)
        # Un-pickling data
        store = pickle.loads(d)
    except Exception as err:
        store = {}
    if type(store) != dict:
        store = {}
    __storage_index = store
    return

def flush_storage(file_name='pbio4.context'):
    """ flush_storage() -- Flush storage to local file. Default to file name
    "pbio4.context". """
    # Pickling data.
    d = pickle.dumps(__storage_index)
    # Compressing data.
    d = lzma.compress(d)
    # Writing to file.
    f = open(file_name, 'wb')
    f.seek(0)
    f.write(d)
    f.close()
    return

def get(engine_id):
    """ get(engine_id) -- Retrieve local storage for given engine. """
    if not __storage_index:
        load_storage()
    data = copy.deepcopy(__storage_index.get(engine_id, {}))
    return data

def set(engine_id, data):
    """ set(engine_id, data) -- Set local storage data for given engine. """
    if not __storage_index:
        load_storage()
    __storage_index[engine_id] = copy.deepcopy(data)
    flush_storage()
    return

def get(engine_id, key):
    """ get(engine_id, key) -- Retrieve data 'key' from local storage for given
    engine. """
    if not __storage_index:
        load_storage()
    data = __storage_index.get(engine_id, {}).get(key)
    data = copy.deepcopy(data)
    return data

def set(engine_id, key, data):
    """ set(engine_id, key, data) -- Set local storage data for 'key' for given
    engine. """
    if not __storage_index:
        load_storage()
    data = copy.deepcopy(data)
    if engine_id not in __storage_index:
        __storage_index[engine_id] = {}
    __storage_index[engine_id][key] = data
    flush_storage()
    return
