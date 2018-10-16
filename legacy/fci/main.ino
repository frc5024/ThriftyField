void setup(){
  Serial.begin(9600);
  int payload = 0;
  
  // set up pins
  pinMode(10,INPUT);
  pinMode(16,INPUT);
  pinMode(14,INPUT);
  pinMode(9,INPUT);
  pinMode(8,INPUT);
  pinMode(7,INPUT);
}

void loop(){
	//reset payload
	payload = 1000;
	
	// Payload:
	// [useless bit][0,1,2][0,1,2][0,1,2][vaults?]
	
	//red switch
	if(digitalRead(9) == HIGH){
		payload += 100;
	}else if(digitalRead(10) == HIGH){
		payload += 200;
	}
	
	//scale
	if(digitalRead(8) == HIGH){
		payload += 10;
	}else if(digitalRead(14) == HIGH){
		payload += 20;
	}
	
	//blue switch
	if(digitalRead(7) == HIGH){
		payload += 1;
	}else if(digitalRead(14) == HIGH){
		payload += 2;
	}
	
  Serial.write(payload); // send the payload
}