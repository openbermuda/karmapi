""" 

If a karma pi does not have the data it is asked for it has a
couple of choices.

If it has the stuff needed to build it then it can do just that.

If there is another karma pi that already has t he data it can just
ask for a copy,

So any karma pi can have one or more peers that it gets and shares
data with.

These things tend to come in pairs.

So we have peer and pair, so lets call it pear.
"""
from requests import get, put


class Pear:

    def __init__(self, url=None):

        self.url = url

    def get(self, path):

        return get(self.url + path).json()

    def put(self, path):

        return put(self.url + path).json()
    
