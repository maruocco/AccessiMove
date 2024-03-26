#Jack Duggan
# Customizable gesture mapping and thresholds a basic settings menu 

import pygame 
import pygame_menu as pm 
import os  # Import the os module for file operations

class SettingsMenu:
    def __init__(self, width=900, height=700):
        pygame.init()
        pygame.display.set_caption("Settings")
        self.WIDTH = width
        self.HEIGHT = height
        #self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))   OPENS MENU ON START UP
        self.file_path = "thresholds.txt"  # File path for saving threshold values

        # Standard RGB colors
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.CYAN = (0, 100, 100)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.LIGHT_BLUE = (173, 216, 230)

    def main(self):
        # List that is displayed while selecting the graphics level
        actions = [("Up Arrow Key", "U_ak"),
                   ("Down Arrow Key", "D_ak"),
                   ("Left Arrow Key", "L_ak"),
                   ("Right Arrow Key", "R_ak"),
                   ("Open OSK", "O_osk"),
                   ("Close OSK", "C_osk")]

        # Creating the Thresholds menu
        thresholds = pm.Menu(title="Thresholds",
                             width=self.WIDTH,
                             height=self.HEIGHT,
                             theme=pm.themes.THEME_BLUE)

        # Adjusting the default values
        thresholds._theme.widget_font_size = 25
        thresholds._theme.widget_font_color = self.BLACK
        thresholds._theme.widget_alignment = pm.locals.ALIGN_LEFT

        # Range slider that lets to choose a value using a slider
        thresholds.add.range_slider(title="Up tilt Threshold", default=10, range_values=(5, 20), increment=1,
                                    value_format=lambda x: str(int(x)), rangeslider_id="upThreshold")
        thresholds.add.label(title="")

        thresholds.add.range_slider(title="Down tilt Threshold", default=10, range_values=(5, 20), increment=1,
                                    value_format=lambda x: str(int(x)), rangeslider_id="downThreshold")
        thresholds.add.label(title="")

        thresholds.add.range_slider(title="Left tilt Threshold", default=10, range_values=(5, 20), increment=1,
                                    value_format=lambda x: str(int(x)), rangeslider_id="leftThreshold")
        thresholds.add.label(title="")

        thresholds.add.range_slider(title="Right tilt Threshold", default=10, range_values=(5, 20), increment=1,
                                    value_format=lambda x: str(int(x)), rangeslider_id="rightThreshold")
        thresholds.add.label(title="")

        # Button to restore Threshold defaults
        thresholds.add.button(title="Restore Defaults", action=thresholds.reset_value, align=pm.locals.ALIGN_CENTER)

        # Adding Save Button to save the values of sliders
        thresholds.add.button(title="Save", action=lambda: self.save_values(self.file_path, thresholds),
                              align=pm.locals.ALIGN_CENTER)

        # Creating the Mapping menu
        mapping = pm.Menu(title="Gesture Mapping",
                          width=self.WIDTH,
                          height=self.HEIGHT,
                          theme=pm.themes.THEME_BLUE)

        # Adjusting the default values
        mapping._theme.widget_font_size = 25
        mapping._theme.widget_font_color = self.BLACK
        mapping._theme.widget_alignment = pm.locals.ALIGN_LEFT

        # Range slider that lets to choose a value using a slider
        mapping.add.dropselect(title="Up Tilt", items=actions, dropselect_id="upTilt", default=0)
        mapping.add.label(title="")

        mapping.add.dropselect(title="Down Tilt", items=actions, dropselect_id="downTilt", default=1)
        mapping.add.label(title="")

        mapping.add.dropselect(title="Left Tilt", items=actions, dropselect_id="leftTilt", default=2)
        mapping.add.label(title="")

        mapping.add.dropselect(title="Right Tilt", items=actions, dropselect_id="rightTilt", default=3)
        mapping.add.label(title="")

        mapping.add.button(title="Restore Defaults", action=mapping.reset_value, align=pm.locals.ALIGN_CENTER)

        # Creating the main menu
        mainMenu = pm.Menu(title="AccessiMove",
                           width=self.WIDTH,
                           height=self.HEIGHT,
                           theme=pm.themes.THEME_BLUE)

        # Button that takes to the settings menu when clicked
        mainMenu.add.button(title="Thresholds", action=thresholds, font_color=self.WHITE,
                            background_color=self.LIGHT_BLUE)

        # An empty label that is used to add a separation between the two buttons
        mainMenu.add.label(title="")

        # Exit button that is used to terminate the program
        mainMenu.add.button(title="Gesture Mapping", action=mapping, font_color=self.WHITE,
                            background_color=self.LIGHT_BLUE)

        # Lets us loop the main menu on the screen
        mainMenu.mainloop(self.screen)

    def save_values(self, file_path, thresholds):
        # Getting the data from the thresholds menu
        thresholdsData = thresholds.get_input_data()

        # Accessing the values of the sliders and saving them to a file
        with open(file_path, 'w') as file:
            file.write(f"upTiltThreshold={thresholdsData['upThreshold']}\n")
            file.write(f"downTiltThreshold={thresholdsData['downThreshold']}\n")
            file.write(f"leftTiltThreshold={thresholdsData['leftThreshold']}\n")
            file.write(f"rightTiltThreshold={thresholdsData['rightThreshold']}\n")

        # Saving values to a file or any other desired operation
        print("Values saved successfully!")
        print("Up Tilt Threshold:", thresholdsData['upThreshold'])
        print("Down Tilt Threshold:", thresholdsData['downThreshold'])
        print("Left Tilt Threshold:", thresholdsData['leftThreshold'])
        print("Right Tilt Threshold:", thresholdsData['rightThreshold'])

    def load_threshold_values(self, file_path):
        # Read threshold values from the file
        threshold_values = {}
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                threshold_values[key.strip()] = float(value.strip())
        return threshold_values
    
    def show_menu(self):
        # Display the settings menu
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        self.main()

if __name__ == "__main__":
    settings_menu = SettingsMenu()
    settings_menu.main()

