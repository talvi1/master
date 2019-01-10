#include "stm32f10x.h"
#include "acc.h"
#include "uart.h"
#include <stdio.h>

uint16_t SPI_DATA_RECEIVE;
uint16_t get_SPI_DATA_RECEIVE()
{
	return SPI_DATA_RECEIVE;
}
void set_SPI_DATA_RECEIVE(uint16_t v)
{
	SPI_DATA_RECEIVE =v;
}
void spiClock_Port()
{
	RCC->APB2ENR |= RCC_APB2ENR_AFIOEN| RCC_APB2ENR_IOPBEN |  RCC_APB2ENR_IOPAEN;
	RCC->APB1ENR |= RCC_APB1ENR_SPI2EN;
	
	
	GPIOB->CRH |= GPIO_CRH_MODE13| GPIO_CRH_MODE15|GPIO_CRH_CNF13_1 | GPIO_CRH_CNF15_1; //MODEy 11: Output mode, max speed 50 MHz.
	GPIOB->CRH &= ~GPIO_CRH_CNF15_0 & ~GPIO_CRH_CNF13_0; 																//CNFy 10: Alternate function output Push-pull
	
	//MISO
	GPIOB->CRH &= ~GPIO_CRH_MODE14 & ~GPIO_CRH_CNF14_1;   //inputmode
	GPIOB->CRH |= GPIO_CRH_CNF14_0;                       //Floating input
	
	//Chip slelect
	GPIOB->CRH |= GPIO_CRH_MODE12;    //Output 50Mhz
	GPIOB->CRH &= ~GPIO_CRH_CNF12;    //General Purpose output push-pull
	
	//Port PB12 -  CS
	//     PB13 -  CLK  - CLOCK
	//     PB14 -  MISO - Recive
	//     PB15 -  MOSI - Transmit
	
	
}

void spiINT()
{
	SPI2->CR2 |= 0x00;   
	
	SPI2->CR1 |= SPI_CR1_SSM;
	SPI2->CR1 |= SPI_CR1_SSI;
	SPI2->CR1 |= SPI_CR1_MSTR;
	SPI2->CR1 |= SPI_CR1_SPE;
	
	SPI2->CR1 |= SPI_CR1_BR_1;   //24Mhz / 8
	
	//SPI1->CR1 &= ~SPI_CR1_CPHA;
	//SPI1->CR1 &= ~SPI_CR1_CPOL;
	
	SPI2->CR1 |= SPI_CR1_DFF ;/*!< Data Frame Format */
	//SPI1->CR1 &= ~SPI_CR1_LSBFIRST;///*!< Frame Format */ 0: MSB transmitted first
	GPIOB->BSRR |= 0x1FFF;
}




void delay2(uint32_t count)
{
    int i=0;
    for(i=0; i< count; ++i)
    {
    }
}
void start()
{
	GPIOB->BSRR |= GPIO_BSRR_BR12;
}
void stop()
{
	GPIOB->BSRR |= GPIO_BSRR_BS12;
}

void spi_send(uint16_t s)
{
	while ((SPI2->SR & SPI_SR_TXE) != 0x2)
	{
	}
	SPI2->DR = s ;
}
void spi_recive()
{
	uint16_t r;
	while ((SPI2->SR & SPI_SR_RXNE) != 0x1)
	{
	}
	r = SPI2->DR;
	SPI_DATA_RECEIVE = r;
}

uint16_t acc_data(void)
{
	
	while ((SPI2->SR & SPI_SR_RXNE) != 0x1)
	{
	}
	return SPI2->DR;
	
}

void adxl_write(uint8_t reg, uint8_t value)
{
	char num[16];
	uint8_t data[2];
	uint16_t write;
	data[0] = reg;
	data[1] = value;
	
	
	write = data[0]<<8 | data[1];
	sprintf(num,"%d", write);
	print_str(num);
	newline();
	start();
	spi_send(write);
	spi_recive();
	stop();
	
}
uint16_t adxl_read(uint8_t reg, uint8_t value)
{
		char num[16];
		uint8_t data[2];
		uint16_t read,acc;
		data[0] = reg ;
		data[1] = value;
	
		read = data[0]<<8 | data[1];
		sprintf(num,"%d", read);
		print_str(num);
		start();
		spi_send(read);
		acc = acc_data();
		stop();	
	
		sprintf(num,"%d", acc);
		print_str("Read value ");
		print_str(num);
		delay(1000000);
		newline();
}
void get_device_id()
{
		char num[16];
		uint16_t acc;
	
		start();
		spi_send(0x8000);
		while ((SPI2->SR & SPI_SR_RXNE) != 0x1)
		{
		}
		acc = SPI2->DR;
		stop();
		
		
}
void transfer(uint16_t v)
{
	uint16_t z;
	
	start();
	spi_send(v);
	while ((SPI2->SR & SPI_SR_RXNE) != 0x1)
	{
	}
	z = SPI2->DR;
	
	stop();
	
}

void adxl_powerOn()
{
	
}
void accINIT()
{
	
}


