#include <stdint.h>

#define GREEN_ON	0X00000200 //
 #define GREEN_OFF	0x02000000 //
 #define BLUE_ON	0x00000100 //
 #define BLUE_OFF	0x01000000 //
 
 void MasterClockInit(void);
void uart_portSetup(void);
	void uart_send_message(uint16_t v);
	char uart_receive_message(void);
	void print_str(char * message);
	void action2(char v);
	void newline(void);
	void set_incoming_letter(char c);
	void send_diffrent_char(void);
	void delay(uint32_t count);
	void cml_control(void);

