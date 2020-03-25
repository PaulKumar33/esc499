#include "SerialDriver.h"
#include<iostream>
using namespace std;
#include<string>
#include<stdlib.h>


__stdcall void Init(){
	printf("Initializing DLL library\n");
}

SerialDriver::SerialDriver(char *portName){
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

}

SerialDriver::~SerialDriver(){
	if(this->connected){
		this->connected = false;
		CloseHandle(this->handler);
	}
}

float SerialDriver::readSerialPort(char *buffer, unsigned int buf_size){
	DWORD bytesRead;
	unsigned int toRead = 0;

	ClearCommError(this->handler, &this->errors, &this->status);

	if(this->status.cbInQue >0){
		if(this->status.cbInQue > buf_size){
			toRead = buf_size;
		}
		else{
			toRead = this->status.cbInQue;
		}
	}
	if(ReadFile(this->handler, buffer, toRead, &bytesRead, NULL)){
		return bytesRead;
	}
	return 0;
}

bool SerialDriver::writeSerialPort(char *buffer, unsigned int buf_size){
	DWORD bytesSend;
	if(!WriteFile(this->handler, (void*)buffer, buf_size, &bytesSend, 0)){
		ClearCommError(this->handler,&this->errors, &this->status);
		return false;
	}
	else{
		return true;
	}
}

bool SerialDriver::isConnected(){
	if(!connected){
		printf("Serial Device is not connected\n");
	}
	else{
		printf("Connected to serial device\n");
	}
	return this->connected;

}

int main(){
	cout<<"Initializing Serial Driver"<<endl;
	return 0;
}




