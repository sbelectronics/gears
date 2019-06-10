# Gears
Scott Baker, http://www.smbaker.com/

This repository holds two related projects. The first is a stepper motor controller using an ATTiny85, and the second is a stepper motor controller using a Raspberry Pi. In either case, drivers from pololu are used. The goal of these projects are to control some toy gears.

## ATTiny85 version

  pb0 - dir
  pb1 - step
  pb2 - sleep
  pb3 - potentiometer
  pb4 - button0
  pb5 - button1

## Raspberry pi version

  GPIO17 - dir
  GPIO18 - step
  GPIO19 - sleep
  
  GPIO23 - Enc_A
  GPIO24 - Enc_B
  GPIO25 - Enc_sw
  GPIO05 - Enc_R
  GPIO06 - Enc_G
  GPIO07 - Enc_Blu
  GPIO13 - Button0
  GPIO19 - Button1

  Note: Board error - Enc_B and Enc_Blu were connected

  auto startup:
  sudo crontab -e
      @reboot bash /home/pi/gears/start_web.sh &> /dev/null   