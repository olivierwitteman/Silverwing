from Companion import Companion

if __name__ == '__main__':

    companion = Companion(useBeagleBone=False, useMAVLink=False)
    companion.start()

    while (1):
        try:
            continue
        except KeyboardInterrupt:
            print("Exiting")
            companion.stop()
            exit()
