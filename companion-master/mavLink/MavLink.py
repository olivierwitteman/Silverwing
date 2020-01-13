import os


class MavLink(object):
    def __init__(self, port=None):
        self._connection = self.connect(port)

    def send(self, mavLinkMessage):
        if (self._connection != None):
            if mavLinkMessage is None:
                print("Mavlink message not sent, Mavlink message is None")
            try:
                self._connection.mav.send(mavLinkMessage)
            except:
                print("MavLink message not sent!")
        else:
            # No connection (i.e., port) indicates a dummy connection.
            pass

    def connect(self, port):
        if (port != None):
            from pymavlink import mavutil

            # Sets up MAVLink 2.0 connection.
            os.environ["MAVLINK20"] = "0"
            mavLinkConnection = mavutil.mavlink_connection(port, baud=921600, dialect="custom_messages")

            # Waits for first heartbeat.
            print("Waiting 5s for heartbeat..")
            if (mavLinkConnection.wait_heartbeat(timeout=5) != None):
                print("Heartbeat from system %d!" % (mavLinkConnection.target_system))
            else:
                print("Error: No heartbeat received! Exiting.")
                mavLinkConnection.close()
                exit()
            return mavLinkConnection
        else:
            # No port indicates a dummy connection.
            return None

    def getConnection(self):
        return self._connection
