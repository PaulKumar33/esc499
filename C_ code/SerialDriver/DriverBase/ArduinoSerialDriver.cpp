#include <stdio.h>
using namespace std;
#include <string>
#include <stdlib.h>
//#include <iostream>

#include "ArduinoSerialDriver.h"
//#include <iostream>


__stdcall void initialize(){
	printf("Attempting to initialize Arduino Serial Driver\n");
}
void ArduinoSerialDriver(char *portName){
	connected = false;
	handler = CreateFileA(static_cast<LPCSTR>(portName),
		GENERIC_READ | GENERIC_WRITE,
		0,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL);

	if(handler == INVALID_HANDLE_VALUE){
		if(GetLastError() == ERROR_FILE_NOT_FOUND){
			printf("Error: Invalid handle\n");
			printf("Port %s not available\n", portName);
		}
		else{
		printf("Error\n");
		}
	}

	else{
		
		if(!GetCommState(handler, &dcbSerialParameters)){
			printf("Failed to get serial parameters\n");
		}
		else{
			printf(">> Running auto init\n");
			printf("Baudrate: 115200\n");
			printf("Buffer byte size: 8\n");
			printf("StopBits: 1\n");
			printf("Parity: None\n");
			dcbSerialParameters.BaudRate = CBR_19200;
			dcbSerialParameters.ByteSize = 8;
			dcbSerialParameters.StopBits = ONESTOPBIT;
			dcbSerialParameters.Parity = NOPARITY;
			dcbSerialParameters.fDtrControl = DTR_CONTROL_ENABLE;

			if(!SetCommState(handler, &dcbSerialParameters))
				printf(">> Error: could not set serial port state\n");
			else{
				connected = true;
				printf(">> Connected to Arduino Serial Device\n");
				PurgeComm(handler, PURGE_RXCLEAR | PURGE_TXCLEAR);
				printf(">> Purging device...\n");
				Sleep(ARDUINO_WAIT_TIME);
			}
		}
	}

}

bool IsConnected(){
	if(!connected){
		printf(">> There is no serial device connected\n");
	}
	else{
		printf(">> Serial device connected\n");
	}
	return connected;
}

bool DisconnectDevice(){
	if(connected){
		connected = false;
		CloseHandle(handler);
		printf(">> Handle Closed. No Device is connected");
		return true;
	}
	else{
		printf(">> No device is connected\n");
		return false;
	}
}

bool ConfigureController(int baudrate, int bytesize, float stopbits)
{
	//this is a library method. Call externally to configure the atmega controller
	DWORD timout;
	DWORD baud;
	//DCB dcb;
	bool char_flag = false;
	DWORD bytecase = 8;

	printf(">> COnfiguring Serial Device....\n");
	printf(">> Baudrate: %s\n", baudrate);
	printf(">> ByteSize: %s\n", bytesize);
	printf(">> Stopbits: %s\n", bytesize);
	printf(">> Parity:   %s\n", NOPARITY);

	int rates[7] = {9600, 19200, 38400, 57600, 115200, 128000, 256000};
	DWORD rates_array[7] = {CBR_9600, CBR_19200, CBR_38400, CBR_57600,CBR_115200,
						  CBR_128000, CBR_256000};
	int baudIndex = 0;
	for(int index = 0; index < sizeof(rates); index++){
		if(rates[index] == baudrate){
			baudIndex = index;
		}
		else if(rates[index] != baudrate & index == sizeof(rates_array)-1){
			printf(">>Invalid baudrate\n");
			Sleep(500);
			printf(">> Aborting Config\n");
			return false;
		}
		else{
			continue;
		}
	}
	//setting the baud rate
	baud = rates_array[baudIndex];

	// for number of bits in serial buffer. they should pass in an integer
	int i = bytesize - 6;
	switch(i){
		case 1 : bytecase = 7;
		case 2 : bytecase = 8;
	}

	// stop bits
	DWORD stop_bits = ONESTOPBIT;
	if(stopbits == 1.0){
		stop_bits = ONESTOPBIT;
	}
	else if(stopbits == 1.5){
		stop_bits = ONE5STOPBITS;
	}
	else if(stopbits == 2.0){
		stop_bits = TWOSTOPBITS;
	}
	else{
		printf(">> Invalid stopbits setting\n");
		Sleep(500);
		printf(">> Aborting Config\n");
		return false;
	}

	dcbSerialParameters.BaudRate = baud;
	dcbSerialParameters.ByteSize = bytecase;
	dcbSerialParameters.Parity = NOPARITY;
	dcbSerialParameters.StopBits = stop_bits;
	dcbSerialParameters.fDtrControl = DTR_CONTROL_ENABLE;
	if(!SetCommState(handler, &dcbSerialParameters)){
		printf(">> Device was not able to be set\n");
		Sleep(500);
		printf(">> Aborting Config\n");
		return false;
	}
	printf(">> Configuration complete");
}

float ReadSerialPort(char *buffer, unsigned int buf_size){
	//this method reads the serial port
	//pass the buffer in by reference so the value is stored in the address
	Sleep(1);
	DWORD bytesRead;
	unsigned int toRead = 0;
	int value;

	ClearCommError(handler, &errors, &status);
	if(status.cbInQue > 0){
		if(status.cbInQue > buf_size){
			toRead = buf_size;
		}
		else{
			toRead = status.cbInQue;
		}
	}
	if(ReadFile(handler, buffer, toRead, &bytesRead, NULL)){
		//printf("%s\n", buffer);
		float fr = atof(buffer);
		return fr;
	}
	return 9999.0;
}

bool WriteSerialPort(char *buffer, unsigned int buf_size){
	//this method writes to the serial port
	DWORD bytesSend;
	if(!WriteFile(handler, (void*)buffer, buf_size, &bytesSend, 0)){
		ClearCommError(handler, &errors, &status);
		return false;
	}
	return true;
}

bool ClearBuffer(){
	//this method is used to clear the serial buffer
	bool status = PurgeComm(handler, PURGE_RXCLEAR | PURGE_TXCLEAR);
	if(!status){
		printf("Purge failed when clearing serial buffer\n");
		return false;
	}
	return true;
}

/*ArduinoSerialDriver::ArduinoSerialDriver(char *portName){
	this->connected = false;
	this->handler = CreateFileA(static_cast<LPCSTR>(portName),
		GENERIC_READ | GENERIC_WRITE,
		0,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL);

	if(this->handler == INVALID_HANDLE_VALUE){
		if(GetLastError() == ERROR_FILE_NOT_FOUND){
			printf("Error: Invalid handle\n");
			printf("Port %s not available\n", portName);
		}
		else{
		printf("Error\n");
		}
	}

	else{
		DCB dcbSerialParameters = {0};
		if(!GetCommState(this->handler, &dcbSerialParameters)){
			printf("Failed to get serial parameters\n");
		}
		else{
			dcbSerialParameters.BaudRate = CBR_19200;
			dcbSerialParameters.ByteSize = 8;
			dcbSerialParameters.StopBits = ONESTOPBIT;
			dcbSerialParameters.Parity = NOPARITY;
			dcbSerialParameters.fDtrControl = DTR_CONTROL_ENABLE;

			if(!SetCommState(handler, &dcbSerialParameters))
				printf("Error: could not set serial port state\n");
			else{
				this->connected = true;
				PurgeComm(this->handler, PURGE_RXCLEAR | PURGE_TXCLEAR);
				Sleep(ARDUINO_WAIT_TIME);
			}
		}
	}

}*/

void Connect(){
	printf("does nothing for now\n");
}
