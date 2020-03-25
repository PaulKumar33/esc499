#ifndef ARDUINOSERIALDRIVER_H
#define ARDUINOSERIALDRIVER_H

#ifdef __cplusplus
extern "C" {
#endif

#ifdef BUILDING_ARDUINOSERIALDRIVER
#define	ARDUINOSERIALDRIVER __declspec(dllexport)
#else
#define ARDUINOSERIALDRIVER __declspec(dllimport)
#endif

#define ARDUINO_WAIT_TIME 2000
#define MAX_DATA_LENGTH 255

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

HANDLE handler;
bool connected;
COMSTAT status;
DWORD errors;

DCB dcbSerialParameters = {0};

void __stdcall ARDUINOSERIALDRIVER initialize();
void ARDUINOSERIALDRIVER ArduinoSerialDriver(char *portName);
bool ARDUINOSERIALDRIVER IsConnected();
bool ARDUINOSERIALDRIVER DisconnectDevice();
bool ARDUINOSERIALDRIVER ConfigureController(int baudrate, int bytesize, float stopbits);
float ARDUINOSERIALDRIVER ReadSerialPort(char *buffer, unsigned int buf_size);
bool ARDUINOSERIALDRIVER WriteSerialPort(char *buffer, unsigned int buf_size);
void ARDUINOSERIALDRIVER Connect();
bool ARDUINOSERIALDRIVER ClearBuffer();

#ifdef __cplusplus
}
#endif

/*class ARDUINOSERIALDRIVER ArduinoSerialDriver{
public:
	ArduinoSerialDriver(char *portName){};
	virtual ~ArduinoSerialDriver(){};
	void Connect();
	};*/

#endif // ARDUINOSERIALDRIVER_H
