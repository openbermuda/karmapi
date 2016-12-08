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
import time

import pandas
fft = pandas.np.fft

from karmapi import flash

BASE_FOLDER = '.'

PEARS = []
PEAR = None

def config(path):
    """ Process configurarion data """
    data = json.load(path.open())
    
    if 'pears' in data:
        PEARS = data['pears']
        PEAR = PEARS[0]

class Parms:

    def __init__(self, data=None):

        if data:
            self.__dict__.update(data)

    def update(self, data):

        self.__dict__.update(data)

    def get(self, parm):
        """ Return parm or None if id does not exist """

        return self.__dict__.get(parm)

def find_path(path, paths):
    """ Find first matching path in paths 

    Paths is a dictionary.

    The values are dictionaries too, with a path key.
    """
    for key, target in paths.items():

        parms = match_path(path, Path(target['path']))

        if parms:
            parms.update(dict(target=target))
            return parms

    return False

CASTS = dict(int=int, float=float)


def match_path(path, target_path):
    """ See if path matches target """
    
    fields = path.parts
    target_fields = target_path.parts

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

    folders = list(path.parts)
    print(folders)
    bases = []
    relatives = folders[1:]
    
    for folder in folders:
        bases.append(folder)
    
        base = Path(*bases)
        relative_path = Path(*relatives)
        
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
    return dispatch(Path(path), key='builds')

def get(path):
    """ Get data for a path """
    print("GET:", path)
    print("CWD:", os.getcwd())
    result = None
    problem = None
    path = Path(path)
    
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

    fields = Path(path).parts
    path = []
    for field in fields:
        path.append(field)

        meta_data = meta.update(
            load_meta_path(Path(*path)))

    return meta

def meta(path):
    """ Return meta data for path """
    path = Path(path)
    if path.is_dir():
        # try adding meta.json
        path = path / 'meta.json'

    if (not path.exists()):
        # see if a peer has it
        got = try_pear(path)

        if not got:
            raise AttributeError("Unrecognised path: {}".format(path))
        
    with path.open() as infile:
        return json.load(infile)

def save_meta(path, meta):
    """ Save meta data at path """
    path = Path(path)
    
    if path.is_dir():
        path = path / 'meta.json'
    
    with (path).open('w') as outfile:
        json.dump(meta, outfile, indent=2, sort_keys=True)

def build_from_meta(path):
    """Build item at path using meta data 

    The idea here is to build something we just give the path.

    Meta data is read and fingers crossed it has enough information
    for the thing to build itself.

    All this does is finds a function or method to call and calls it
    with the path.

    The meta data will likely get re-read when the thing gets called
    -- we could pass it on, but this approach means all builders need
    to be given is a path.

    """
    meta = Parms(get_all_meta_data(path.parent))

    # extract function to call
    function = get_item(target.get('karma'))

    print("Calling:", target.get('karma'))
    result = function(path)
        
    return result
    
        
def load_meta_path(path):
    """ Load meta data a path if it exists """
    filename = path / 'meta.json'

    if filename.exists():
        with filename.open() as infile:
            return json.loads(infile.read())

    # return empty dictionary if there is no meta data here
    return {}

def get_item(path, module=None):
    """ Given a path, return the item

    Note that path here is a dotted module path per python import.

    Item is usually some sort of python callable.

    It could be a function or a class name.
    """
    path = path.split('.')

    if module is None:
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
    path = Path(path)
    folder = path.parent

    folder.mkdir(parents=True, exist_ok=True)


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

def raw_read(path):

    return path.open('r').read()

        
READERS = dict(
    csv=pandas.read_csv,
    hdf=pandas.read_hdf,
    raw=raw_read)

def save_csv(path, df):
    """ Save dataframe as csv """
    df.to_csv(str(path), index=False)

WRITERS = dict(
    csv=save_csv,
    hdf=flash.save_hdf)    

def try_pear(path):
    """ Try and get data for path from a peer """
    if PEAR is None:
        return None

    return PEAR.mirror(path)
    

def load(path):
    """ Read data at path and return a pandas DataFrame 

    For now assumes item at path is a csv file.

    If pear is True then try and get from a pear if it
    is missing
    """
    path = Path(path)
    meta = get_all_meta_data(path)

    if (not path.exists()):
        # see if a peer has it
        got = try_pear(path)

        if not got:
            raise AttributeError("Unrecognised path: {}".format(path))

    form = meta.get('format', 'csv')
    
    reader = READERS.get(form)
    df = reader(str(path))

    return df

def save(path, df, exist_ok=True, mkdirs=True):
    """ Save dataframe df at path.

    Reads meta data and if it finds a format attribute
    uses a writer for the given format.

    See also load.
    """
    path = Path(path)
    
    # create folder if we have been asked to
    if mkdirs:
        path.parent.mkdir(exist_ok=exist_ok, parents=True)

    # load meta data to find format to save with
    meta = get_all_meta_data(path)

    form = meta.get('format', 'csv')

    # get the writer to use
    writer = WRITERS.get(form)

    # do the write
    writer(path, df)


def sono(xx, window=None):
    """ Return sonogram of xx """

    n = len(xx)

    if window is None:
        window = 128

    kk = len(xx) - window

    result = []
    for yy in range(kk):

        result.append(fft.fft(xx[yy:yy+window]))
    
    return result


def isono(xx, points=None, k=24):

    if points is None:
        points = set(range(1, k))
    
    vfft = fft.fft(xx)

    for x in range(1, int(len(vfft)/2)):
        if x not in points:
            vfft[x] = 0
            vfft[-x] = 0

    iso = fft.ifft(vfft)

    xdf = pandas.DataFrame(dict(value=xx))

    xdf['fit'] = iso.real

    xdf['delta'] = xdf.value - xdf.fit

    return xdf


def update_meta(path, data):
    """ Update meta data at path with new data """

    m = meta(path)
    
    m.update(data)

    base.save_meta(path, m)


@contextmanager
def current_working_directory(path):
    """ Temporarily change working directory """
    cwd = Path.cwd()

    # Change where we are
    os.chdir(str(path))

    try:
        # yield the path
        yield Path(path)
    finally:
        # change back to where we started
        os.chdir(str(cwd))

class Timer:

    def __init__(self):

        self.tt = []
        self.tags = []

    def time(self, tag=None):
        """ Take a time snap shot """
        self.tt.append(time.time())
        self.tags.append(tag)

    def stats(self):
        """ Generate timing stats """

        stats = {}

        now = None
        for ix, (stamp, tag) in enumerate(zip(self.tt, self.tags)):
            if now is not None:
                if tag is None:
                    tag = 't{}'.format(ix)
                    
                stats[tag] = stamp - now
                
            now = stamp

        stats['total'] = self.tt[-1] - self.tt[0]

        return stats
