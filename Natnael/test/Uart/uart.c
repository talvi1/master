 #include "uart.h"
 #include "acc.h"
 #include "stm32f10x.h"
 #include "string.h"
 #include <stdio.h>
 #include <stdbool.h>
	 
	char incoming_letter;
	bool stop_dump = true;
	bool new_char;
 
	char incoming_letter;
 
 
 void MasterClockInit(void)
{
		uint32_t temp = 0x00;
    //If you hover over the RCC you can go to the definition and then
    //see it is a structure of all the RCC registers.  Then you can
    //simply assign a value.
    RCC->CFGR = 0x00050002;     // Output PLL/2 as MCO,
                                // PLLMUL X3, PREDIV1 is PLL input

    RCC->CR =  0x01010081;      // Turn on PLL, HSE, HSI

    while (temp != 0x02000000)  // Wait for the PLL to stabilize
    {
        temp = RCC->CR & 0x02000000; //Check to see if the PLL lock bit is set
    }

    
}
	/*
Function: uart_portSetup
		    Enable peripheral clocks for various ports and subsystems
				configure the RX and TX pins. 
				Enable inturupt;
Parameters:
	N/A
Returns:
	N/A

*/
  void uart_portSetup(void)
{
	
		RCC->APB2ENR |= RCC_APB2ENR_AFIOEN | RCC_APB2ENR_IOPAEN | RCC_APB2ENR_IOPCEN;;
 	  RCC->APB1ENR  |= RCC_APB1ENR_USART2EN;
	
		//PB2 Transmiter; Output50MHz, Alternate function output Push-pull
		GPIOA->CRL |= GPIO_CRL_MODE2 | GPIO_CRL_CNF2_1;
		GPIOA->CRL &= ~GPIO_CRL_CNF2_0;
	
		//PB3 Recvier; 00: Input mode , Floating input
		GPIOA->CRL &= ~GPIO_CRL_MODE3 ;
		GPIOA->CRL |= GPIO_CRL_CNF3_0;
	
		//PC8 Transmiter; Output50MHz, Alternate function output Push-pull
		GPIOC->CRH |= GPIO_CRH_MODE9 |GPIO_CRH_MODE8;
		GPIOC->CRH &= ~GPIO_CRH_CNF9 & ~GPIO_CRH_CNF8;
	
	
		USART2->CR1 |= USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
				USART2->BRR |= 0x09c4;
	USART2->CR1  |= USART_CR1_RXNEIE;// UART3 Receive Interrupt Enable.
		
	
     // Enable interrupt fromUSART1(NVIC level) 
   NVIC_EnableIRQ(USART2_IRQn);   
		
}

	 /*
Function: uart_send_message
		    send bytes using USART
				waits for the buffer to load;
Parameters:
	uint16_t v = input byte;
Returns:
	N/A

*/
void uart_send_message(uint16_t v)
{
	while ((USART2->SR & USART_SR_TXE) != USART_SR_TXE)
	{
	}
	USART2->DR = v ;
	
}
/* Creates a new line.*/
void	newline(void)
	{
		uart_send_message('\n');						
		uart_send_message('\r');
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
	
void set_incoming_letter(char c)
{
	incoming_letter = c;
	new_char =true;
}

void UART_Message_Config(uint16_t v)
{
	while ((USART2->SR & USART_SR_TXE) != USART_SR_TXE)
	{
	}
	USART2->DR = v ;
	
	
}
void delay(uint32_t count)
{
    int i=0;
    for(i=0; i< count; ++i)
    {
    }
}

void cml_control(void)
{
	if(new_char == true)
	{
		action2(incoming_letter);
		new_char = false;
	}
}
void light_on(char number, char status)
{
	if (number == '1' && status == 'n')
		GPIOC->BSRR = BLUE_OFF|GREEN_ON;
	else if (number == '2' && status == 'n')
		GPIOC->BSRR = BLUE_ON| GREEN_OFF;
}


void action2(char v)
{
		int const NUM_OF_CHARACTERS = 30;
		static char command[NUM_OF_CHARACTERS] ;
		static int i;
		int a;
		char num[64];
		volatile int temp;

		char back = 0x08;
		if(v== 0x1b)
		{
			stop_dump = true;
			command[0] = '\n';
			command[2] = '\n';
		}

		 if (v!= 0x1b&&v!=0x0d && i<30)
		{
			
			if ((v == 0x08||v == 0x7f) && (i>0))
			{
				
				print_str(&back);
				print_str(" ");
				print_str(&back);
				command[i-1]= '\n';
				i--;
			}
			else if((v != 0x08 &&v != 0x7f))
			{
				command[i]=v;
				print_str(&v);
				i++;
			}
			
		}
		else{
					if ((command[0] =='l' || command[0]=='l')&&(command[3]!='\n'))
						light_on(command[3],command[5]);
					
					if ((command[0] =='T' || command[0]=='t')&&(command[0]!='\n'))
					{
						a = 0xc0<<8|0x11;						
						sprintf(num,"%d", a);
						print_str(num);
					}
						if ((command[0]=='h' ||command[0]=='H')&&(command[3]=='P' ||command[3]=='p')&&command[3]!='\n')
					{
						newline();
						print_str("~~~~~~~~~~~~~~~~~~~~~~~~~~~How to~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\r");
						print_str("led <n> on  -> Turns the specified led on. \n\r");
						print_str("led <n> off -> Turns the specified led off.  \n\r");
						print_str("All led on  -> Turns the all led on.  \n\r");
						print_str("All led off -> Turns the all led off.  \n\r");
						newline();
						print_str("thank You for using our service. \n\r");
						newline();
					}
				
					else
					{
						newline();
						
						print_str("CMD>> ");
						i=0;
						memset(command, 0, sizeof(command));
					}
					
					
		}

}
