# SYSC3010-KoalaTea
3rd year project

Dana Weaver
Hao Tuan Chau
Kevin Ho
Vivian Le

## How to run KoalaTea System:

- get the source code:

`$ git clone https://github.com/danaweaver/SYSC3010-KoalaTea.git`
- Go into the SYSC3010-KoalaTea directory:

`$ cd SYSC3010-KoalaTea`

### Setting up the mobile application:
*Note: Instruction is only for Xcode, Xcode version 9.0.1, React Native version 0.59.4*
- Go into MobileApp folder

`$ cd MobileApp`
- Run command

`$ react-native start`
- Open XCode and choose opening project directory `SYSC3010-KoalaTea/MobileApp`
- Click button Run/Build to run the app on a simulator

### Setting up the DatabaseServer Pi (Raspberry Pi #1):
*Note: Connect the two Pis via ethernet*

- Run the DatabaseServer program:

`$ python DatabaseServer/DatabaseServer.py`

### Setting up the Controller Pi (Raspberry Pi #2):
*Note: Connect the two Pis via ethernet*
- Open SwitchControl.py and change the EMAIL and PASSWORD variables
  to the smart switch login information
- Run the ControllerServer program:

`$ python Controller/ControllerServer.py`

### Setting up the Arduino:
- Setup hardware according to wiring diagram below
- Download and install arduino onto Raspberry Pi #2
- Open up the arduino program
- Run the ino file located in /koalaTeaArduino
![Wiring Diagram](https://raw.githubusercontent.com/danaweaver/SYSC3010-KoalaTea/master/wiringDiagram.png)
