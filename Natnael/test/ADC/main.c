#include "stm32f10x.h"                  // Device header
#include "custom_header.h"

int main()
{
	 MasterClockInit();
	 portClockInt();
	 portSetup();
	LDC_ports();
	LCD_INIT();
		ADCPortsetup();
	GPIOA->BSRR = LED1_OFF|LED2_OFF|LED3_OFF|LED4_OFF;
//	while(1)
//	{
//		
//		string_LCD();
//	}
	
		while(1)
	{
		//switchbutton_vs_LED_1_to_1();
		convertohex(1);
		commandToLCD(LCD_LN1);
//		if((GPIOA->IDR & GPIO_IDR_IDR6) == 0)
//		{
//		convertohex(1);
//		commandToLCD(LCD_LN1);
//		}
//		else if((GPIOA->IDR & GPIO_IDR_IDR7) == 0)
//		{
//				convertohex(0); 
//			commandToLCD(LCD_LN1);
//		}
//		else
//		{
//			commandToLCD(LCD_LN1);
//		}
		
		
		
	}
	
}