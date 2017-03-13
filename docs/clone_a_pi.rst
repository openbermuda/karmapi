=====================
 Cloning Pi SD Cards
=====================

Create a folder, say *piggy* to mount the second partition on the SD
card::

  sudo mount /dev/mmcblk0p2 piggy


Get a local copy of the whole partition::

  sudo rsync -va --delete piggy/ karma_image/


Unmount the card:::

   sudo umount piggy
  

Mount the original image you loaded onto the SD card:
  
First, take a look at the partitions in the image::

   fdisk -lu raspbian.img  
  

Create a devide that mounts the partition directly from the image file::

   sudo losetup /dev/loop0 raspbian_with_pig.img -o $((137216 * 512))

The mysterious 137216 should be the sector at which the partition
starts.  You need to read this from the fdisk output,


Mount the loop device::

    sudo mount /dev/loop0 piggy/


Now sync the copy that you made over to this filesystem::
    

    rsync -va --delete karma_image/p2/ piggy/


Help along the way
==================

Running::

  df

will show you what file systems are currently mounted and where.


Add a *-n* to rsync commands if you want it to just show you what it
will do.

