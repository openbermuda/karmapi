======
 Help
======

tankrain
========

Browse photos in yyyy/mm/dd folders.

Today::

  tankrain karmapi/camera


yyyy/mm/dd::

  tankrain karmapi/camera --date yyyy/mm/dd


Current folder (assuming has yyyy/mm/dd structure)::


  tankrain .


blume
=====

View csv files::


  blume karmapi/sensehat/2017/11/20


Make a gif from a bunch of images
=================================

To convert a bunch of image files to a gif:


    convert image.jpg image2.jpg image.gif


Copying files from another machine
==================================

rsync is a magic program to sync files.

For example::

    rsync -va pi@pipost:karmapi/camera/  karmapi/camera/


Cron tasks on the pi
====================

Look in /etc/cron.d

Entry for taking pictures is /etc/cron.d/veyes
