""" Karma Pi base 

get(path): get data at path

build(path):  build data at path

get_meta(path):  get meta data for path

"""
import os
import importlib
import json
import datetime
from pathlib import Path
from contextlib import contextmanager

import pandas

BASE_FOLDER = '.'

PEARS = []

class Parms:

    def __init__(self, data=None):

        if data:
            self.__dict__.update(data)

    def update(self, data):

        self.__dict__.update(data)
        

def find_path(path, paths):
    """ Find first matching path in paths 

    Paths is a dictionary.

    The values are dictionaries too, with a path key.
    """
    for key, target in paths.items():

        parms = match_path(path, target['path'])

        if parms:
            parms.update(dict(target=target))
            return parms

    return False

CASTS = dict(int=int, float=float)


def match_path(path, target_path):
    """ See if path matches target """
    
    fields = path.split('/')
    target_fields = target_path.split('/')

    if len(fields) != len(target_fields): return None
    
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


def meta_data_match(path, key='gets'):
    """ Work our way along path looking for a match """

    folders = path.split('/')
    print(folders)
    bases = []
    relatives = folders[1:]
    
    for folder in folders:
        bases.append(folder)
    
        base = '/'.join(bases)
        relative_path = '/'.join(relatives)
        
        if relatives:
            del relatives[0]

        meta = load_meta_path(base)

        parms = find_path(relative_path, meta.get(key, {}))

        if parms:
            parms.update(dict(base=base,
                              path=relative_path))
            return parms
    
def build(path):
    """ Dispatch to the appropriate function 

    NB flask has already solved this.
    """
    return dispatch(path, key='builds')

def get(path):
    """ Get data for a path """
    print("GET:", path)
    print("CWD:", os.getcwd())
    result = None
    problem = None
    
    try:
        result = dispatch(path, key='gets')
    except Exception as e:

        print('OOOPS')
        print(e)
        problem = e
        
        # try a peer if we have any
        for pear in PEARS:
            try:
                result = pear.get(path)

                # FIXME, save result so we don't have to fetch it again.
                # Problem here is we need to be able to go from the model
                # to the form stored on disk.  Might need a save or write
                # method, split out from build.
                break
            except Exception as e:
                # if an exception, just try next PEAR
                continue

    if result is None:
        if problem:
            raise problem

        else:
            raise AttributeError("Unrecognised path: {}".format(path))

    return result

def dispatch(path, key='gets'):
    """  Dispatch a function call """

    # work our way down path looking for a meta data match
    match = meta_data_match(path, key)

    if not match:
        raise AttributeError("Unrecognised path: {}".format(path))

    # unpack match return value
    base = match.base
    target = match.target
    relative_path = match.path

    # extract function to call
    function = get_item(target.get('karma'))

    print("Calling:", target.get('karma'))
    result = function(match)
        
    return result


def get_all_meta_data(path):
    """ Spin along a path gathering up all meta data """
    meta = {}

    fields = path.split('/')
    path = []
    for field in fields:
        path.append(field)

        meta_data = meta.update(
            load_meta_path('/'.join(path)))

    return meta
        
def load_meta_path(path):
    """ Load meta data a path if it exists """
    filename = os.path.join(path, 'meta.json')
    if os.path.exists(filename):
        with open(filename) as infile:
            return json.loads(infile.read())

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

def not_yet_implemented(path):
    
    raise NotImplemented(path)


def create_folder_if_missing(path):
    """ Create a folder 
    
    path is a path to a file, we just want to create
    the base folder if it is missing.
    """
    folder, filename = os.path.split(path)

    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

def full_path(base, path):

    return '/'.join([base, path])

def day_range(start, end):
    """ Generate a range of days 

    yields datetime.date(day) for each day from start to end, 
    excluding end.

    """
    aday = datetime.timedelta(days=1)

    day = start

    while day < end:
        yield day
        day += aday

def load(path):
    """ Read data at path and return a pandas DataFrame 

    For now assumes item at path is a csv file.
    """

    return pandas.read_csv(path)

def save(fptr, df):
    """ Save dataframe df at fptr.

    For now, save as csv.

    FIXME: include meta data for format, or use file extension.
    """

    df.to_csv(fptr, index=False)

@contextmanager
def current_working_directory(path):
    """ Temporarily change working directory """
    cwd = Path.cwd()

    # Change where we are
    os.chdir(path)

    try:
        # yield the path
        yield Path(path)
    finally:
        # change back to where we started
        os.chdir(str(cwd))

