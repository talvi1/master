#include "accel_i2c.h"
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
	d1[1] = 0x7F;
	if(HAL_I2C_Master_Transmit(handle, address, (uint8_t *)d1, 2, 1000) != HAL_OK)
	{
		return 0x01;
	}
	uint8_t reg[2];
	reg[0] = 0x1C;
	reg[1] = 0x00;
	if(HAL_I2C_Master_Transmit(handle, address, (uint8_t *)reg, 2, 1000) != HAL_OK)
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
	float z = accel_z/8192.0;
	float z1 = 2.596;
//	uart_send_message(data[0]);
//	uart_send_message(data[1]);
//	print_str("\n\r");
	char c[25];
	sprintf(c, "%g", z);
	print_str(c);
	print_str("\n\r");
}
