
#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_i2c.h"

uint8_t MPU6050_Init(I2C_HandleTypeDef* I2C);
uint8_t getAccel(I2C_HandleTypeDef* I2C, uint8_t *accel_data, uint8_t index);
void read_register(I2C_HandleTypeDef* I2C, uint8_t reg, char *name, int length);
void calibration(I2C_HandleTypeDef* I2C);
