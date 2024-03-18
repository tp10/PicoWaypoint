import utime
from machine import Pin, SPI
from mfrc522 import MFRC522

led = machine.Pin("LED", machine.Pin.OUT)


# rdr = mfrc522.MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)

while True:
    led.value(1)
    rdr = MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            if rdr.select_tag(raw_uid) == rdr.OK:
                print("in here")
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                i = 25

                # for i in range(1, 26):
                print(i)
                if rdr.auth(rdr.AUTHENT1B, i, key, raw_uid) == rdr.OK:
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
                    stat = rdr.write(i, b'25-'+dayS + monthS + str(utime.localtime()[0])[-2:] + "-" + hourS  + minuteS +  secondS)
                    stat = rdr.write(i+1, b'25-'+dayS + monthS + str(utime.localtime()[0])[-2:] + "-" + hourS  + minuteS +  secondS)
                    
                    if stat == rdr.OK:
                        print("written 1 ")
                        led.off()
                        utime.sleep(1)
                        led.on()
                    else:
                        print("failed 1 ")
                        led.off()
                        utime.sleep(0.1)
                        led.on()
                        utime.sleep(0.1)
                        led.off()
                        utime.sleep(0.1)
                        led.on()
                        utime.sleep(0.1)
                else:
                    print("failed 2 ")
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)
                rdr.stop_crypto1()
    utime.sleep(1)


