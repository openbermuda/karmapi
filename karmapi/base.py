""" Karma Pi base 
"""

class Parms:
    pass

def find_path(path, paths):
    """ Find first matching path in paths """
    for target in paths:

        parms = match_path(path, target)

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
    match = find_path(path, BUILD_PATHS)
    
    if not target_path:
        raise AttributeError("Unrecognised path: {}".format(path))

    # Call the builder
    target_path, parms = match
    BUILD_PATHS[target_path](path)


def get_data(path):
    """ Get data for a path """
    if not os.path.exists(path):
        raise AttributeError

    # get the meta data
    meta = get_meta_data(path)

    # Now figure out the module to use
    # Find the function to call
    # call it
    

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

    return {}
