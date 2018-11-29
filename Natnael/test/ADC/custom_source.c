 /******************************************************************************
 * Name:    lab1_lib.c
 * Description: STM32 peripherals initialization and functions
 * Version: V1.00
 * Author: Dave Duguid / Trevor Douglas
 *
 * This software is supplied "AS IS" without warranties of any kind.
 *
 *
 *----------------------------------------------------------------------------
 * History:
 *          V1.00 Initial Version
 *          V1.1 reformatted (kjn)
 *****************************************************************************/
 #include "stm32f10x.h"
 #include "custom_header.h"
 #include <cstring>

 void MasterClockInit(void)
{
		uint32_t temp = 0x00;
    //If you hover over the RCC you can go to the definition and then
    //see it is a structure of all the RCC registers.  Then you can
    //simply assign a value.
    RCC->CFGR = 0x07050002;     // Output PLL/2 as MCO,
                                // PLLMUL X3, PREDIV1 is PLL input

    RCC->CR =  0x01010081;      // Turn on PLL, HSE, HSI

    while (temp != 0x02000000)  // Wait for the PLL to stabilize
    {
        temp = RCC->CR & 0x02000000; //Check to see if the PLL lock bit is set
    }

  
		
    
	}


	
	
	void portClockInt(void)
{
	//Enable peripheral clocks for various ports and subsystems
    //Bit 4: Port C Bit3: Port B Bit 2: Port A
    RCC->APB2ENR |=  RCC_APB2ENR_IOPCEN | RCC_APB2ENR_IOPBEN
        | RCC_APB2ENR_IOPAEN | RCC_APB2ENR_ADC1EN ;
	
	
}

void portSetup(void)
{
	// Write a 0xB ( 1011b ) into the configuration and mode bits for PA8 (AFIO)
    GPIOA->CRH |= GPIO_CRH_MODE9 | GPIO_CRH_MODE10 | GPIO_CRH_MODE11 | GPIO_CRH_MODE12  ;
    GPIOA->CRH &= ~GPIO_CRH_CNF9 & ~GPIO_CRH_CNF10 & ~GPIO_CRH_CNF11 & ~GPIO_CRH_CNF12 ;
	
		
	  
	
}
void delay2(uint32_t count)
{
    int i=0;
    for(i=0; i< count; ++i)
    {
    }
}



void switchbutton_vs_LED_1_to_1(void)
{
		int i= 1200000;
		if ((GPIOB->IDR & GPIO_IDR_IDR8) == 0)
    {
			GPIOA->BSRR = LED1_ON ;
			
		}
		else if((GPIOB->IDR & GPIO_IDR_IDR9) == 0)
		{
			GPIOA->BSRR = LED2_ON ;
		}
		else if ((GPIOC->IDR & GPIO_IDR_IDR12) == 0)
    {
			GPIOA->BSRR = LED3_ON ;
			
		}
		else if((GPIOA->IDR & GPIO_IDR_IDR5) == 0)
		{
			GPIOA->BSRR = LED4_ON ;
		}	
		else if((GPIOA->IDR & GPIO_IDR_IDR6) == 0)
		{
			GPIOA->BSRR = LED1_ON|LED2_OFF|LED3_OFF|LED4_OFF;
			delay2(i);
			GPIOA->BSRR = LED1_OFF|LED2_ON|LED3_OFF|LED4_OFF;
			delay2(i);
			GPIOA->BSRR = LED1_OFF|LED2_OFF|LED3_ON|LED4_OFF;
			delay2(i);
			GPIOA->BSRR = LED1_OFF|LED2_OFF|LED3_OFF|LED4_ON;
			delay2(i);
			
		}
		else if((GPIOA->IDR & GPIO_IDR_IDR7) == 0)
		{
			GPIOA->BSRR = LED1_OFF|LED2_OFF|LED3_OFF|LED4_ON;
			delay2(i);
			GPIOA->BSRR = LED1_OFF|LED2_OFF|LED3_ON|LED4_OFF;
			delay2(i);
			GPIOA->BSRR = LED1_OFF|LED2_ON|LED3_OFF|LED4_OFF;
			delay2(i);
			GPIOA->BSRR = LED1_ON|LED2_OFF|LED3_OFF|LED4_OFF;
			delay2(i);		
			
		}
		else
		{
			GPIOA->BSRR = LED1_OFF|LED2_OFF|LED3_OFF|LED4_OFF;
		}
		
	
}

