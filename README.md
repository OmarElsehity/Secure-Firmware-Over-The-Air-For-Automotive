# Secure-Firmware-Over-The-Air
Developing a system that updates the vehicle’s firmware through Wi-Fi, using Raspberry Pi 4 to connect with the server, and download and decrypt the firmware files. The system is designed to use two STM32F103 each connected to the CAN bus. The Pi sends the update package to the target ECU over MCP2515 then a custom Bootloader flashes the firmware into the memory. All the process is monitored through a custom-built infotainment system presented on a 7-inch touch LCD to manage user interactions.

                                                                Infotainment System:

![SFOTA GUI](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/c0243bae-486e-4b4d-83a8-ab2ac9bfd7d1)
![GUI_Dark](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/98567d3e-7f96-4610-b32f-3358e1e81eda)

                                                                SFOTA Overview 

![SFOTA](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/5e2e7ece-3630-4ccb-a8eb-5a210c82d095)

-> System Block Diagram:

![System Block Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/5f277fed-5f9e-4d2b-b13d-5803653795af)

-> Project Design:
This section includes the main features of the project
1. System checks for new updates
2. Request update package
3. Download the update package
4. Installation
   
![System Flow Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/cff67405-6e74-4f57-a5fd-ad5f7cbdbfb4)


-> System Flowchart:

![System Flowchart](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/ef1594b6-129f-49bd-9d07-d3e23142c944)


-> System Sequence Diagram:

![System Sequence Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/add731cc-b050-48ab-b05b-5c59ecd14cfb)


-> Schematic Diagrams:

![Schematic Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/34615517-c311-4e58-bb46-798d67fcb31b)

-> Simplified Schematic Diagram:

![Simplified Schematic Diagram](https://github.com/OmarElsehity/Secure-Firmware-Over-The-Air/assets/79268813/4e5a893b-6179-4ffa-918d-30a9ed703d61)

(Demo Video) 
https://drive.google.com/file/d/1c6D5XZydFfNlUuPHIVN9cETH1KwaFffO/view?usp=drive_link

