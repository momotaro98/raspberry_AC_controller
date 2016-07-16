# raspberry_AC_controller

This is an air conditioning infrared remote controller Web system on Raspberry Pi.
This system uses Flask Web Framework.

**CAUTION**
This application depends on Python3

## Requirement

### LIRC Setting

#### apt-get install lirc

```
# apt-get install lirc
```

#### fix `/etc/config.txt`

```/boot/config.txt
dtoverlay=lirc-rpi, gpio_in_pin=24, gpio_out_pin=25
```

#### fix `/etc/lirc/hardware.conf`

```/etc/lirc/hardware.conf
LIRCD_ARGS="--uinput"
LOAD_MODULES=true
DRIVER="default"
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"
```

#### generate `/etc/lirc/lircd.conf`
未実装

```
$ python convert.py CONTROLLER_NAME
```


### Application Setting

#### git clone and install required dependencies

```
$ git clone http://
$ pip install -r requirements.txt
```

#### generate `acstate.csv`, `acstate_log.csv`, `reserve_state.csv`, and `reserve_state_log.csv`

```
$ echo "2016-04-01 13:24:00,on,cool,25,auto" >> acstate.csv
$ touch acstate_log.csv
$ echo "2016-04-01 15:30:00,undo,0" >> reserve_state.csv
$ touch reserve_state_log.csv
```

#### fix `config.py` according to `lircd.conf`

set `CONTROLLER_NAME` and `context`

```
class Config:
    CONTROLLER_NAME = '' # You have to set
```



## TEST

```
$ py.test
```
