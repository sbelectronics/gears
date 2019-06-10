#! /bin/bash
cd /home/pi/gears


/usr/local/bin/pigpiod || echo "failed to install pgpiod -- already installed?"

nohup python ./web_server.py > /tmp/pi-gears.out 2> /tmp/pi-gears.err & 
