===========
 Sense Hat
===========

If you have a pi with a sense hat then the *karmapi.sense* module
should be of interest.


Crontab
=======

Copy *crontab/sensehat* to */etc/cron.d/sensehat* and it will start a
process (as the pi user) on boot to record data from the sense hat.

You may need to fix the entry to get the path to your python right,
it may not be in the path when cron runs::

    type python3.6

will tell you where it is.

The data is written to *~pi/karmapi/sensehat/yyyy/mm/dd*  folders, one
for each day.


Module Docs
===========

.. automodule:: karmapi.sense
   :members:


      
