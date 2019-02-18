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
	d[1] = 0x00;
	if(HAL_I2C_IsDeviceReady(handle, address, 2, 5) != HAL_OK)
	{
		return 0x01;
	}
	if(HAL_I2C_Master_Transmit(handle, address, &who_am_i, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
	if(HAL_I2C_Master_Receive(handle, address, &var, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
	if(HAL_I2C_Master_Transmit(handle, address, (uint8_t *)d, 2, 1000) != HAL_OK)
	{
		return 0x01;
	}
	d1[0] = 0x19;
	d1[1] = 0x71;
	while(HAL_I2C_Master_Transmit(handle, address, d1, 2, 1000) != HAL_OK);
	
	uint8_t reg[2];
	reg[0] = 0x1C;
	reg[1] = 0x00;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		return 0x01;
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
uint8_t getAccel(I2C_HandleTypeDef* I2C)
{
	I2C_HandleTypeDef* handle = I2C;
	uint8_t reg = 0x3B;
	uint8_t address = 0xD0;
	uint8_t data[6];
	int16_t accel_x, accel_y, accel_z;
	
	uint8_t accelerometer_to_send_to_xbee[2];
	if(HAL_I2C_Master_Transmit(handle, address, &reg, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
		if(HAL_I2C_Master_Receive(handle, address, data, 6, 1000) != HAL_OK)
	{
		return 0x01;
	}
	accel_x = (int16_t)(data[0] << 8 | data[1]);
	accel_y = (int16_t)(data[2] << 8 | data[3]);
	accel_z = (int16_t)(data[4] << 8 | data[5]);
	accelerometer_to_send_to_xbee[0] = data[4];
	accelerometer_to_send_to_xbee[1] = data[5];
	
//	uart_send_int(data[4]);
//	uart_send_int(data[5]);
	
	
float z = accel_z/8192.0;
float z1 = 2.596;

	//print_str("\n\r");
//char c[25];
//sprintf(c, "%u", accel_z);
//print_str("{TIMEPLOT|DATA|My Sensor|T|");
//print_str(c);print_str("}");
//print_str(c);
	
	send_int(accelerometer_to_send_to_xbee,2);

	
	print_str("\n\r");
}


int16_t get_Accelerometer(I2C_HandleTypeDef* I2C)
{
		I2C_HandleTypeDef* handle = I2C;
	I2C_HandleTypeDef hi2c1;
	uint8_t reg = 0x3B;
	uint8_t address = 0xD0;
	uint8_t data[6];
	int16_t accel_x, accel_y, accel_z;
	const int data_size =100;
	const int loop_size =50;
	uint8_t xbee_data[data_size];
	uint8_t accelerometer_to_send_to_xbee[2];
	
	
	if(HAL_I2C_Master_Transmit(handle, address, &reg, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
		if(HAL_I2C_Master_Receive(handle, address, data, 6, 1000) != HAL_OK)
	{
		return 0x01;
	}
	accel_z = (int16_t)(data[4] << 8 | data[5]);
	accelerometer_to_send_to_xbee[0] = data[4];
	accelerometer_to_send_to_xbee[1] = data[5];

	//send_int(accelerometer_to_send_to_xbee,2);

	
	print_str("\n\r");
	
	for(int i=0; i<loop_size;i=i+2)
	{
		xbee_data[i] = data[4];
		xbee_data[i+1] = data[5];
		get_Accelerometer(&hi2c1);
		
	}
	//send_int(xbee_data,data_size);
	
	send_to_xbee(xbee_data);
	return accel_z;

}

void send_to_xbee(uint8_t accelerometer_data_to_send_to_xbee[])
{


	uint16_t arsum = 0;
	const int data_size = 100;
	
	uint8_t final_array_to_send[109];
	
//	uint8_t Delimiter = 0x7E;
//	uint8_t Length = 0x00;
//	uint8_t Length1 =0x00;
//	uint8_t API_identifier = 0x01;
//	uint8_t API_frame_ID = 0x01;
//	uint8_t Destination_address = 0x00;
//	uint8_t Destination_address1 = 0x03;
//	uint8_t Option_byte = 0x00;
	
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
			arsum += accelerometer_data_to_send_to_xbee[i]; 
	}
	uint16_t sum;
	for (int i = 0; i < 8; i++) 
	{
			sum += final_array_to_send[i]; 
	}
	//uint16_t sum = API_identifier + API_frame_ID + Destination_address + Destination_address1 + Option_byte + arsum;
	uint16_t newsum = 0xff & sum;
	uint16_t checksum = 0xff - newsum;
 	uint8_t newchecksum = checksum;
	int i=0;
	while(i<100)
	{
		final_array_to_send[i+8]=accelerometer_data_to_send_to_xbee[0];
		final_array_to_send[i+9]=accelerometer_data_to_send_to_xbee[1];
		i= i+ 2;
	}
	
	final_array_to_send[108] = newchecksum;
	uart_send_xbee_message(final_array_to_send, sizeof(final_array_to_send));
	//print_str("sent");
	send_int(final_array_to_send,data_size+9);
	//print_str((char*)final_array_to_send);
	
	
	
	
	
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
void calibration(I2C_HandleTypeDef* I2C)
{
//	char mesg[25];
	uint8_t address = 0xD0;
	I2C_HandleTypeDef* handle = I2C;
	
	uint8_t reg[2];
	reg[0] = ZA_OFFSET_H;
	reg[1] = 0x02;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting ZA_OFFSET_H") ;
	}
	reg[0] = ZA_OFFSET_L_TC;
	reg[1] = 0x4E;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting ZA_OFFSET_L_TC") ;
	}

	reg[0] = I2C_MST_DELAY_CTRL;
	reg[1] = 0x1;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting I2C_MST_DELAY_CTRL") ;
	}	
	reg[0] = I2C_MST_CTRL;
	reg[1] = 0xA;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting I2C_MST_CTRL") ;
	}
	reg[0] = SMPLRT_DIV;
	reg[1] = 0xff;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting SMPLRT_DIV") ;
	}
	reg[0] =  CONFIG;
	reg[1] = 0x5;
	if(HAL_I2C_Master_Transmit(handle, address, reg, 2, 1000) != HAL_OK)
	{
		print_str("Error setting SMPLRT_DIV") ;
	}
}



