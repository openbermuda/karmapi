"""If a karma pi does not have the data it is asked for it has a
couple of choices.

If it has the stuff needed to build it then it can do just that.

If there is another karma pi that already has the data it can just
ask for a copy,

So any karma pi can have one or more peers that it gets and shares
data with.

These things tend to come in pairs.

So we have peer and pair, so lets call it pear.

For now, Pear's just try to retrieve the thing at path and save it
locally.

"""
from pathlib import Path
import shutil

from requests import get, put

from karmapi import base


class Pear:

    def __init__(self, url):

        self.url = url

    def get(self, path):

        path = Path(path)
        response = get(self.url + path.as_posix() + '.csv')
        if response.status_code != 200:
            raise AttributeError('Status code: {}'.format(
                response.status_code))

        path.write_bytes(response.content)

        return True



class LocalPear:

    def __inti__(self, folder):

        self.folder = Path(folder)

    def get(self, path):

        shutil.copy(str(self.folder / path), str(path))

        


    
