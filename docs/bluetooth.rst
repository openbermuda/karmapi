https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=138145

Followed the following::

  sudo apt-get install bluetooth bluez blueman
  sudo reboot

wait for reboot - The current raspian image does not have native
support for the inbuilt bluetooth on the RPi 3. However if you run::

   hciconfig


It will shows the BD address of the Pi. Run::

     hcitool scan

to get the BD address of the pairable devices in range.

Now to control bluetooth you have to run `bluetoothctl` as the super
user, root::

    sudo bluetoothctl


This brings a command interface with a [bluetooth]# prompt.  At this
prompt::     

    agent on

followed by default-agent

To pair type pair xx:xx:xx:xx:xx:xx where xx:xx:xx:xx:xx:xx is
your BD address of the device you want to pair

Next type::

   trust xx:xx:xx:xx:xx:xx

You can use bluetooth to connect to serial with python so I simply run::
     
  sudo rfcomm bind 0 xx:xx:xx:xx:xx:xx via subprocess.call

to created a serial port.

Make sure to run sudo rfcomm release 0 at the end of the script to
release the serial port



