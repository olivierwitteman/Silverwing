# S01_Companion

## How to run
Start running the Companion software by executing either:
- `python3 __main__.py` in the `companion` folder.
- `python3 companion` in the `/home/debian` folder.
    
    
    
## Class descriptions
- `Companion`. The highest class. Initializes all sensor threads and MAVLink communication. `__main__.py` start all
initialized threads of the `Companion` by calling the `run()` method.

- `AbstractThread` takes a `buffer` object and a port name to which the sensor is attached.
It handles the loop that periodically reads the sensor, puts the values in the buffer, and also logs them.
When defining a new Thread class that inherits from abstractThread, the user has to implement as specific 
`openInterface()` and `read()` function that works with the sensor.

- `AbstractInMessage`. When a ...`Thread` reads from the sensor interface using `read()` , it returns a `Message`. A `Message`
contains a list of `Parameter` objects. Each `Parameter` object represents a certain type of data
read from the sensor, and includes the name, unit and value. E.g., an `Aeroprobe` messages 
contains the Parameters 'Airspeed', 'Indicated Airspeed' and 'Angle of Attack' (and more).
When defining a new `InMessage` class that inherits from `AbstractInMessage`, the user needs to define the function
`_setParameters`, which converts the raw data from the sensor interface (port) to (a list of) parameters.

- `AbstractBuffer`. The buffer stores data read from the sensor, and has a thread that sends the data over MAVLink at
a defined frequency `sendFrequency` (Defined in `Companion.py`).
When defining a new `Buffer` that inherits from `AbstractBuffer`, the user has to define a length (how many parameters
the buffer holds), a function `addMessage(Message)` that copies the values from a `Message` into the buffer, and a function
`toMavlinkMessage()`, which puts the buffer values into the MAVLink message of that sensor.

- `MavlinkReceiverThread`. This thread receives all incoming MAVLink messages from the Pixhawk and handles them accordingly.

- `Logger`. The logger gets called in a sensor thread. Every time `__main__.py` is executed, the logger makes a new file for each
sensor thread. Each message read by the sensor thread is stored in its log file. The log files can be found in `Companion/logger/logs`.

## I want to change (minor) stuff

- Adjust what sensors to use:\
    In `Companion.py` comment/uncomment initialization functions.
- Adjust whether MAVLink with the Pixhawk is used:\
    In `__main__.py` set `UseMAVLink==false` in the `Companion` constructor.
- Adjust or check sensor ports:\
    In `Companion.py` the sensor ports can be found in the initialize() function belonging to each sensor.
    Google the BeagleBone Black pinout to find out what is where.
- Adjust or check out the frequency at which a sensor sends to MAVLink:\
    In `Companion.py` the frequencies can be found in the initialize() function belonging to each sensor. The
    frequency is defined in the respective `Buffer` constructor function as the variable `sendFrequency`.
    This is in Hz. Note, for the sensors that read out analog ports or GPIOs, the port
    is read out at the same frequency as the buffer frequency.
- Adjust which sensor values are printed to the screen.\
    In the `AbstractThread.py` in `run()` adjust the condition that comes before the
    `print(message.ToString())` function. (Or comment it out, whatever floats your boat).
- I have a MAVLink message coming from the Pixhawk that needs to do something.\
Check out `mavLink/MavLinkReceiverThread.py`. Add an extra statement with the name of your 
MAVLink message, and call the relevant function from there.
    
    