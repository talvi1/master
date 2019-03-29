 #include "stm32f1xx_hal.h"
 #include "uart.h"
 #include "string.h"
 #include <stdio.h>
 #include <stdbool.h>
	
  extern UART_HandleTypeDef huart2;	
  extern UART_HandleTypeDef huart1;	
	char incoming_letter;
	bool stop_dump = true;
	bool new_char;
	char incoming_letter;
 
 
/*
Function: uart_send_message
		    send bytes using USART
				waits for the buffer to load;
Parameters:
	uint8_t v = input byte;
Returns:
	N/A

*/

void uart_send_message(uint8_t *v, uint8_t length)
{
	
	HAL_UART_Transmit(&huart1,(uint8_t *)v, length, 1000);
	
}

/*
Function: uart_receive_message
		    receive bytes using USART
				waits for the buffer to load;
Parameters:
	uint8_t r = input byte;
Returns:
	N/A

*/

void uart_receive_message(uint8_t *r, uint8_t length){
	
	 HAL_UART_Receive(&huart1,(uint8_t *)r, length, 1000);

}



	




