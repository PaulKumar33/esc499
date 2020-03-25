// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

int data;
String byte_to_send;



void setup() {
  //sbi(ADCSRA,ADPS2);
  //cbi(ADCSRA,ADPS1);
  //cbi(ADCSRA,ADPS0);
  Serial.begin(115200);
  data = 0.0;
  byte_to_send = "";
}

void loop() {
  // put your main code here, to run repeatedly:
  
  data = analogRead(A0);
  int res = data/1023*3;
  Serial.println(data);  
  delayMicroseconds(500);
}
