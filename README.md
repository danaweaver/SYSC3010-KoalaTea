# SYSC3010-KoalaTea
3rd year project

Dana Weaver 101000606
Hao Tuan Chau 101000491
Kevin Ho 100997967
Vivian Le 100998809

How to run KoalaTea System:
Setting up the mobile application:
****ADD INSTRUCTIONS HERE*****

Setting up the DatabaseServer Pi:
* Note: Connect the two Pis via ethernet *
- On Raspberry Pi #1, get the source code:
$ git clone https://github.com/danaweaver/SYSC3010-KoalaTea.git
- Go into the SYSC3010-KoalaTea directory:
$ cd SYSC3010-KoalaTea
- Run the DatabaseServer program:
$ python DatabaseServer/DatabaseServer.py

Setting up the Controller Pi:
* Note: Connect the two Pis via ethernet *
- On Raspberry Pi #2, get the source code:
$ git clone https://github.com/danaweaver/SYSC3010-KoalaTea.git
- Go into the SYSC3010-KoalaTea directory:
$ cd SYSC3010-KoalaTea
- Open SwitchControl.py and change the EMAIL and PASSWORD variables
  to the smart switch login information
- Run the ControllerServer program:
$ python Controller/ControllerServer.py

Setting up the Arduino:
- Download and install arduino onto Raspberry Pi #2
- Open up the arduino program
- Run the ino file located in /koalaTeaArduino
