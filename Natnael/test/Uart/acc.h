#include <stdint.h>

void spiClock_Port(void);
void spiINT(void);
void delay2(uint32_t count);
void transfer(uint16_t v);
uint16_t get_SPI_DATA_RECEIVE(void);

uint16_t acc_data(void);
void set_SPI_DATA_RECEIVE(uint16_t v);
void adxl_write(uint8_t reg, uint8_t value);
uint16_t adxl_read(uint8_t reg, uint8_t value);
void accINIT(void);  
void get_device_id(void);





