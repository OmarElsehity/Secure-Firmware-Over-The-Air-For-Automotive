![SFOTA_Sequence](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/d058c625-1c47-4687-b33d-528926621a4b)# Secure-Firmware-Over-The-Air
Developing a system that updates the vehicle’s firmware through Wi-Fi, using Raspberry Pi 4 to connect with the server, and download and decrypt the firmware files. The system is designed to use two STM32F103 each connected to the CAN bus. The Pi sends the update package to the target ECU over MCP2515 then a custom Bootloader flashes the firmware into the memory. All the process is monitored through a custom-built infotainment system presented on a 7-inch touch LCD to manage user interactions.

                                                   Infotainment System:
                                                   
![GUI_Dark](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/04321e98-5e83-40d1-ae43-871a3d372d2b)


                                                     SFOTA Overview 

![SFOTA Poster](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/9b20712d-a8c3-4d37-a342-18afe1f2d786)
    

-> System Block Diagram:

![Blank diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/d9d8b0aa-5a0d-4105-8775-40571a3df725)


-> Project Design:
This section includes the main features of the project
1. System checks for new updates
2. Request update package
3. Download the update package
4. Installation

![Screenshot (72)](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/49a31ebe-f44e-4fee-a66e-3bcd8c2d0056)
 

-> System Flowchart:

![Grad Flow Chart](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/f4012d5c-93ea-4e95-84f4-228c27ec2d83)


-> System Sequence Diagram:

![SFOTA_Sequence](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/ae3e8564-04ea-40c6-9af0-f11a2afdeec4)


-> Schematic Diagrams:

![Schematic_SFOTA](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/06b221cb-8824-4789-832b-d6383c55796b)

-> Simplified Schematic Diagram:

![Schematic Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/1d1297fa-0a09-492e-85df-eab430b91b8f)


(Demo Video) 
https://drive.google.com/file/d/1c6D5XZydFfNlUuPHIVN9cETH1KwaFffO/view?usp=drive_link

