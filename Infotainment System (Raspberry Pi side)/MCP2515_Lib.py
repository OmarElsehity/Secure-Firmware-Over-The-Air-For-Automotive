import spidev
import RPi.GPIO as GPIO

# Initialize SPI device
spi = spidev.SpiDev()
spi.open(0, 0) # (bus, device)

# Set SPI mode and speed
spi.mode = 0
spi.max_speed_hz = 50000 # 1MHz
# set up GPIO for CS
#GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)  # CS0
GPIO.output(8, GPIO.HIGH)


################# VARIABLES ##############

arr=(0x68,0x65,0x6c,0x6c,0x6f,0x31,0x32,0x33)
ID=-1 
 
rx=0 
data_length=0 
## Control registers 
CANSTAT = 0x0E 
CANCTRL = 0x0F  
CNF1 = 0x2A  
CNF2 = 0x29  
CNF3 = 0x28  
CANINTE  = 0x2B
CANINTF  = 0x2C 
TXB0CTRL = 0x30 
TXB1CTRL = 0x40 
TXB2CTRL = 0x50 
RXB0CTRL = 0x60 
RXB1CTRL = 0x70 

## TX buffer 
TXB0SIDH = 0x31  
TXB0SIDL = 0x32  
TXB0DLC  = 0x35  
TXB0D0   = 0x36  ## TXB0D0+1 = TXB0D1 ,TXB0D0+2 = TXB0D2 etc.. 
 
## RX buffer 0 
RXB0SIDH = 0x61  
RXB0SIDL = 0x62  
RXB0DLC  = 0x65  
RXB0D0   = 0x66  ## RXB0D0+1 = RXB0D1 ,RXB0D0+2 = RXB0D2 etc.. 
## RX buffer 1 
RXB1SIDH = 0x71  
RXB1SIDL = 0x72  
RXB1DLC  = 0x75  
RXB1D0   = 0x76  ## RXB1D0+1 = RXB1D1 ,RXB1D0+2 = RXB1D2 etc.. 
 
## Instructions el mohemin 
Write_inst = 0x02  
Reset_inst = 0xC0  
Read_inst  = 0x03  
Bit_Modify_inst = 0x05  
READ_RX_BUFFER = 0x90   ## buffer 0 =READ_RX_BUFFER +2  buffer 1 =READ_RX_BUFFER +6   
# function definitions
def MCP2515_Write_instruction(Address ,data ):
    GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
    spi.xfer([Write_inst])  ## Send write command 
    spi.xfer([Address])  ## Send register address 
    spi.xfer([data])  ## Send data 
    GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module 

def MCP2515_Read_Byte_instruction( Address ): ## not tested 
    dummy_data =0x00  
    Rx_data =0 
    GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
    spi.xfer([Read_inst])  ## Send read command 
    spi.xfer([Address])  ## Send register address 
    Rx_data=spi.xfer([dummy_data])  ## receive data 
    GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module 
    return Rx_data  

def MCP2515_StartTransmission_instruction( Buffer_number ):
    if (Buffer_number ==0): 
        GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
        spi.xfer([0x81])  ## Send register address 
        GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module   
    elif (Buffer_number ==1): 
        GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
        spi.xfer([0x82])  ## Send register address 
        GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module   
    elif (Buffer_number ==2): 
        GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
        spi.xfer([0x84])  ## Send register address 
        GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module   

def MCP2515_ConfigurationMode(): ##  SOF bit time w 7agat keda 
    MCP2515_Write_instruction(CANCTRL ,0x80)  

def MCP2515_NormalMode():
    MCP2515_Write_instruction(CANCTRL ,0x00)  

def MCP2515_SleepMode():
    MCP2515_Write_instruction(CANCTRL ,0x20)  

def MCP2515_Reset(): 
    GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
    spi.xfer([Reset_inst])  
    GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module  
 
def MCP2515_CANInit(): 
    MCP2515_Write_instruction(CNF1 ,0x00)  
    MCP2515_Write_instruction(CNF2 ,0x91)   
    MCP2515_Write_instruction(CNF3 ,0x01)  
 
def MCP2515_BitModify( Address , Mask, Data ): ##not tested 
    GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
    spi.xfer([Bit_Modify_inst])  ## Send command 
    spi.xfer([Address])  ## Send Address 
    spi.xfer([Mask])  ## Send mask 
    spi.xfer([Data])  ## Send data 
    GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module 
 
def MCP2515_SetPriorityHigh(Buffer): 
    if(Buffer==0): 
        MCP2515_BitModify(TXB0CTRL,0x03,0x03)  
  
