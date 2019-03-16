#include "accel_i2c.h"
#include "MPU6050.h"
#include "uart.h"
#include <stdio.h>

uint8_t MPU6050_Init(I2C_HandleTypeDef* I2C)
{
	
	uint8_t var;
	uint8_t who_am_i = 0x75;
	I2C_HandleTypeDef* handle = I2C;
	uint8_t address = 0xD0;
	uint8_t d[2], d1[2];
	d[0] = 0x6B;
	d[1] = 0x0;
	if(HAL_I2C_IsDeviceReady(handle, address, 2, 5) != HAL_OK)
	{
		return 0x01;
	}
	if(HAL_I2C_Master_Transmit(handle, address, &who_am_i, 1, 1000) != HAL_OK)
	{
		return 0x02;
	}
	if(HAL_I2C_Master_Receive(handle, address, &var, 1, 1000) != HAL_OK)
	{
		return 0x03;
	}
	if(HAL_I2C_Master_Transmit(handle, address, (uint8_t *)d, 2, 1000) != HAL_OK)
	{
		return 0x04;
	}
	d1[0] = 0x19;
	d1[1] = 0x71;
	while(HAL_I2C_Master_Transmit(handle, address, d1, 2, 1000) != HAL_OK);
	
	uint8_t reg[2];
	reg[0] = 0x1C;
	reg[1] = 0x00;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		return 0x05;
	}
//	uint8_t temp;
//	if(HAL_I2C_Master_Receive(handle, address, &temp, 1, 1000) != HAL_OK)
	{
//		return 0x01;
	}
