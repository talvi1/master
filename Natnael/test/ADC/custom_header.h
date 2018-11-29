/******************************************************************************
 * Name:    lab1_lib.h
 * Description: STM32 peripherals initialization
 * Version: V1.00
 * Authors: Dave Duguid / Trevor Douglas
 *
 * This software is supplied "AS IS" without warranties of any kind.
 *
 *
 *----------------------------------------------------------------------------
 * History:
 *          V1.00 Initial Version
 *          V1.1 reformatted (kjn)
 *****************************************************************************/
#include <stdint.h>

 #define LED1_ON	0X02000000 //
 #define LED1_OFF	0x00000200 //
 #define LED2_ON	0x04000000 //
 #define LED2_OFF	0x00000400 //
 
 #define LED3_ON	0X08000000 //
 #define LED3_OFF	0x00000800 //
 #define LED4_ON	0x10000000 //
 #define LED4_OFF	0x00001000 //
 
 //Commands for Hitachi 44780 compatible LCD controllers
#define LCD_8B2L 0x38 // ; Enable 8 bit data, 2 display lines
#define LCD_DCB 0x0F // ; Enable Display, Cursor, Blink
#define LCD_MCR 0x06 // ; Set Move Cursor Right
#define LCD_CLR 0x01 // ; Home and clear LCD
#define LCD_LN1 0x80 // ;Set DDRAM to start of line 1
#define LCD_LN2 0xC0 // ; Set DDRAM to start of line 2


// Control signal manipulation for LCDs on 352/384/387 board
// PB0:RS PB1:ENA PB5:R/W*
#define LCD_CM_ENA 0x00210002 //
#define LCD_CM_DIS 0x00230000 //
#define LCD_DM_ENA 0x00200003 //
#define LCD_DM_DIS 0x00220001 //
 
 
// Initialize the Cortex M3 clock using the RCC registers
  void MasterClockInit(void);
	void portClockInt(void);
	void portSetup(void);
	void delay2(uint32_t TEST);
	void lighton(void);
	void switchbutton_vs_LED_1_to_1(void);
	
	void LDC_ports (void);
	void commandToLCD(uint8_t data);
	void dataToLCD(uint8_t data);
	void LCD_INIT (void);
	void string_LCD(void);
	void ADCPortsetup();
	uint16_t ADC_read(int);
	void convertohex(int);
	
	void SysTick_INT_Ports_value(void);
	void SysTick_INTIT_Ports(void);
	
	
	