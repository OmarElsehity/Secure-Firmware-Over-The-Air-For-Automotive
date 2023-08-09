
/*******Author Emad Heikal & Omar Elsehity *
******* Sponsered by Swift ACT
*/
/* Includes ------------------------------------------------------------------*/
#include "main.h"

#define MSET_BIT(var, bit)   var |=  (1 << (bit))
#define CLR_BIT(var, bit)   var &= ~(1 << (bit))
#define TOG_BIT(var, bit)   var ^=  (1 << (bit))
#define GET_BIT(var, bit)   ((var >> bit) & 1)



/* Declaring SRAM sections */

volatile  unsigned long int  vctTable[500]__attribute__((__section__(".VCTORTABLE_")))={0};
volatile unsigned short int Code[100]={0};

/* Declaring variables */

#define _10_Secs 																12500
#define _15_Secs																18750
#define _20_Secs																25000

static uint8_t EOC=0; 											/* end of code boolean*/
static uint32_t CodeAddress= 0x08000000;
static uint32_t StartAddress= 0x08000000;
typedef void (*Function_t)(void);
Function_t addr_to_call = 0;
char CheckOnce=0;
char VersionNumber=0;
char StatusRequest=0;
char CAN_MX_Received=0;
static uint32_t CodeArea1=0x08002000; 
static uint32_t CodeArea2=0x08008A00;

/* Function Prototypes */

uint8_t AsciToHex(uint8_t Copy_u8Asci);
uint8_t ParseDatafromRecord(volatile unsigned char* Copy_u8BufData);
void func(void);
void BOOTLOADER_RAM(uint32_t  Copy_u32EraseAddress , uint16_t * Copy_u16WriteAddress, uint16_t  Copy_u16Data);
void JumpCodeArea(void);
void CopyVectorTableIntoRAM();
static unsigned char  x;


/* Private variables ---------------------------------------------------------*/
CAN_HandleTypeDef hcan;


/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_CAN_Init(void);
void FPEC_Init(void);
static inline __attribute__((always_inline)) void __DISABLE_IRQ(void);
static inline __attribute__((always_inline)) void __ENABLE_IRQ(void);
/* Private user code ---------------------------------------------------------*/

// Initialize Tx and Rx Headers
CAN_RxHeaderTypeDef RxHeader;
CAN_TxHeaderTypeDef TxHeader;

// Initialize Tx and Rx Buffers
uint8_t TxData[8] = {0};

static uint8_t RxData[8];

// TxMailbox used to store the Tx message
uint32_t TxMailbox;

// To count can frames (8 bytes at a time)
volatile int FrameNumber = 0;
volatile char FullRecordFlag=0;
unsigned char EOR_A=0; // end of record flag;
unsigned char EOR_B=0; // end of record flag;
volatile unsigned char index=0; 



/**
 * @brief  The application entry point.
 * @retval int
 */
// A Record of Received Data
volatile unsigned char Data_Record_A[60]={0} ;
volatile unsigned char Data_Record_B[60]={0} ;


