# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 16:56:27 2021
This is a command line script that awaits key presses for CTRL+ALT to begin looking for ingredients in your inventory.
To set up in-game, navigate to your ingredient inventory all the way at the top of the list. Once CTRL+Alt press is detected,
down arrow button presses will occur after the ingredient is parsed. 
@author: wyatt
"""
import mss
import pytesseract
import numpy as np
from PIL import Image
import win32api
import cv2
import re, string
from IngredientManager import IngredientManager
import time
from PressKey import *

IM = IngredientManager()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  # your path may be different

def adjusted_capture(screen, base_pixel_x, base_pixel_y, y_size, x_size):
        '''Allows for dynamic shot capture on (almost) any resolution.
		Shape is based on intially captured height (1080) and width (1920).
		Proportional results provided with input based on user screensize'''

        screen_w_adj = (screen.shape[0]/1080)
        screen_h_adj = (screen.shape[1]/1920)

        aspect_ratio = screen.shape[0]/screen.shape[1]
        aspect_adj = (1080/1920)/aspect_ratio

        screen = np.array(screen[int((base_pixel_y*(1/aspect_adj))*screen_h_adj):\
									 int((y_size*(screen.shape[0]/1080) \
									  +((base_pixel_y*(1/aspect_adj))*screen_h_adj))),
                                int((base_pixel_x*aspect_adj)*screen_w_adj):\
									int((x_size*(screen.shape[1]/1920) \
							     +(base_pixel_x*aspect_adj)*screen_w_adj)), :])


        return screen

print("Alchemy Ingredient Parser - Version 1.0")
print("In Vanilla Skyrim Inventory, navigate to the top of your ingredients list. ")
print("Press CTRL+ALT to initiate parsing")
while True:
	state_ctrl = win32api.GetKeyState(0x11)
	state_alt = win32api.GetKeyState(0x12)
	LastIng = ""
	Capture = True
	if state_ctrl < 0 and state_alt<0:
			while(Capture):
				with mss.mss() as sct:
					image = np.array(sct.grab(sct.monitors[1]))
					image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				#Capture selected inventory
				inv = adjusted_capture(image, 370,542,60,331)
				#Capture first effect
				FirstEffect = adjusted_capture(image, 1040,790,50,300)
				#Capture second effect
				SecondEffect = adjusted_capture(image, 1340,790,50,300)
				#Capture third effect
				ThirdEffect = adjusted_capture(image, 1040,830,50,275)
				#Capture fourth effect
				FourthEffect = adjusted_capture(image, 1340,830,50,275)
				#current_date = datetime.date.today().strftime("%d-%m-%Y")
				im = Image.fromarray(inv)
				im.save("inventory.png")
				im = Image.fromarray(FirstEffect)
				im.save("1.png")
				im = Image.fromarray(SecondEffect)
				im.save("2.png")
				im = Image.fromarray(ThirdEffect)
				im.save("3.png")
				im = Image.fromarray(FourthEffect)
				im.save("4.png")

				KnownEffect = [False,False,False,False]
				for i in range(1,5):
					temp_Parse = pytesseract.image_to_string(Image.open(str(i) + ".png"))
					temp_Parse= temp_Parse[0:temp_Parse.find("\n")]
					#UN is checked for parsed pytesseract result. No other instances of
					#	results would have two uppercase chars (UN from UNKNOWN).
					#	Minimizing resulting errors
					#	by only checking this occurance
					if "UN" not in temp_Parse:
						KnownEffect[i-1] = True

				#Parese image and cleanse up to \n char to just get ingredient name
				inv = pytesseract.image_to_string(Image.open("inventory.png"))
				inv = inv[0:inv.find("\n")]
				#Check if at bottom of inventory and stop the capture if so.
				if inv == LastIng:
					Capture = False
				else:
					LastIng = inv
					IM.AddPlayerIng(inv, KnownEffect[0], \
					 KnownEffect[1], \
					 KnownEffect[2], \
					 KnownEffect[3])
					PressDown()
			IM.ExportToCSV()
