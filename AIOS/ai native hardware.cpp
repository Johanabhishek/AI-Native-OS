// ==========================================
// PROJECT: AI-NATIVE OS PROTOTYPE (T-HUB DEMO)
// MODULE: THERMAL MANAGEMENT KERNEL
// ==========================================

// --- HARDWARE MAPPING ---
const int sensorPin = 34; // The "Nervous System" (Input)
const int ledGreen = 15;  // State: NORMAL
const int ledRed = 2;     // State: CRITICAL
const int ledBlue = 4;    // State: AI_FIX_APPLIED

// --- KERNEL VARIABLES ---
int systemLoad = 0;       // 0 to 100%
bool aiIntervention = false;

void setup() {
  // 1. Initialize Serial Terminal (The "Log")
  Serial.begin(115200);
  Serial.println("\n[BOOT] AI-Native Kernel v0.1 loading...");
  delay(500);
  Serial.println("[CHECK] NPU... DETECTED");
  Serial.println("[CHECK] Neural Engine... ONLINE");
  Serial.println("[INFO] System Ready. Awaiting User Input.\n");

  // 2. Configure Hardware
  pinMode(ledGreen, OUTPUT);
  pinMode(ledRed, OUTPUT);
  pinMode(ledBlue, OUTPUT);
  pinMode(sensorPin, INPUT);
}

void loop() {
  // 1. SENSE (Read the Potentiometer)
  int rawValue = analogRead(sensorPin);
  
  // Convert 0-4095 to 0-100% Load
  systemLoad = map(rawValue, 0, 4095, 0, 100);

  // 2. INFERENCE (The "AI" Decision Logic)
  // Scenario A: Safe Zone (Load < 40%)
  if (systemLoad < 40) {
    setSystemState(HIGH, LOW, LOW); // Green ON
    logStatus("NORMAL", "Efficiency Optimized");
    aiIntervention = false;
  }
  
  // Scenario B: Danger Zone (Load > 40% but < 80%)
  // Traditional OS would just let it get hot.
  else if (systemLoad >= 40 && systemLoad < 80) {
    setSystemState(LOW, HIGH, LOW); // Red ON
    logStatus("WARNING", "Thermal Throttling Imminent");
    aiIntervention = false;
  }
  
  // Scenario C: AI Takeover (Load > 80%)
  // The AI realizes the user needs max power, so it activates cooling instead of slowing down.
  else {
    setSystemState(LOW, LOW, HIGH); // Blue ON
    aiIntervention = true;
    logStatus("CRITICAL", "AI Rerouting Power to Cooling Grid");
  }

  // Small delay to make the logs readable
  delay(200);
}

// Helper function to control LEDs cleanly
void setSystemState(int g, int r, int b) {
  digitalWrite(ledGreen, g);
  digitalWrite(ledRed, r);
  digitalWrite(ledBlue, b);
}

// Helper function to print cool "OS Style" logs
void logStatus(String level, String message) {
  Serial.print("[KERNEL] Load: ");
  Serial.print(systemLoad);
  Serial.print("% | Status: [");
  Serial.print(level);
  Serial.print("] >> ");
  Serial.println(message);
}