int main(void)
{
	uint32_t it=0;
	unsigned char CharacterCount=0;
	
	CopyVectorTableIntoRAM();

	/* MCU Configuration--------------------------------------------------------*/

	/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
	HAL_Init();

	/* Configure the system clock */
	SystemClock_Config();

	/* Initialize all configured peripherals */
	MX_GPIO_Init();
	MX_CAN_Init();

	/* Initialize the CAN */
	HAL_CAN_Start(&hcan);
	
	// Initialize TxHeader
	TxHeader.DLC = 8;  // data length
	TxHeader.IDE = CAN_ID_STD;
	TxHeader.RTR = CAN_RTR_DATA;
	TxHeader.StdId = 0x104;  // ID
	
	// Activate the notification
	HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO0_MSG_PENDING);

	uint32_t start_time = HAL_GetTick(); // Get current time in ms
  while (HAL_GetTick() - start_time < _20_Secs){
		if( *((uint16_t*)CodeArea2) != 0xFFFF){ // checking if there is code in this erea
			StartAddress= CodeArea2;
			JumpCodeArea();
		}
		if(CAN_MX_Received==1){
			break;
		}
	}; // Wait until time elaps
	
	if (CAN_MX_Received==0){ // time passed and nothing happened
		if( *((uint16_t*)CodeArea2) != 0xFFFF){ // checking if there is code in this erea
			StartAddress= CodeArea2;
			JumpCodeArea();
		}
		else if (*((uint16_t*)CodeArea1) != 0xFFFF){
			StartAddress= CodeArea1;
			JumpCodeArea();
		}
		else{
			//JumpCodeArea();
		}
		
	}
	while(1){
		if(StatusRequest==1){
			uint8_t *ptr=(uint8_t*)0x0800FC00;
			for(char temp;temp <8;temp++){
			TxData[temp] = ptr[temp];
			}
			HAL_CAN_AddTxMessage(&hcan, &TxHeader, TxData, &TxMailbox);
			StatusRequest=0;
		}
		if (FullRecordFlag==1){
			if(EOR_A==1){
				CharacterCount = ParseDatafromRecord(Data_Record_A);
				
				for (int i=0;i<(CharacterCount/2);i++){
					BOOTLOADER_RAM(0,(uint16_t*)(CodeAddress),Code[i]);
					CodeAddress+=0x2;
				}
			}
			
			if(EOR_B==1){
				CharacterCount = ParseDatafromRecord(Data_Record_B);
				
				for (int i=0;i<(CharacterCount/2);i++){
					BOOTLOADER_RAM(0,(uint16_t*)(CodeAddress),Code[i]);
					CodeAddress+=0x2;
				}
			}
			FullRecordFlag=0;
		}
		if(EOC==1){
		//	JumpCodeArea();
		}
	}		
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief CAN Initialization Function
  * @param None
  * @retval None
  */
