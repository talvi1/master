#include "accel_i2c.h"
#include "uart.h"

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
	uint8_t reg = 0x1C;
	if(HAL_I2C_Master_Transmit(handle, address, &reg, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
	uint8_t temp;
	if(HAL_I2C_Master_Receive(handle, address, &temp, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
	return var;
}
uint8_t getAccel(I2C_HandleTypeDef* I2C)
{
	I2C_HandleTypeDef* handle = I2C;
	uint8_t reg = 0x40;
	uint8_t address = 0xD0;
	uint8_t data;
	if(HAL_I2C_Master_Transmit(handle, address, &reg, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
		if(HAL_I2C_Master_Receive(handle, address, &data, 1, 1000) != HAL_OK)
	{
		return 0x01;
	}
		uart_send_message(data);
}
