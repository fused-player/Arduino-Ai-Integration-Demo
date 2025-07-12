import subprocess 
import torch
from TTS.api import TTS
import pygame
import time
import serial

SerialInst = serial.Serial()
SerialInst.baudrate = 9600
SerialInst.port = '/dev/ttyACM0'
SerialInst.open()

def voice_output(splitted_response):
	pygame.init()

	for index,word in enumerate(splitted_response):
		if word == "link:":
			splitted_response = splitted_response[0:index]
	for index,word in enumerate(splitted_response):
		if word == "image:":
			splitted_response = splitted_response[0:index]

	response = ' '.join(splitted_response)
	device = "cuda" if torch.cuda.is_available() else "cpu"

	tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)

	tts.tts_to_file(response, speaker_wav="audio/clone/audio.wav", language = "en",file_path="audio/m_temp/output.wav",stability = 1)

	pygame.mixer.music.load("audio/m_temp/output.wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(10)

def Arduino_tasks(splitted_response):
    print(splitted_response)
    for index,word in enumerate(splitted_response):
        if word == "cmd:":
            print(" Arduino tasks() ************************ ")
            to_do = ' '.join(splitted_response[index+1:])
            print(' '.join(to_do))
            SerialInst.write(to_do.encode('utf-8'))
            
    
