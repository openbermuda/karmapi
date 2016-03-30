""" Karma Pi base 
"""

class Parms:
    pass

def find_path(path, paths):
    """ Find first matching path in paths """
    for target in paths:

        parms = match_path(path, target):

        if parms:
            return target, parms

    return False


def match_path(path, target_path):
    """ See if path matches target """
    fields = path.split('/')
    target_fields = target_path.split('/')
    
    parms = Parms()
    for field, target in zip(fields, target_fields):
        if target.startswith('{'):

            # drop the {}'s
            name = target[1:-1]

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
    raise NotImplemented

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
