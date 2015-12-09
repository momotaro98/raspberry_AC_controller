# raspberry_AC_controller

This is an air conditioning infrared remote controller with Raspberry Pi.

## Prepairation
#### Raspbian Setting
```
# apt-get install lirc
# echo "dtoverlay=lirc-rpi, gpio_in_pin=24, gpio_out_pin=25" >> /boot/config.txt
```

## Init Setting
fix `config.py`
```
Class Config:
    CONTROLLER_NAME = 'Panasonic'
    SIGNALS = {'stop': 'stop', 'warm': 'warm', 'cool': 'cool'}
```
