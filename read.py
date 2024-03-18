import mfrc522
from os import uname
from machine import Pin
led = Pin("LED", Pin.OUT)

def RUN():
    print("Init. " + str(uname()[0]))
    led.on()

    rdr = mfrc522.MFRC522(sck=2,miso=4,mosi=7,cs=5,rst=18)

    print("")
    print("Place card before reader. READ ADDR: 0x08")
    print("")

    try:
       while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1B, 1, key, raw_uid) == rdr.OK:
                            #print(rdr.read(8).toString())
                            print(type(rdr.read(1)))
                            this = bytes(rdr.read(1)).hex()
                            print("Address 8 data: %s" % bytes.fromhex(this))
                            rdr.stop_crypto1()
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("EXITING PROGRAM")

if __name__=="__main__":
	RUN()




