# IDPA-Landrunner
[Pamasol Willi Mäder AG](https://www.pamasol.com/) has specialised in the development and production of solutions for aerosols and spray systems since 1965. 

Its Automatiker Lehrlinge (German for “mechatronic apprentices”) go through a 4-year apprenticeship. They get an on the job training by qualified Pamasol employees and go to college one or two days per week.

Apprentices can optionally add BMS (Berufsmaturitätschule) to their school experience, which qualifies students for higher education after the apprenticeship. To pass the BMS every student has, among other tests, to perform a IDPA or written-out **I**nter**d**isziplinäre **P**rojekt**a**rbeit (German for “interdisciplinary project work”). In this case the student programmed a game called Landrunner.

> Landrunner is programmed in [Python](https://www.python.org/) and it runs on a [Raspberry Pi 3](https://www.raspberrypi.org/) which is connected to a joystick and a screen.

![Landrunner animation](doc/landrunner_animation.gif)


## How to install on a PC with Windows 10 operating system

1. You'll need to install Python 3.7+ (other versions of Pyhton could also work).  Download and install Python from [python.org/downloads](https://www.python.org/downloads/). Open a terminal (for example [cmd](https://en.wikipedia.org/wiki/Cmd.exe)) and check if Python is installed correctly with command `python --version`. You should get an output like *Python 3.8.2*.

2. Install [Virtualenvwrapper for Windows](https://github.com/davidmarble/virtualenvwrapper-win/) via pip package-manager: `pip install virtualenvwrapper-win`.

> Virtualenvwrapper for Windows is a tool for creating isolated virtual python environments.

3. Create a new virtual enviroment: `mkvirtualenv -p 3 landrunner`

4. Run `workon landrunner` in cmd. As soon as console switched to the virtual enviroment, you should get a command line like *(landrunner) C:\repos\IDPA-Landrunner>*.

> Please note: *virtualenvwrapper-win* commands only work in the regular command prompt cmd. They will not work in Powershell. When you are in [Visual Studio Code](https://code.visualstudio.com/) terminal for example, run `cmd /k workon landrunner`.

5. Clone this repository with `git clone https://github.com/pamasol/IDPA-Landrunner.git` and navigate into the project folder with `cd IDPA-Landrunner`.

6. In the virtual enviroment, install dependencies with `pip install -r requirements.txt`.

7. Run the script with `python landrunner.py`. As soon as it is started press **space key** and enjoy!


## How to install on a Raspberry Pi 3
1. You'll need to install Raspbian Buster with desktop and recommended software on your RaspberryPi (it was tested with the Raspbian Version September 2019 and a RaspberryPi 3 B+). Download and install Raspbian from [raspberrypi.org/downloads/raspbian](https://www.raspberrypi.org/downloads/raspbian/).

2. After installing Raspbian clone this repository on to your RaspberryPi with `git clone https://github.com/pamasol/IDPA-Landrunner.git` and navigate into the folder with `cd IDPA-Landrunner`. 

3. The requirements should already be installed within Raspbian. If not, install depencies with `pip install -r requirements.txt`.

4. To run the game at the startup of the RasperryPi, you'll need to edit the bash.rc file. Open a terminal and type ` sudo nano /home/pi/.bashrc`. Go to the last line of the script and add 
`echo Running at boot`
`sudo python /home/pi/sample.py`. For more Help visit [dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/). I used the second method of this tutorial.

5. Now your RasperryPi should be ready to go. Restart the Pi and the game should start. 


## Documentation

This project is well documented in German language. See [IDPA_Dokumentation_Marvin_Bueeler.pdf](doc/IDPA_Dokumentation_Marvin_Bueeler.pdf) for more information.
