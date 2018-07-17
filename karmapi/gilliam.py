""" The tale of Gilliam and the GILly

So before anyone complains, this all came about because of this:

@freakboy3742 aka Russell Keith-Magee::

   I'm suddenly very disappointed that in all Python's history with the GIL,
   nobody has name.. a GIL-related package GILLIAM.

So here it is.

There's more to the story of course.

The bigger the conference the more likely someone will propose a GILectomy.

It is like Godwin's law, but it ends in surgery.

And the patient awakes, dazed and confused and only three times slower the before surgery.

But low hanging water melons abound so more fun to come.

I must have been using python nearly five years before I was aware of this GIL
thing there.

In DC, 2003 perhaps.

There were these things called threads, they talk to each other.

Actually, mostly they did not do too much talking.  

Most times you used them to do n things at once.

If they can share one processor, then all is good.

Except when it isn't.   Which is mostly when someone tries to talk.

By this time computers came with many cpus.  

So if you had many threads that was just one python process and one cpu.

Much of this code is where humans come in.  Interfaces for humans.

One cpu can keep up with a human.  

So that leaves n-1 to do the fun stuff.

But if you have cool threads then at certain times they grab the GIL.

The Global Interpretter Lock.

The thread with the GIL is the one that can rock.

If it just takes a beat then they all keep up.

So if you are lucky terry will know where he is and what time it is.

And if you ask with or without a flag terry may tell how you are running.

And now for something completely the same? 
"""

import dis
import sys
import datetime

def where():
    return "Sheffield Somewhere"

def when():
    return datetime.datetime.now()


def terry(flag=None):
    """ 
    Am I running in a co-routine?

    Credits: @dabeaz and @yarkot
    """
    flag = flag or 128

    co_flags = sys._getframe(2).f_code.co_flags

    return co_flags & flag


if __name__ == '__main__':

    # A sketch with Terry Gilliam the main character
    print(where())
    print(when())
    print(terry())

