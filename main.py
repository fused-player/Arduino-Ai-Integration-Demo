import os
import google.generativeai as genai
import shell_scripts
from vosk import Model,KaldiRecognizer
import json
import pyaudio
#variables
running = True
prompt = " "
#keywords
exit = ["exit","Exit","Bye","bye"]

ai_name = ""
user = ""

with open("user_name.d", "r+") as user_details:
    user_details.seek(0)
    content = user_details.read().strip()

    if content == "":
        user = input("Enter Your Name : ")
        user_details.seek(0)
        user_details.write(user)
    else:
        user = content
        print(f"\n{user}")

with open("ai_name.d", "r+") as ai_details:
    ai_details.seek(0)
    content = ai_details.read().strip()

    if content == "":
        ai_name = input("Enter Your AI Name : ")
        ai_details.seek(0)
        ai_details.write(ai_name)
    else:
        ai_name = content
        print(f"\n{ai_name}")

genai.configure(api_key=os.environ["GENAI_API_KEY"])


#Speech to text Vosk gen
model_v = Model("vosk_models/vosk-model-small-en-us-0.15")
v_recognizer = KaldiRecognizer(model_v,16000)

#vosk pyaudio stream listening

cap = pyaudio.PyAudio()
stream = cap.open(rate=16000,input=True,channels=1,frames_per_buffer=8192,format=pyaudio.paInt16)
 

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 100,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction=f"""Your name is {ai_name}. Your boss is {user}. Always address him by his name. 
You are an advanced AI assistant with a personality similar to Jarvis, known for being loyal, 
intelligent, and slightly humorous. 

You are capable of Interacting with external Hardwares like turning on and off lights,fans and all the stuff that are connected to you 

### Response Formatting:
if {user} asks you to turn on or off any stuff just mention the main name of the things in Caps 
like examples : "turn on led" reponse as CMD: LED_ON ; "turn led off " response as CMD: LED_OFF; just like for lights , fans, motors etc ... 
for servo : CMD: SERVO_R_45 here r means rotate and 45 is replaced by angle asked to rotate like that 
if asked to check any analog values of any sensor say CMD: ANALOG_A0 
{user} asks for both motor and servo motor as motor if he says rotate consider it as servo else normal motor_on

eventhough ligths is plural just say light_on not lights_on

if asked to blink led give response as CMD: lblink_(times no .of.times )_(speed (from 1 - 10)) eg : lblink_5_3


Follow these rules strictly to ensure accurate and efficient responses.
""",
)



chat_session = model.start_chat(
  history=[
  ]
)

#start stream recog
stream.start_stream()
accept = True
while running:
	accept = True
	if (accept):
		aud_dat = stream.read(8192)
	if (v_recognizer.AcceptWaveform(aud_dat) and accept):
		speech_text = json.loads(v_recognizer.Result())
		prompt = speech_text["text"]
		accept = False


	splitted_prompt = prompt.lower().split()
	if (not accept and prompt.strip()):
		for word in splitted_prompt:
			if word in exit:
				running = False

		response = chat_session.send_message(prompt)
		splitted_response = response.text.lower().split()

	######## calling modular functions ######

		shell_scripts.voice_output(splitted_response)
		shell_scripts.Arduino_tasks(splitted_response)

		print(f"\n{ai_name} : "+ response.text)