def MCP2515_SetID(ID): ## tested and working 
    IDHigh = (ID >>3) & 0xff  
    IDLow =  (ID <<5) & 0xff 
    MCP2515_Write_instruction(TXB0SIDH,IDHigh)  
    MCP2515_Write_instruction(TXB0SIDL,IDLow)  

def MCP2515_SetDataLength(Length): ## tested and working 
    if(Length>8):
        Length=8  
    MCP2515_Write_instruction(TXB0DLC,Length)  

def MCP2515_LoadData(offset , data ):## tested and working 
    MCP2515_Write_instruction(TXB0D0+offset, data)  

def MCP2515_OneShotMode(): ## tested and working 
    MCP2515_Write_instruction(CANCTRL ,0x08)  
  
def MCP2515_StopTransmission(): ## msh sha8al 
    MCP2515_Write_instruction(TXB0CTRL,0)  
 
 
def MCP2515_Configure_Rx_Buffers(): ## working but not fully tested 
    MCP2515_Write_instruction(RXB0CTRL,0x64) ## RXB0 masks or filters are off and roll over is allowed 
    MCP2515_Write_instruction(RXB1CTRL,0x60) ## RXB0 masks or filters are off and roll over is allowed 
 
def MCP2515_Get_RXB0_ID (): ## tested and working 
    SIDLow = 0  
    SIDHigh= 0  
    ID=0  
    SIDHigh = MCP2515_Read_Byte_instruction(RXB0SIDH)  
    SIDLow  = MCP2515_Read_Byte_instruction(RXB0SIDL)
    SIDHigh = (SIDHigh[0] <<3)  
    SIDLow = (SIDLow[0]>>5) 
    ID= SIDHigh | SIDLow  
    return ID  

def MCP2515_Get_RXB1_ID (): ## not tested 
    SIDLow = 0  
    SIDHigh= 0  
    ID=0  
    SIDHigh = MCP2515_Read_Byte_instruction(RXB1SIDH)  
    SIDLow  = MCP2515_Read_Byte_instruction(RXB1SIDL)  
    SIDHigh = (SIDHigh[0] <<3)  
    SIDLow = (SIDLow[0]>>5)  
    ID= SIDHigh | SIDLow  
    return ID  
 
def MCP2515_Get_RXB0_Data_Length (): ##tested and working 
    Data_size=0  
    Data_size = MCP2515_Read_Byte_instruction(RXB0DLC)  
    Data_size = (Data_size[0] & 0x0F)  
    if(Data_size>8): 
        Data_size=0  
    return Data_size    
 
def MCP2515_Get_RXB1_Data_Length (): ##/ tested and working 
    Data_size=0  
    Data_size = MCP2515_Read_Byte_instruction(RXB1DLC)  
    Data_size = (Data_size[0] & 0x0F)  
    if(Data_size>8): 
        Data_size=0  
    return Data_size    

def MCP2515_Read_RXBuffer0_byte(): ## tested and working 
    DataLength=0
    RX=[]
    DataLength = MCP2515_Get_RXB1_Data_Length()  
    GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
   
    spi.xfer([READ_RX_BUFFER+2])  ## Send command 
    for i in range(DataLength):
        receive= spi.xfer([0x00])[0]
        RX.append ( chr(receive) ) ## receive data  

    GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module
    return RX

def MCP2515_Read_RXBuffer1_byte(): ## tested and working 
    DataLength=0  
    DataLength = MCP2515_Get_RXB1_Data_Length()
    RX_2 =[]
    GPIO.output(8, GPIO.LOW)  ## Select MCP2515 module 
   
    spi.xfer([READ_RX_BUFFER+6])  ## Send command 
    for i in range(DataLength):
        RX_2.append (spi.xfer([0x00]))  ## receive data   
   
    GPIO.output(8, GPIO.HIGH)  ## Deselect MCP2515 module 
    return RX_2   
   
def MCP2515_Message_RxBuffer0_Flag():## tested and working 
    check=0  
    check = MCP2515_Read_Byte_instruction(CANINTF)  
    check = (check[0] & 0x01)  ## first bit 
    if(check ==1):
        return True  
    else: 
        return False  
  
 
def MCP2515_Message_RxBuffer1_Flag():## tested and working 
    check=0  
    check = MCP2515_Read_Byte_instruction(CANINTF)  
    check = (check[0] & 0x02)  ## first bit 
    if(check == 2): 
        return True   
    else:
        return False  
  

def MCP2515_Set_RxBuffer0_Full_Int():## tested and working 
    MCP2515_BitModify(CANINTE,0x01,0x01)  

def MCP2515_Set_RxBuffer1_Full_Int():## tested and working 
    MCP2515_BitModify(CANINTE,0x02,0x02)  

def ASCII(dec):
    return chr(dec)


