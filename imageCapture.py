from gpiozero import Button
from time import sleep, time
from picamera2 import Picamera2, Preview
import os
import requests
import pygame
from libcamera import Transform
import piexif
from PIL import Image

# Initialize the PiCamera
picam = Picamera2()

config = picam.create_preview_configuration(transform=Transform(hflip=True, vflip=True))
picam.configure(config)

picam.start_preview(Preview.QTGL)


# Set the path where you want to save the image
desktop_path = os.path.expanduser("/home/aaronchucarroll/Desktop/")

# Set up the button
button = Button(26, pull_up=False) 

def rotate(filepath):
    try:
        image = Image.open(filepath)
        exif_data = piexif.load(filepath)
        new_orientation = 3
        image = image.rotate(90, expand=True)
        exif_data['Orientation'] = new_orientation
        exif_bytes = piexif.dump(exif_data)
        image.save(filepath, exif=exif_bytes)
        print("Image successfully rotated")
    except:
        print("Could not rotate image.")

language_number = 0
while True:
    button.wait_for_press()
    start_time = time()
    button.wait_for_release()
    pressed_duration = time() - start_time
	
    if pressed_duration > 0.5:
        language_number += 1
        language_key = language_number % 5
        print(language_number)
        print(language_key)
        match language_key:
            case 0:
                pygame.mixer.init()
                pygame.mixer.music.load("/home/aaronchucarroll/hackathon/english.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    if button.is_pressed:
                        pygame.mixer.music.stop()
                        break
                sleep(0.5)
            case 1:
                pygame.mixer.init()
                pygame.mixer.music.load("/home/aaronchucarroll/hackathon/spanish.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    if button.is_pressed:
                        pygame.mixer.music.stop()
                        break
                sleep(0.5)
            case 2:
                pygame.mixer.init()
                pygame.mixer.music.load("/home/aaronchucarroll/hackathon/french.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    if button.is_pressed:
                        pygame.mixer.music.stop()
                        break
                sleep(0.5)
            case 3:
                pygame.mixer.init()
                pygame.mixer.music.load("/home/aaronchucarroll/hackathon/italian.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    if button.is_pressed:
                        pygame.mixer.music.stop()
                        break
                sleep(0.5)
            case 4:
                pygame.mixer.init()
                pygame.mixer.music.load("/home/aaronchucarroll/hackathon/mandarin.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    if button.is_pressed:
                        pygame.mixer.music.stop()
                        break
                sleep(0.5)
    else:
    	# Capture the image
        picam.start()
        picam.capture_file("test-image.jpg")
        print("Image captured")
        rotate("test-image.jpg")
        language_key = language_number % 5
        print(language_number)
        print(language_key)
        language = ""
        match language_key:
            case 0:
                language = "en-US"
            case 1:
                language = "es-ES"
            case 2:
                language = "fr-FR"
            case 3:
                language = "it-IT"
            case 4:
                language = "cmn-CN"
        url = "https://truvision-416017.ue.r.appspot.com/detect_text?language=" + language
        print(url)
        files = {"file": open("/home/aaronchucarroll/hackathon/test-image.jpg", "rb")}
        
		# Send the POST request
        x = requests.post(url, files=files)
        if x.status_code == 200:
            desktop_path=os.path.expanduser("/home/aaronchucarroll/hackathon/")
            filename = "audio.mp3"
            save_path = os.path.join(desktop_path, filename)
            
            with open(save_path, 'wb') as f:
                f.write(x.content)
            print(f"File saved to {save_path}")
            pygame.mixer.init()
            pygame.mixer.music.load("/home/aaronchucarroll/hackathon/audio.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                if button.is_pressed:
                     pygame.mixer.music.stop()
                     break
            sleep(0.5)
        else:
            print("Failed to download file")
            pygame.mixer.init()
            pygame.mixer.music.load("/home/aaronchucarroll/hackathon/file_not_found.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                if button.is_pressed:
                     pygame.mixer.music.stop()
                     break
            sleep(0.5)
