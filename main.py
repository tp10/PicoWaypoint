import utime
from machine import Pin, SPI
from mfrc522 import MFRC522

led = machine.Pin("LED", machine.Pin.OUT)
green_led = machine.Pin(10, machine.Pin.OUT)
blue_led = machine.Pin(21, machine.Pin.OUT)
buzzer = machine.Pin(17, machine.Pin.OUT)

# rdr = mfrc522.MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)

while True:
    led.value(1)
    blue_led.on()
    buzzer.off()
    rdr = MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            if rdr.select_tag(raw_uid) == rdr.OK:
                print("in here")
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                if rdr.auth(rdr.AUTHENT1B, 25, key, raw_uid) == rdr.OK:
                    month = utime.localtime()[1]
                    day = utime.localtime()[2]
                    hour = utime.localtime()[3]
                    minute = utime.localtime()[4]
                    second = utime.localtime()[5]
                    desired_width = 2
                    monthS = "{:0>{}}".format(month, desired_width)
                    dayS = "{:0>{}}".format(day, desired_width)
                    hourS = "{:0>{}}".format(hour, desired_width)
                    minuteS = "{:0>{}}".format(minute, desired_width)
                    secondS = "{:0>{}}".format(second, desired_width)
                    stat = rdr.write(25, b'25-'+dayS + monthS + str(utime.localtime()[0])[-2:] + "-" + hourS  + minuteS +  secondS)
                    rdr.stop_crypto1()
                    if stat == rdr.OK:

                        led.off()
                        buzzer.on()
                        green_led.on()

                        utime.sleep(0.4)
                        
                        buzzer.off()
                        green_led.off()
                        led.on()
                        
                    else:
                        led.off()
                        utime.sleep(0.1)
                        led.on()
                        utime.sleep(0.1)
                        led.off()
                        utime.sleep(0.1)
                        led.on()
                        utime.sleep(0.1)
                else:
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)

    #utime.sleep(0.5)

