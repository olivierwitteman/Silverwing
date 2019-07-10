import socket
import time


class DeltaComm:

    def __init__(self):
        self.IP = "192.168.2.17"  # Assigned IP to Delta SM3300
        self.PORT = 8462  # Fixed port on Delta SM3300
        try:
            self.open_connection()
        except socket.error:
            # self.IP = "192.168.2.86"
            self.IP = "192.168.2.96"
            self.open_connection()
        # self.set_method()

    def open_connection(self):
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.settimeout(10) # 10 second timeout on commands
        self.srvsock.connect((self.IP, self.PORT))

    def close_connection(self):
        # self.set_method('Local')
        self.set_state(0)
        self.srvsock.close()

    def send(self, message):
        self.srvsock.send(message)

    def set_state(self, state):
        msg = "OUTP "+ str(state) + "\n"
        self.send(msg.encode('ascii'))
        print('State set to {!s}'.format(bool(self.ask_state())))

    def ask_state(self):
        self.send(b"OUTP?\n")
        state = float(self.srvsock.recv(4096))
        return state

    def ask_voltage(self):
        self.send(b"MEASure:VOLtage?\n")
        initvoltage = self.srvsock.recv(4096)
        voltage = float(initvoltage)
        return voltage

    def ask_current(self):
        self.send(b"MEASure:CURrent?\n")
        current = float(self.srvsock.recv(4096))
        return current

    def ask_power(self):
        self.send(b"MEASure:POWer?\n")
        power = float(self.srvsock.recv(4096))
        return power

    def set_current(self, current):
        self.send(str.encode("SOURce:CURrent " + str(current) +"\n"))

    def last_current(self):
        self.send(b"SOURce:CURrent?\n")
        last_current = float(self.srvsock.recv(4096))
        return last_current

    def set_voltage(self, voltage):
        self.send(str.encode("SOURce:VOLtage " + str(voltage) + "\n"))

    def last_voltage(self):
        self.send(b"SOURce:VOLtage?\n")
        last_voltage = float(self.srvsock.recv(4096))
        return last_voltage

    def delta_current(self):
        self.dcurrent = abs(abs(self.current)-abs(self.ask_current()))
        if self.dcurrent < 0.01:
            self.dcurrent = 0.01
        else:
            pass
        return self.dcurrent

    def discharge(self, current, minvolt, mincurrent):
        setcurrent = current
        self.current = abs(current)
        print('discharge')
        self.set_voltage(self.ask_voltage())
        step = 0.1
        try:
            while current < 0 and mincurrent < 0 and -20. <= self.temp <= 60.:
                try:
                    self.plot()
                    if self.series*minvolt < self.ask_voltage() <= self.series*4.3:
                        self.set_state(1)
                        voltage = self.ask_voltage()
                        if self.ask_current() >= current:
                            self.set_voltage(voltage-step*self.delta_current())
                            print("check: ", self.delta_current())
                            time.sleep(0.001*self.series)
                        elif self.ask_current() < current:
                            self.set_voltage(voltage+step*self.delta_current())
                            time.sleep(0.001*self.series)
                    elif self.ask_voltage() <= self.series*minvolt:
                        self.set_state(1)
                        while self.ask_current() < mincurrent and -20. <= self.temp <= 60.:
                            self.set_voltage(self.series*minvolt)
                            self.data_aq("discharge")
                            self.plot()
                        self.set_state(0)
                        print('Battery is empty')
                        current = 0
                except socket.timeout:
                    self.open_connection()
        finally:
            self.set_state(0)
            self.finalplot(setcurrent)
            self.finalsave('discharge')
            avgvolt = float(sum(self.vlst)/len(self.vlst))
            print("temperature (C): {!s}".format(self.temp))
            print("Capacity (Ah): {!s}".format(round(self.caplst[-1], 2)))
            print("Average Voltage (V): {!s}".format(round(avgvolt, 2)))

        print("temperature (C): ", self.temp)

    def sink(self):
        self.send(str.encode("SYSTem:POWersink present?\n"))
        response = self.srvsock.recv(4096)
        return response

    def set_method(self, method='Remote'):  # 'Remote' or 'Local'
        self.send(str.encode("SYSTem:REMote:CV[:STAtus] {!s}\n".format(method)))
        self.send(str.encode("SYSTem:REMote:CC[:STAtus] {!s}\n".format(method)))
        print('Method set to {!s}'.format(method))

    def ask_method(self):
        self.send(str.encode("SYSTem:REMote:CV[:STAtus]?\n"))
        cv_method = self.srvsock.recv(4096)
        print(cv_method)
        self.send(str.encode("SYSTem:REMote:CC[:STAtus]?\n"))
        cc_method = self.srvsock.recv(4096)
        return cv_method, cc_method

    def enable_watchdog(self):
        timeout = 5000
        msg = 'SYSTem: COMmunicate:WATchdog SET,{!s}\n'.format(timeout)
        self.send(msg.encode('ascii'))
        print('Watchdog set with timeout of {!s}s'.format(round(timeout/1000.), 2))

    def ask_watchdog(self):
        self.send(str.encode("SYSTem: COMmunicate:WATchdog SET?\n"))
        cv_method = self.srvsock.recv(4096)
        print(cv_method)
