import mfrc522
from os import uname
import utime


def RUN():
    print("Init. " + str(uname()[0]))

    rdr = mfrc522.MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)

    print("")
    print("Place card before reader. WRITE ADDR: 0x08")
    print("")

    try:
        while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("CARD DETECTED")
                    print(" -  TAG TYPE : 0x%02x" % tag_type)
                    print(" -  UID      : 0x%02x%02x%02x%02x" %
                        (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

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
                                print("DATA WRITTEN TO ADDRESS 0x07")
                            else:
                                print("FAILED")
                        else:
                            print("AUTH ERR")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("EXITING PROGRAM")

if __name__=="__main__":
	RUN()

