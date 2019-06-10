HOST=198.0.0.250
rsync -avz --exclude "__history" --exclude "*~" --exclude "*.gif" --exclude "*.JPG" -e ssh . pi@$HOST:/home/pi/gears
