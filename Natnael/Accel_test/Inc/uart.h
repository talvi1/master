#include <stdint.h>

#define GREEN_ON	0X00000200 //
 #define GREEN_OFF	0x02000000 //
 #define BLUE_ON	0x00000100 //
 #define BLUE_OFF	0x01000000 //
 
	
	void uart_send_message(char v);
	char uart_receive_message(void);
	void print_str(char * message);
	void send_int(uint8_t *data_array, int size);
	void uart_send_int(uint8_t v);
	void print_arr(uint8_t *data_array, int size);
