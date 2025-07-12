********** Arduino Ai Integration **********

********** created by fused-player **********

String input;
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); // Example
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    
    input.trim();
    input.toLowerCase();

    if (input == "led_on") {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (input == "led_off") {
      digitalWrite(LED_BUILTIN, LOW);
    } else if (input.startsWith("servo_r_")) {
      // Extract angle and move servo
    }

    Serial.println(input + "_TASK_DONE");
  }
}
