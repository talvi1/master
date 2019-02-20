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
	uint16_t v = input byte;
Returns:
	N/A

*/
void uart_send_message(char v)
{
	uint8_t data_t[1];
	data_t[0] = v;
	HAL_UART_Transmit(&huart2,(uint8_t *)data_t, 1, 10000);
	
}

void uart_send_int(uint8_t v)
{
	uint8_t data_t[1];
	data_t[0] = v;
	HAL_UART_Transmit(&huart2,(uint8_t *)data_t, 1, 10000);
	
}


/*
Function: print_str
		   used to send multiple chars.
			print on byte at time.
Parameters:
	char * message = pointer to the char array location 
Returns:
	N/A

*/
void print_str(char * message)
	{
		int i=0;
		uint16_t messagelength = strlen(message);
		for ( i=0; i< messagelength; i++)
		{ 
			uart_send_message(*message);
			message++;
		}
		
}
	

/*
Function: print_str
		   used to send multiple chars.
			print on byte at time.
Parameters:
	char * message = pointer to the char array location 
Returns:
	N/A

*/
void send_arr(uint8_t *data_array, int size)
	{
		int i=0;
		//uint16_t messagelength = strlen(message);
		for ( i=0; i< size; i++)
		{ 
			uart_send_message(*data_array);
			data_array++;
		}
		
}
void print_arr(uint8_t *data_array, int size)
{
	
	for(int i = 0; i < size; i++)
	{
		
	}
	
}

	
void uart_send_xbee_message(uint8_t *v, uint16_t length)
{
	
	HAL_UART_Transmit(&huart1,(uint8_t *)v, length, 1000);
	
}
/*
Function: print_str
		   used to send multiple chars.
			print on byte at time.
Parameters:
	char * message = pointer to the char array location 
Returns:
	N/A

*/
void send_int(uint8_t *data_array, int size)
	{
		int i=0;
		//uint16_t messagelength = strlen(message);
		for ( i=0; i< size; i++)
		{ 
			uart_send_int(*data_array);
			data_array++;
		}
		
}



