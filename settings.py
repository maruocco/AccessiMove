# Python program to create a basic settings menu using the pygame_menu module 

import pygame 
import pygame_menu as pm 

pygame.init() 

pygame.display.set_caption("Settings")

# Screen 
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
LIGHT_BLUE = (173, 216, 230)

# Main function of the program 


def main(): 
	# List that is displayed while selecting the graphics level 
	actions = [("Up Arrow Key", "U_ak"), 
				("Down Arrow Key", "D_ak"), 
				("Left Arrow Key", "L_ak"), 
				("Right Arrow Key", "R_ak")] 


	# This function displays the currently selected options 

	def printSettings(): 
		print("\n\n") 
		# getting the data using "get_input_data" method of the Menu class 
		settingsData = settings.get_input_data() 

		for key in settingsData.keys(): 
			print(f"{key}\t:\t{settingsData[key]}") 

	# Creating the Thresholds menu 
	thresholds = pm.Menu(title="Thresholds", 
					width=WIDTH, 
					height=HEIGHT, 
					theme=pm.themes.THEME_BLUE) 

	# Adjusting the default values 
	thresholds._theme.widget_font_size = 25
	thresholds._theme.widget_font_color = BLACK 
	thresholds._theme.widget_alignment = pm.locals.ALIGN_LEFT 

    	# Range slider that lets to choose a value using a slider 
	thresholds.add.range_slider(title="Up tilt Threshold", default=60, range_values=( 
		50, 100), increment=1, value_format=lambda x: str(int(x)), rangeslider_id="upThreshold") 
	thresholds.add.label(title="") 
	
	thresholds.add.range_slider(title="Down tilt Threshold", default=60, range_values=( 
    	50, 100), increment=1, value_format=lambda x: str(int(x)), rangeslider_id="downThreshold") 
	thresholds.add.label(title="") 
	
	thresholds.add.range_slider(title="Left tilt Threshold", default=60, range_values=( 
		50, 100), increment=1, value_format=lambda x: str(int(x)), rangeslider_id="leftThreshold") 
	thresholds.add.label(title="") 
	
	thresholds.add.range_slider(title="Right tilt Threshold", default=60, range_values=( 
		50, 100), increment=1, value_format=lambda x: str(int(x)), rangeslider_id="rightThreshold") 
	thresholds.add.label(title="") 	

    #Button to restore Threshold defaults
	thresholds.add.button(title="Restore Defaults", action=thresholds.reset_value, 
						align=pm.locals.ALIGN_CENTER) 
	
    # Creating the Mapping menu 
	mapping = pm.Menu(title="Gesture Mapping", 
					width=WIDTH, 
					height=HEIGHT, 
					theme=pm.themes.THEME_BLUE) 
	
    	# Adjusting the default values 
	mapping._theme.widget_font_size = 25
	mapping._theme.widget_font_color = BLACK 
	mapping._theme.widget_alignment = pm.locals.ALIGN_LEFT 
	
       	# Range slider that lets to choose a value using a slider 
	mapping.add.dropselect(title="Up Tilt", items=actions, 
                            dropselect_id="upTilt", default=0)
	mapping.add.label(title="") 	
	
	mapping.add.dropselect(title="Down Tilt", items=actions, 
                            dropselect_id="downTilt", default=1)
	mapping.add.label(title="")
	
	mapping.add.dropselect(title="Left Tilt", items=actions, 
                            dropselect_id="leftTilt", default=2)
	mapping.add.label(title="")
	
	mapping.add.dropselect(title="Right Tilt", items=actions, 
                            dropselect_id="rightTilt", default=3)
	mapping.add.label(title="")
	



	mapping.add.button(title="Restore Defaults", action=mapping.reset_value, 
					align=pm.locals.ALIGN_CENTER) 



	# Creating the main menu 
	mainMenu = pm.Menu(title="AccessiMove", 
					width=WIDTH, 
					height=HEIGHT, 
					theme=pm.themes.THEME_BLUE) 

	# Adjusting the default values 
	mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER 

	# Button that takes to the settings menu when clicked 
	mainMenu.add.button(title="Thresholds", action=thresholds, 
						font_color=WHITE, background_color=LIGHT_BLUE) 

	# An empty label that is used to add a seperation between the two buttons 
	mainMenu.add.label(title="") 

	# Exit button that is used to terminate the program 
	mainMenu.add.button(title="Gesture Mapping", action=mapping, 
						font_color=WHITE, background_color=LIGHT_BLUE) 

	# Lets us loop the main menu on the screen 
	mainMenu.mainloop(screen) 


if __name__ == "__main__": 
	main() 