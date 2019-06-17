#! /bin/bash
cd /home/pi/gears

MICROSTEPS=4
MAXFREQ=1000
FREQ=100
SHUTDOWN=120
STARTUP=
if [ -f /etc/gears/config ]; then
    source /etc/gears/config
fi

/usr/bin/pigpiod || echo "failed to install pgpiod -- already installed?"

nohup python ./web_server.py \
      --microsteps $MICROSTEPS \
      --maxfreq $MAXFREQ \
      --freq $FREQ \
      --shutdown $SHUTDOWN \
      $STARTUP \
      > /tmp/pi-gears.out 2> /tmp/pi-gears.err & 