static void MX_CAN_Init(void)
{

  /* USER CODE BEGIN CAN_Init 0 */

  /* USER CODE END CAN_Init 0 */

  /* USER CODE BEGIN CAN_Init 1 */

  /* USER CODE END CAN_Init 1 */
  hcan.Instance = CAN1;
  hcan.Init.Prescaler = 1;
  hcan.Init.Mode = CAN_MODE_NORMAL;
  hcan.Init.SyncJumpWidth = CAN_SJW_1TQ;
  hcan.Init.TimeSeg1 = CAN_BS1_13TQ;
  hcan.Init.TimeSeg2 = CAN_BS2_2TQ;
  hcan.Init.TimeTriggeredMode = DISABLE;
  hcan.Init.AutoBusOff = DISABLE;
  hcan.Init.AutoWakeUp = DISABLE;
  hcan.Init.AutoRetransmission = DISABLE;
  hcan.Init.ReceiveFifoLocked = DISABLE;
  hcan.Init.TransmitFifoPriority = DISABLE;
  if (HAL_CAN_Init(&hcan) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN CAN_Init 2 */

	CAN_FilterTypeDef canfilterconfig;

	canfilterconfig.FilterActivation = CAN_FILTER_ENABLE;
	canfilterconfig.FilterBank = 7;  // which filter bank to use from the assigned ones
	canfilterconfig.FilterFIFOAssignment = CAN_FILTER_FIFO0;
	canfilterconfig.FilterIdHigh = 0x103<<5;
	canfilterconfig.FilterIdLow = 0;
	canfilterconfig.FilterMaskIdHigh = 0x103<<5;
	canfilterconfig.FilterMaskIdLow = 0x0000;
	canfilterconfig.FilterMode = CAN_FILTERMODE_IDMASK;
	canfilterconfig.FilterScale = CAN_FILTERSCALE_32BIT;
	canfilterconfig.SlaveStartFilterBank = 0;  // doesn't matter in single can controllers

	HAL_CAN_ConfigFilter(&hcan, &canfilterconfig);

  /* USER CODE END CAN_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
void FPEC_Init(void){
MSET_BIT(*((uint32_t*)(0x40021000 + 0x14))  , 4);
}
/*disable all interrupts*/
static inline __attribute__((always_inline)) void __DISABLE_IRQ(void)
{__asm volatile("CPSID i");}
/*enable all interrupts*/
static inline __attribute__((always_inline)) void __ENABLE_IRQ(void)
{__asm volatile("CPSIE i");}
	
#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

__attribute__((__section__(".myramfunction")))
void BOOTLOADER_RAM(uint32_t  Copy_u32EraseAddress , uint16_t * Copy_u16WriteAddress, uint16_t  Copy_u16Data){ /* missing logic law aktar men page bass mashy l7ad delwa2ty */
#define FLASH_ACR						*((volatile uint32_t * ) (0x40022000 ))
#define FLASH_KEYR          *((volatile uint32_t * ) (0x40022004 ))
#define FLASH_OPTKEYR       *((volatile uint32_t * ) (0x40022008 ))
#define FLASH_SR            *((volatile uint32_t * ) (0x4002200c ))
#define FLASH_CR            *((volatile uint32_t * ) (0x40022010 ))
#define FLASH_AR            *((volatile uint32_t * ) (0x40022014 ))
#define FLASH_OBR           *((volatile uint32_t * ) (0x4002201c ))
#define FLASH_WRPR          *((volatile uint32_t * ) (0x40022020 ))


/*void FPEC_voidFlashPageErase(uint32_t Copy_u32EraseAddress)*/

/*void FPEC_voidUnlockFlashMemory(void)*/

	if( GET_BIT(FLASH_CR, 7) == 1 ){
		FLASH_KEYR = 0x45670123;
		FLASH_KEYR = 0xCDEF89AB;
	}
	if(Copy_u32EraseAddress !=0){
		
		CLR_BIT(FLASH_CR,0); 									/* disabling flash prog  bit */
		while (GET_BIT(FLASH_SR ,0) == 1);			/* busy wait untill the FPEC is free (not busy) */
		SET_BIT(FLASH_CR ,1); 									/* page erase is set */
		FLASH_AR = Copy_u32EraseAddress ;
		SET_BIT(FLASH_CR ,6); 									/* start erasing */
		while (GET_BIT(FLASH_SR ,0) == 1); 			/* busy wait untill the FPEC is free (not busy) */
	}
	if(Copy_u16WriteAddress != 0){
		
		CLR_BIT(FLASH_CR,1); 					/* disabling erasing bit */
		SET_BIT(FLASH_CR,0); 						/* start programing  */
		/*SET_BIT(FLASH_ACR,3); // to set a half word writing mode ( recommended by datasheet)*/
		while (GET_BIT(FLASH_SR ,0) == 1); /* busy wait untill the FPEC is free (not busy) */
		*(Copy_u16WriteAddress )= Copy_u16Data ;			
		}
}
uint8_t AsciToHex(uint8_t Copy_u8Asci)
{
	volatile uint8_t Result;
	if ( (Copy_u8Asci >= 48) && (Copy_u8Asci <= 57) )
	{
		Result = Copy_u8Asci - 48;
	}

	else
	{
		Result = Copy_u8Asci - 55;
	}

	return Result;
}


uint8_t ParseDatafromRecord(volatile unsigned char* Copy_u8BufData){
	
   /* in this fuction we parse through the hex file and take the necessary data and send it to the FPEC to burn it into flash 
	* Input : hex file 
	* Output : Record Flash CodeAddress ; Record Data ; record data Character count or record CC /2 for FPEC
	*/

	volatile uint8_t DigitLow,DigitHigh,CC,i;
	uint8_t DataDigit0,DataDigit1,DataDigit2,DataDigit3;
	uint8_t DataCounter = 0;
	
	
	/* Copy_u8BufData[0] is : 
	
	* Getting Character Count  from BufData[1] and BufData[2] */

	DigitHigh = AsciToHex (Copy_u8BufData[1]);
	DigitLow  = AsciToHex (Copy_u8BufData[2]);
	CC        = (DigitHigh<<4) | DigitLow ;

	/* Getting the CodeAddress */
	
	DataDigit0 = AsciToHex (Copy_u8BufData[3]);
	DataDigit1 = AsciToHex (Copy_u8BufData[4]);
	DataDigit2 = AsciToHex (Copy_u8BufData[5]);
	DataDigit3 = AsciToHex (Copy_u8BufData[6]);
	
	/* Flash memory range is from 0x800 0000 to 0x800 FFFF (64KB)
	
	 * Clearing the  lower  part of the CodeAddress 			   */
	if(AsciToHex (Copy_u8BufData[8])== 4){ /* EXtended address (higher part of base address) */
		/* this is the first record */
		/*
		CodeAddress = CodeAddress & 0xFFFF0000;
		CodeAddress = CodeAddress | (DataDigit3) | (DataDigit2 << 4) | (DataDigit1 << 8) | (DataDigit0<<12);*/
		CC=0;
	}
	else{
		
		CodeAddress = CodeAddress & 0xFF000000;
		CodeAddress = CodeAddress | (DataDigit3) | (DataDigit2 << 4) | (DataDigit1 << 8) | (DataDigit0<<12);
		
		/* from Bufdata[9] to Bufdata[(cc+9)] */
		
		/* Writing in flash through FPEC is done 16 bits or 2 bytes at a time 
		* So looping over 2 bytes in each iteration 
		* for saving digits in data array
		* EX: C943 is 2 bytes if saved in little endian would be 43C9
		* or (4)<<12 | (3)<< 8 | (c) << 4 | (9) 
		*/
		if (CheckOnce==0){
			StartAddress=CodeAddress;
			if(CodeAddress>= 0x08008A00){
				
				for(uint32_t temp=0x08008A00;temp<0x0800FC00;temp+=0x400){
					BOOTLOADER_RAM(temp,0,0);
					}
			
			}
			else if(CodeAddress< 0x08008A00){
			
				for(uint32_t temp=0x08002000;temp<0x08008A00;temp+=0x400){
					BOOTLOADER_RAM(temp,0,0);
					}
			}
			CheckOnce=1;
		}
		
		for (i=0;i<CC/2; i++)
		{
			DataDigit0 = AsciToHex (Copy_u8BufData[4*i+9 ]); 
			DataDigit1 = AsciToHex (Copy_u8BufData[4*i+10]);
			DataDigit2 = AsciToHex (Copy_u8BufData[4*i+11]);
			DataDigit3 = AsciToHex (Copy_u8BufData[4*i+12]);
			
			Code[DataCounter] = (DataDigit3 << 8) | (DataDigit2 << 12) | (DataDigit1) | (DataDigit0<<4);
			DataCounter++;
		}

	}
	if(AsciToHex (Copy_u8BufData[8])== 1){
		EOC=1;
		if(StartAddress< 0x08008A00){
			BOOTLOADER_RAM(0,(uint16_t *)0x0800FC00,VersionNumber);
	
		}else if(StartAddress< 0x08008A00){
			BOOTLOADER_RAM(0,(uint16_t *)0x0800FC02,VersionNumber);
		}
	}
	return CC;
}

void JumpCodeArea(void){
			__asm volatile ("cpsid i" );
    	addr_to_call = (*(Function_t*)(StartAddress+4));
			addr_to_call();
	
}
/**
 * CAN RX1 Interrupt
 */
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
	
	// Receive the message in Rx Header
	HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData);
	if (RxData[0]=='S' &&RxData[1]=='T' &&RxData[2]=='A' &&RxData[3]=='T' &&RxData[4]=='U' &&RxData[5]=='S' ){
		StatusRequest=1;
	}
	else if (RxData[0]=='V' &&RxData[1]=='e' &&RxData[2]=='r' &&RxData[3]==':'){
		VersionNumber=AsciToHex(RxData[4]);
		CAN_MX_Received=1;
	}
	else{
		for(char i=0;i<8;i++){
			if(EOR_A ==0){
				Data_Record_A[index]= RxData[i];
				index++;
				if(RxData[i]=='\n'){
					EOR_A=1;
					EOR_B=0;
					index=0;
					FullRecordFlag=1;
					i++;
					
				}
			}
			if(i>7) break;
			if(EOR_A ==1){
				Data_Record_B[index]= RxData[i];
				index++;
				if(RxData[i]=='\n'){
					EOR_A=0;
					EOR_B=1;
					index=0;
					FullRecordFlag=1;
					
					
				}
			}
			if(i>7) break;

		}
	}
}
void CopyVectorTableIntoRAM(){
	
	*(uint32_t *)(0xE000ED08)= 0x08000000; 
	uint32_t *VTOR_ptr =(uint32_t*)(0x08000000);
	
	__asm volatile ("cpsid i" );

	for(unsigned int M=0;	M<500;M++){										
  	vctTable[M] =	VTOR_ptr[M];
	}
	*(uint32_t *)(0xE000ED08)= 0x20004000; 
	__asm volatile ("cpsie i" );
	
}


