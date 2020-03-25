#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h> 
#include <windows.h>
#include <windef.h>
#include <winnt.h>
#include <winbase.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <ftd2xx.h>
#include <sys/time.h>




FT_HANDLE ftHandle;
FT_STATUS ftstatus;
DWORD numDevs;

FT_DEVICE_LIST_INFO_NODE *devinfo;

void DeviceInforList(){
	//this method returns the number of ftdi devices connected
	//ftstatus = FT_CreateDeviceInfoList(&numDevs);
	printf(">> Geting device info...\n");
	ftstatus = FT_CreateDeviceInfoList(&numDevs);
	if(ftstatus == FT_OK){
		printf("Number of devices available: %s\n", numDevs);
		//return numDevs
		//return true;
	}
	else{
		printf("There was an error retrieving devices\n");
		//return false;
	}
}

void GetDeviceInfoList(){
	printf(">> Preparing device info list...\n");
	Sleep(500);
	DeviceInforList();
	devinfo = (FT_DEVICE_LIST_INFO_NODE*)malloc(sizeof(FT_DEVICE_LIST_INFO_NODE) *numDevs);
	printf("here\n");
	Sleep(500);
	ftstatus = FT_GetDeviceInfoList(devinfo, &numDevs);

	if(ftstatus = FT_OK){
		//flow for this
		printf(">> ftStatus return status OK\n");
		Sleep(500);
		for(int i =0; i<numDevs; i++){
			printf(">> ftHandle: 0x%x", devinfo[i].ftHandle);
		}
	}
	else{
		printf("there was an error getting the info list\n");
	}

}

void OpenDevice(){
	printf("Attempting to open device\n");
	ftstatus = FT_Open(0, &ftHandle);
	if(ftstatus == FT_OK){
		printf("Open Device\n");
		printf("Device Handle: %s\n", ftHandle);
	}
	else{
		printf("there was an error opening the device\n");
	}
}

int main(int argc, char * argv[])
{
	DeviceInforList();
	GetDeviceInfoList();
	OpenDevice();
   //code
	printf("This is the main method\n");
	printf("press any key to continue\n");
	getchar();
}