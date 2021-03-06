import delta_sm3300 as d
delta = d.DeltaComm()
import time

delta.set_voltage(0.1)
delta.set_current(0.1)
delta.set_state(1)

delta.enable_watchdog()

print(delta.ask_watchdog())
time.sleep(6)

delta.set_state(0)
delta.close_connection()
