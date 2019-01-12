
#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_i2c.h"

uint8_t MPU6050_Init(I2C_HandleTypeDef* I2C);
uint8_t getAccel(I2C_HandleTypeDef* I2C);
