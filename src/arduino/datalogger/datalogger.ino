#define BUFFER_LEN 13
byte buffer[BUFFER_LEN];

void setup() { 
  Serial.begin(9600);
  buffer[0] = 0;
  buffer[1] = 0;
  buffer[2] = 0;
}

void loop() {  
 for (int i=0; i<5; i++) {
   *(&buffer[(i*2)+3]) = (int) analogRead(i);
 } 

 Serial.write(buffer, BUFFER_LEN);
 delay(100);
}
