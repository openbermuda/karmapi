""" Karma Pi base 

get(path): get data at path

build(path):  build data at path

get_meta(path):  get meta data for path

"""

class Parms:
    pass

def find_path(path, paths):
    """ Find first matching path in paths 

    Paths is a dictionary.

    The values are dictionaries too, with a path key.
    """
    for key, target in paths.items():

        parms = match_path(path, target['path'])

        if parms:
            return target, parms

    return False

CASTS = dict(int=int, float=float)

def match_path(path, target_path):
    """ See if path matches target """
    fields = path.split('/')
    target_fields = target_path.split('/')

    parms = Parms()
    for field, target in zip(fields, target_fields):
        if target.startswith('<'):

            # drop the <>'s
            name = target[1:-1]

            if ':' in name:
                typehint, name = name.split(':')

                field = CASTS.get(typehint, str)(field)

            setattr(parms, name, field)

        else:
            if field != target:
                return None

    return parms


def build(path):
    """ Dispatch to the appropriate function 

    NB flask has already solved this.
    """
    meta = get_meta_data(path)

    return dispatch(path, meta.get('builds', {}))

def get(path):
    """ Get data for a path """
    # get the meta data
    meta = get_meta_data(path)

    return dispatch(path, meta.get('paths', {}))
    

def dispatch(path, paths):
    """  Dispatch a function call """
    # match the path to meta data paths
    match = find_path(path, paths)

    if not match:
        raise AttributeError("Unrecognised path: {}".format(path))

    # unpack match return value
    target, parms = match

    # extract function to call
    function = get_item(target.get('karma'))

    # Call the function
    return function(path)


def get_meta_data(path):
    """ Spin along a path gathering up meta data """
    meta = {}

    fields = path.split('/')
    path = []
    for field in fields:
        path.append(field)
        
        meta.update(load_meta_path('/'.join(path)))

    return meta
        
def load_meta_path(path):
    """ Load meta data a path if it exists """
    filename = os.path.join(path, 'meta.json')
    if os.path.exists(filename):
        with open(filename) as infile:
            return json.loads(infile)

    # return empty dictionary if there is no meta data here
    return {}

def get_item(path):
    """ Given a path, return the item

    Item is usually some sort of python callable.

    It could be a function or a class name.
    """
    path = path.split('.')

    module_name = '.'.join(path[:-1])

    module = importlib.import_module(module_name)

    return getattr(module, path[-1])
    
