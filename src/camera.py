import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.camera
import time
from datetime import datetime

def take_picture():
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0",(640,480))
    cam.start()
    time.sleep(3)
    img = cam.get_image()
    cam.stop()
    new_picture_name = str(datetime.utcnow()) + '.png'
    pygame.image.save(img,"static/unknown_people/{}".format(new_picture_name))
    return "static/unknown_people/" + new_picture_name