import utime
from machine import Pin, SPI
from mfrc522 import MFRC522

i = 0
led = machine.Pin("LED", machine.Pin.OUT)

writableArray = [8, 9,10,12,13,14,16,17,18,20,21,22,24,25,26,28,29,30,32,33,34,36,37,38,40,41,42,44,45,46,48,49,50,56,57,58,60,61,62]
# rdr = mfrc522.MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)
print(len(writableArray))
while True:
    led.value(1)
    rdr = MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)
    (stat, tag_type) = rdr.request(rdr.REQIDL)

    if stat == rdr.OK:

        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            if rdr.select_tag(raw_uid) == rdr.OK:
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                if rdr.auth(rdr.AUTHENT1B, writableArray[i], key, raw_uid) == rdr.OK:
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

                    stat = rdr.write(writableArray[i], b'25-'+dayS + monthS + str(utime.localtime()[0])[-2:] + "-" + hourS  + minuteS +  secondS)
                    #print(i , "-", stat , "-" , rdr.OK)

                    
                    if stat == rdr.OK:
                        print("written  ", writableArray[i])
                        if i == (len(writableArray) - 1):
                            i = 0
                        else:
                            i = i + 1
                        led.off()
                        led.on()
                    else:
                        print("failed  ", writableArray[i])
                        if i == (len(writableArray) - 1):
                            i = 0
                        else:
                            i = i + 1
                        led.off()
                        utime.sleep(0.1)
                        led.on()
                        utime.sleep(0.1)
                        led.off()
                        utime.sleep(0.1)
                        led.on()
                        utime.sleep(0.1)
                else:
                    print("failed auth ", writableArray[i])
                    if i == (len(writableArray) - 1):
                        i = 0
                    else:
                        i = i + 1
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)
                rdr.stop_crypto1()
    #utime.sleep(0.1)





