""" Send messages to your world """

from karmapi import piglet

class Talk(piglet.Docs):

    """ send messages """
    
    def __init__(self, *args):

        super().__init__(*args)

        self.set_text(self.__doc__)
        

    