//	temp = 0x00;
//	if(HAL_I2C_Master_Transmit(handle, address, &temp, 1, 1000) != HAL_OK)
	{
//		return 0x01;
	}
	return var;
}
int16_t getAccel(I2C_HandleTypeDef* I2C)
{
	I2C_HandleTypeDef* handle = I2C;
	uint8_t reg = 0x3B;
	uint8_t address = 0xD0;
	uint8_t data[6];
	int16_t  accel_z;
	
//	uint8_t xbeeData[2];
	if(HAL_I2C_Master_Transmit(handle, address, &reg, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
		if(HAL_I2C_Master_Receive(handle, address, data, 6, 1000) != HAL_OK)
	{
		return 0x01;
	}
	//accel_x = (int16_t)(data[0] << 8 | data[1]);
	//accel_y = (int16_t)(data[2] << 8 | data[3]);
	accel_z = (int16_t)(data[4] << 8 | data[5]);
	//*(accel_data+index) = data[4];
	//*(accel_data+(index+1)) = data[5];
//	xbeeData[0] = data[4];
//	xbeeData[1] = data[5];
	
	//uart_send_int(data[4]);
	//uart_send_int(data[5]);
	
	
//	float z = accel_z/2048.0;
//	float z1 = 2.596;

	//print_str("\n\r");
//	char c[25];
//	sprintf(c, "%f", z);
//print_str("{TIMEPLOT|DATA|My Sensor|T|");
//	print_str(c);
	//print_str("}");
//print_str(c);
	
//	send_int(xbeeData,2);

	
//	print_str("\n\r");

		return accel_z;
}


void read_register(I2C_HandleTypeDef* I2C, uint8_t reg, char *name, int length)
{
	uint8_t data[8];
	uint8_t address = 0xD0;
	
	char c[25];
//	char hex_tmp[33];

	I2C_HandleTypeDef* handle = I2C;
	if(HAL_I2C_Master_Transmit(handle, address, &reg, 1, 1000) != HAL_OK)
	{
		data[0]= 0x01;
	}
	
		while(HAL_I2C_Master_Receive(handle, address, data,length, 1000) != HAL_OK);
	
	
	print_str("Reading register ");
	print_str(name);
	
	sprintf(c, "0x%X", *data);
	print_str(c);
	
	print_str("\n\r");
	
	
	
}

//Accelerometer Calibration 

//A - ZA_OFFSET_H = 0x05
//  - ZA_OFFSET_L_TC = 0x99

//B - ZA_OFFSET_H = 0x05
//  - ZA_OFFSET_L_TC = 0xCB

//C - ZA_OFFSET_H = 0x07
//  - ZA_OFFSET_L_TC = 0x5B
void calibration(I2C_HandleTypeDef* I2C)
{
//	char mesg[25];
	uint8_t address = 0xD0;
	I2C_HandleTypeDef* handle = I2C;
	
	uint8_t reg[2];
	reg[0] = ZA_OFFSET_H;
	reg[1] = 0x05;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting ZA_OFFSET_H") ;
	}
	reg[0] = ZA_OFFSET_L_TC;
	reg[1] = 0x99;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting ZA_OFFSET_L_TC") ;
	}
	reg[0] = SMPLRT_DIV;
	reg[1] = 0x04;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting SMPLRT_DIV") ;
	}
	//Set LSB sensitivity to +/- 8g
	reg[0] = ACCEL_CONFIG;
	reg[1] = 0x18;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting ACCEL_CONFIG") ;
	}
	//Set digital low pass filter bandwidth to 94 Hz
	reg[0] = CONFIG;
	reg[1] = 0x02;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting CONFIG") ;
	}
	//Interrupt configured for active high and clears on read operation of data registers
	reg[0] = INT_PIN_CFG;
	reg[1] = 0x30;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting INT_PIN_CFG");
	}
	//Enable interrupt on data ready to read in sensor data registers
	reg[0] = INT_ENABLE;
	reg[1] = 0x01;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting INT_ENABLE");
	}
	
}
void send_to_xbee(uint8_t *accelerometer_data_to_send_to_xbee)
{


	uint16_t arsum = 0;
	const int data_size = 100;
	uint8_t init[1];
	uint8_t final_array_to_send[109];
	
//	uint8_t Delimiter = 0x7E;
//	uint8_t Length = 0x00;
//	uint8_t Length1 =0x00;
	uint8_t API_identifier = 0x01;
	uint8_t API_frame_ID = 0x01;
	uint8_t Destination_address = 0x00;
	uint8_t Destination_address1 = 0x03;
	uint8_t Option_byte = 0x00;
	
	final_array_to_send[0] = 0x7E;
	final_array_to_send[1] = 0x00;
	final_array_to_send[2] = 0x69;
	final_array_to_send[3] = 0x01;
	final_array_to_send[4] = 0x01;
	final_array_to_send[5] = 0x00;
	final_array_to_send[6] = 0x03;
	final_array_to_send[7] = 0x00;
	
	for (int i = 0; i < data_size; i++) 
	{
			arsum += *(accelerometer_data_to_send_to_xbee+i); 
	}
//	uint16_t sum;
//	for (int i = 0; i < 8; i++) 
//	{
//			sum += final_array_to_send[i]; 
//	}
	uint16_t sum = API_identifier + API_frame_ID + Destination_address + Destination_address1 + Option_byte + arsum;
	uint16_t newsum = 0xff & sum;
	uint16_t checksum = 0xff - newsum;
 	uint8_t newchecksum = checksum;
	char c[25];
	sprintf(c, "%x", newchecksum);
	print_str("\n\r The newchecksum = ");
	print_str(c);
	print_str("\n\r");
	int i=0;
	while(i<100)
	{
		final_array_to_send[i+8]= *(accelerometer_data_to_send_to_xbee+i);
		//final_array_to_send[i+9]=;
		i++;
	}
	
	final_array_to_send[108] = newchecksum;
	
	init[0] = 0x42;
	uart_send_xbee_message(init,sizeof(init));
	uart_send_xbee_message(final_array_to_send, sizeof(final_array_to_send));
	//print_str("sent");
	send_int(final_array_to_send,data_size+9);
	//print_str((char*)final_array_to_send);
	
}





