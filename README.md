# Secure-Firmware-Over-The-Air
Developing a system that updates the vehicle’s firmware through Wi-Fi, using Raspberry Pi 4 to connect with the server, and download and decrypt the firmware files. The system is designed to use two STM32F103 each connected to the CAN bus. The Pi sends the update package to the target ECU over MCP2515 then a custom Bootloader flashes the firmware into the memory. All the process is monitored through a custom-built infotainment system presented on a 7-inch touch LCD to manage user interactions.

                                                                Infotainment System:

![GUI_Dark](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/98567d3e-7f96-4610-b32f-3358e1e81eda)

                                                                  SFOTA Overview 

                                                                
![SFOTA Poster](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/df5019dd-c95b-4937-881b-f76909021f1d)


-> System Block Diagram:

![Blank diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/fc50b3ff-3bd9-4d54-916e-0fa228e39eab)

-> Project Design:
This section includes the main features of the project
1. System checks for new updates
2. Request update package
3. Download the update package
4. Installation
   
![Screenshot (72)](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/797d3ba1-b843-4fe6-a296-5508cafcffed)


-> System Flowchart:

![Grad Flow Chart](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/71b1a87d-6910-4122-86e1-fef2e2185ad7)


-> System Sequence Diagram:

![SFOTA_Sequence](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/584823f3-0ed3-4e22-af5b-d83695997183)


-> Schematic Diagrams:

![Schematic_SFOTA](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/b641026d-3e15-4886-bcfc-d5c7c1f5509f)

-> Simplified Schematic Diagram:

![Schematic Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/c9079ce9-b062-4f36-9c16-4909bf7140d7)

(Demo Video) 
https://drive.google.com/file/d/1c6D5XZydFfNlUuPHIVN9cETH1KwaFffO/view?usp=drive_link

