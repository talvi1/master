
#include "uart.h"
#include "acc.h"
#include "stm32f10x.h"
int main()
{
	//MasterClockInit();
	uart_portSetup();
	spiClock_Port();
	spiINT();
	adxl_write(0xc0, 0x11);
	newline();
	newline();
	print_str("     WELCOME!! \n\n\r");
	newline();
	print_str("CMD>> ");
	
	while(1)
	{
		cml_control();
		//adxl_write(0x55, 0x55);
		//get_device_id();
transfer(0x1212);
		delay2(6000);

		
		//dump_adc();
	}
	
}

/*
Function: USART2_IRQHandler
		USART interrupt
Parameters:
	N/A
Returns:
	N/A

*/
void USART2_IRQHandler()
{
  if(USART2->SR & USART_SR_RXNE)
  {
		char SR = USART2->DR;
//		//action2(USART2->DR);
//		if(SR ==0x1b)
//			//set_stop_bump(true);
		set_incoming_letter(SR);
  }
	
}
