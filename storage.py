
import copy

def get(engine_id):
    """ get(engine_id) -- Retrieve local storage for given engine. """
    if not __storage_index:
        load_storage()
    data = copy.deepcopy(__storage_index[engine_id])
    return data

def set(engine_id, data):
    """ set(engine_id) -- Set local storage data for given engine. """
    if not __storage_index:
        load_storage()
    __storage_index[engine_id] = copy.deepcopy(data)
    flush_storage()
