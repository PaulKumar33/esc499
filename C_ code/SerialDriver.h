#ifndef SERIALDRIVER_H
#define SERIALDRIVER_H

#ifdef __cplusplus
extern "C" {
#endif

#ifdef BUILDING_SERIALDRIVER_DLL
#define	SERIALDRIVER __declspec(dllexport)
#else
#define SERIALDRIVER __declspec(dllimport)
#endif

void __stdcall SERIALDRIVER Init();

#ifdef __cplusplus
}
#endif


#define	ARDUINO_WAIT_TIME 2000 //leave this for now may need to tinker with
#define MAX_DATA_LENGTH 255

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

class SerialDriver
{
private:
	HANDLE handler;
	bool connected;
	COMSTAT status;
	DWORD errors;
public:
	SerialDriver(char *portName); //constructor
	~SerialDriver();

	float readSerialPort(char *buffer, unsigned int buf_size);
	bool writeSerialPort(char *buffer, unsigned int buf_size);
	bool isConnected();
};

#endif // SERIALDRIVER_H