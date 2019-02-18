
#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_i2c.h"

uint8_t MPU6050_Init(I2C_HandleTypeDef* I2C);
uint8_t getAccel(I2C_HandleTypeDef* I2C);
void read_register(I2C_HandleTypeDef* I2C, uint8_t reg, char *name, int length);
void calibration(I2C_HandleTypeDef* I2C);

int16_t  get_Accelerometer(I2C_HandleTypeDef* I2C);
void send_to_xbee(uint8_t accelerometer_data_to_send_to_xbee[]);