void LDC_ports (void)
{
	GPIOB->CRL |= GPIO_CRL_MODE0 | GPIO_CRL_MODE5 | GPIO_CRL_MODE1;
  GPIOB->CRL &= ~GPIO_CRL_CNF0& ~GPIO_CRL_CNF5 & ~GPIO_CRL_CNF1 ;
	
	GPIOC->CRL |= GPIO_CRL_MODE0 | GPIO_CRL_MODE1 | GPIO_CRL_MODE2 | GPIO_CRL_MODE3| GPIO_CRL_MODE4 | GPIO_CRL_MODE5 | GPIO_CRL_MODE6 | GPIO_CRL_MODE7 ;
  GPIOC->CRL &= ~GPIO_CRL_CNF0& ~GPIO_CRL_CNF1 & ~GPIO_CRL_CNF2 & ~GPIO_CRL_CNF3 & ~GPIO_CRL_CNF4 & ~GPIO_CRL_CNF5 & ~GPIO_CRL_CNF6 & ~GPIO_CRL_CNF7  ;
}

void LCD_INIT ()
{
	delay2(2400000); //Wait for more than 15 ms
	commandToLCD(LCD_8B2L);
	
	delay2(170000);//Wait for more than 4.1 ms
	commandToLCD(LCD_8B2L);
	
	delay2(170000); //Wait for more than 100 탎
	commandToLCD(LCD_8B2L);
	
	delay2(170000); //Wait for more than 37 탎
	commandToLCD(LCD_DCB);
	
	delay2(170000); //Wait for more than 37 탎
	commandToLCD(LCD_MCR);
	
	delay2(170000); //Wait for more than 37 탎
	commandToLCD(LCD_CLR);
	
		delay2(170000); //Wait for more than 37 탎
	commandToLCD(LCD_LN1);
	
	
	
}
void commandToLCD(uint8_t data)
{
	GPIOB->BSRR = LCD_CM_ENA; //RS low, E high
	// GPIOC->ODR = data; //BAD: may affect upper bits on port C
	GPIOC->ODR &= 0xFF00; //GOOD: clears the low bits without affecting high bits
	GPIOC->ODR |= data; //GOOD: only affects lowest 8 bits of Port C
	delay2(8000);
	GPIOB->BSRR = LCD_CM_DIS; //RS low, E low
	delay2(8000);
}

void dataToLCD(uint8_t data)
{
	GPIOB->BSRR = LCD_DM_ENA; //RS low, E high
	// GPIOC->ODR = data; //BAD: may affect upper bits on port C
	GPIOC->ODR &= 0xFF00; //GOOD: clears the low bits without affecting high bits
	GPIOC->ODR |= data; //GOOD: only affects lowest 8 bits of Port C
	delay2(8000);
	GPIOB->BSRR = LCD_DM_DIS; //RS low, E low
	delay2(8000);
}



void string_LCD()

{	
	dataToLCD(0x4e);//N
	 
	dataToLCD(0x41);//A
	dataToLCD(0x54);//T
	dataToLCD(0x4e);//N
	dataToLCD(0x41);//A
	dataToLCD(0x45);//E
	dataToLCD(0x4c);//L
	
	dataToLCD(0x20);//sapce
	
	dataToLCD(0x41);//A
	dataToLCD(0x4c);//L
	dataToLCD(0x45);//E
	dataToLCD(0x4d);//M
	dataToLCD(0x55);//U
		
	
		
	delay2(170000); //Wait for more than 37 탎
	commandToLCD(LCD_LN2);
	
	
	 
	dataToLCD(0x32);//2
	dataToLCD(0x30);//0
	dataToLCD(0x30);//0
	dataToLCD(0x33);//3
	dataToLCD(0x35);//5
	dataToLCD(0x34);//4
	dataToLCD(0x33);//3
	dataToLCD(0x39);//9
	dataToLCD(0x39);//9
	
	dataToLCD(0x20);//sapce
	
	if((GPIOA->IDR & GPIO_IDR_IDR6) == 0)
	{
		dataToLCD(0x31);//0
	}
	else
	{
		dataToLCD(0x30);//0
	}
	if ((GPIOA->IDR & GPIO_IDR_IDR7) == 0)
	{
		dataToLCD(0x31);//0
	}
	else
	{
		dataToLCD(0x30);//0
	}
		if((GPIOC->IDR & GPIO_IDR_IDR10) == 0)
	{
		dataToLCD(0x31);//0
	}
	else
	{
		dataToLCD(0x30);//0
	}
	if ((GPIOC->IDR & GPIO_IDR_IDR11) ==   0)
	{
		dataToLCD(0x31);//0
	}
	else
	{
		dataToLCD(0x30);//0
	}
	commandToLCD(LCD_LN1);
}
void ADCPortsetup()
{
		GPIOA->CRL &= ~GPIO_CRL_MODE1 & ~GPIO_CRL_MODE2  ; //00: Input mode (reset state)
    GPIOA->CRL &= ~GPIO_CRL_CNF1 & ~GPIO_CRL_CNF2  ; //00: Analog mode
		
		
	
	  ADC1->CR2 |= ADC_CR2_ADON | ADC_CR2_CAL ; //1: Enable calibration 1: Enable ADC ON
		
		ADC1->SMPR2 |= ADC_SMPR2_SMP1; //111: 239.5 cycles
		
	//	ADC1->SQR1 |= ADC_SQR1_L_1;  // 2 channel 
	
		
	
		
}


