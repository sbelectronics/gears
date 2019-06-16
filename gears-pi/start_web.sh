#! /bin/bash
cd /home/pi/gears

MICROSTEPS=4
MAXFREQ=1000
STARTUP=
if [ -f /etc/gears/config ]; then
    source /etc/gears/config
fi

/usr/bin/pigpiod || echo "failed to install pgpiod -- already installed?"

nohup python ./web_server.py \
      --microsteps $MICROSTEPS \
      --maxxfreq $MAXFREQ \
      $STARTUP \
      > /tmp/pi-gears.out 2> /tmp/pi-gears.err & 
