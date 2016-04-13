=======
 TO DO
=======


Documented but missing
======================

yosser
======

stats
=====

get, build, pear gets and builds should be fixed to save stats on how
long they took, how much disk they used and more.  Bandwidth usage
would be good to know too.

Meta data
=========

Having this in a separate tree would make it easier to manage with
git. 

Byte size
=========

Things that are good to have, not much work.

Rename weather to globe
-----------------------

yosser
------

path suffixes
-------------

With the following path:

  locations/bermuda/time/1979,11,05,photo.png

if we can split off the suffix then we can use that to determine what
type of thing to return.

In a jupyter python shell you could then do:


   >>> show(get("locations/bermuda/time/1979,11,05,photo.png)")

   
and an image of the photo-radiation (sunlight), for 5th November 1979
would pop up.