uint16_t ADC_read(int select)
{
	uint16_t data = 0;
	if (select ==0)
	{
		ADC1->SQR3 |= ADC_SQR3_SQ1_0;  //1st conversion in regular sequence
	}
	else 
	{
		ADC1->SQR3 |= ADC_SQR3_SQ1_1;
	}
	ADC1->CR2 |= ADC_CR2_ADON  ; //1: Enable calibration 1: ADC  start conversion
	while( (ADC1->SR & 0x2) !=2)
	{
	}
	data = ADC1->DR;
		return data;
		

}
void convertohex(int select)
{
	char  numbers[6],realtemp[4];
	uint16_t z;
	int x = 0x2;
	int j,i,k;
	int value,printvalue;
	
		z = 0.8*ADC_read(select);
		
	for (j = 0; j < 6; j++)
	{
		uint8_t x = (z & 0xF);
		numbers[j] = x;
		z = (z >>4 );
	
	}
	if (select ==0)
	{
		dataToLCD(0x54);//T
		dataToLCD(0x3d);//=
		dataToLCD(0x30);//0
		dataToLCD(0x78);//x
		k = 2;
	}
	else
	{
		dataToLCD(0x56);//V
	
		dataToLCD(0x3d);//=
		dataToLCD(0x30);//0
		dataToLCD(0x78);//x
		k = 3;
	}
	
	for (i = 2; i >= 0; i--)
	{
		if (numbers[i] <0xa)
		{
			dataToLCD(0x30+numbers[i]);
		}
		else
		{
			dataToLCD(0x41+(numbers[i] - 0xa));
		}
	}
	value = numbers[0] + (numbers[1]*16)+(numbers[2]*16*16) + (numbers[3]*16*16*16);
		
	dataToLCD(0x20);
	for ( i= 0; i<4 ;i++)
	{
		realtemp[i] = value%10; 
		
		value /=10;
	}
	while (k>=0)
	{
		if ((select ==0&&k ==0)||(select ==1&&k ==2))
		{
			dataToLCD(0x2E);//.
		}
		
		
		if (realtemp[k] <0x30)
		{
			dataToLCD(realtemp[k]+0x30);
		}
		else
		{
			dataToLCD(realtemp[k]);
		}
		k--;
	}
	if (select ==0)
	{
		dataToLCD(0xB0);//C
		dataToLCD(0x43);//C
		
	}
	else
	{
		dataToLCD(0x56);//V
	}


	delay2(8000000);
	
	
}
void SysTick_INT_Ports_value(void)
{
	SysTick -> CTRL = 0x00;
	SysTick -> VAL = 0x00;
	SysTick -> LOAD = 0x16E360;
	SysTick -> CTRL = 0x07;
}

void SysTick_INTIT_Ports(void)
{
	RCC->APB2ENR |= RCC_APB2ENR_AFIOEN;
	RCC->APB2ENR |= RCC_APB2ENR_IOPCEN | RCC_APB2ENR_IOPBEN |RCC_APB2ENR_IOPAEN;
	
	GPIOC->CRH |= GPIO_CRH_MODE9 |GPIO_CRH_MODE8;
	GPIOC->CRH &= ~GPIO_CRH_CNF9 & ~GPIO_CRH_CNF8;
	
	AFIO->EXTICR[0] &= ~AFIO_EXTICR1_EXTI0_PA;
	EXTI->IMR |= EXTI_IMR_MR0;
	EXTI->FTSR |= EXTI_FTSR_TR0;
	NVIC->ISER[0] |= NVIC_ISER_SETENA_6;
	
}


