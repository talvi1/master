
#include "xbee.h"
#include <stdio.h>

I2C_HandleTypeDef hi2c1;
I2C_HandleTypeDef hi2c2;

void send_to_xbee(void)
{
	 
	 uint16_t arsum;
	const int data_size =100;
	const int loop_size =50;
	uint8_t xbee_data[data_size];
	 uint8_t * accelerometer_data = get_Accelerometer(&hi2c1);
	for(int i=0; i<loop_size;i++)
	{
		xbee_data[i] = *(accelerometer_data);
		xbee_data[i+1] = *(accelerometer_data+1);
	}
	
	send_int(xbee_data,data_size);

	
	print_str("\n\r");

	
	 uint16_t Delimiter = 0x7E;
	 uint16_t Length = 0x00;
	 uint16_t Length1 = 0x37;
	 uint16_t API_identifier = 0x01;
	 uint16_t API_frame_ID = 0x01;
	 uint16_t Destination_address = 0x00;
	 uint16_t Destination_address1 = 0x02;
	 uint16_t Option_byte = 0x00;
	for (int i = 0; i < 50; i++) 
	 {
		 arsum += ar[i]; 
	 }
		 
	
	 
	 uint16_t sum = API_identifier + API_frame_ID + Destination_address + Destination_address1 + Option_byte + arsum;
	 uint16_t newsum = 0x00ff & sum;
	 uint16_t checksum = 0x00ff - newsum;
	 uint8_t newchecksum = checksum;
	 uint16_t newnewchecksum = newchecksum;
}
