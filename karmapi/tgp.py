"""Remember Pretty Good Privacy?

It is still doing the rounds, as gpg and other related projects.

tgp is Total Garbage Passwords.

Don't use this at home.  It is for the times when you are having
trouble satisfying alphabet soup password rules: 

  * Password must contain a letter and number.

  * p4assword must upper and lower case.

  * P4ssword most contain punctuation

P4sswor!

tgp takes a simple word and lightly garbles it.

Great for satisfying password rules, not so great for security and
privacy.

The usage of this would be as follows.

First, create a secure passphrase[1].  Say six words randomly chosen,
for example using diceware:

  http://openbermuda.org/80days/posts/dice-passwords.html

Now when you find out that the passphrase doesn't satisfy the arcane
restrictions on passwords use TGP to generate a random salt that
modifies the phrase.  FIXME: add code to generate random salts.

Now a password manager could save the salts for sites.  All you have
to remember is the passphrase and type that in.  The password manager
does the rest.

This might actually result in a password that is not total garbage
after all.

[1] this is the important bit.
"""

from karmapi import base

class TGP:

    """ A total garbage password """

    def __init__(self, key, parms=None):

        self.keyword = key

        if parms:
            self.salt = string_to_salt(parms.salt)

    def set_salt(self, salt):

        self.salt = string_to_salt(salt)

    def password(self):
        """ Generate password """
        password = ''
        
        salts = self.salt
        short = len(self.keyword) - len(salts)
        if short > 0:
            salts = salts + (['0'] * short)

        for key, salt in zip(self.keyword, salts):
            for pepper in salt:
                key = self.garble(key, pepper)
            password += key

        return password

    def garble(self, key, pepper):

        mappers = dict(n=self.number,
                       u=self.upper,
                       l=self.lower,
                       p=self.punctuation)
    
        try:
            pepper = int(pepper)
            return self.add(key, pepper)
        
        except:
            mapper = mappers.get(pepper)
            if mapper:
                return mapper(key)
            else:
                return key

    def upper(self, key):
        """ Convert key to upper case """
        return key.upper()

    def lower(self, key):
        """ Convert key to lower case """
        return key.lower()

    def punctuation(self, key):
        """ Convert key to punctuation """
        punks = '!@=-+?'

        ix = ord(key)
        
        return punks[ix % len(punks)]

    def add(self, key, pepper):
        """ Assumes key is a lowercase character """
        if key.isdigit():
            return self.iadd(key, pepper)

        if key.isupper():
            ax = ord('A')
        else:
            ax = ord('a')
        
        xkey = ord(key)
        xkey += pepper - ax

        if xkey < 0:
            xkey += 26
        if xkey >= 26:
            xkey -= 26
            
        return chr(xkey + ax)

    def iadd(self, key, pepper):
        """ Assumes key is a digit """
        a0 = ord('0')
        
        xkey = ord(key)
        xkey += pepper - a0

        if xkey < 0:
            xkey += 10
        if xkey >= 10:
            xkey -= 10
            
        return chr(xkey + a0)

    def number(self, key):

        numbers = dict(a=4, e=3, i=1)

        return str(numbers.get(key, '0'))

        

def string_to_salt(fields):

    salt = []
    for field in fields.split(','):
        salt.append(field.split())

    return salt

        
if __name__ == '__main__':

    meta = base.Parms(dict(salt='0, n -1,  0, 0,  0,  u, 3 p'))

    key = input('Enter phrase: ')

    tgp = TGP(key, meta)

    print(tgp.password())
