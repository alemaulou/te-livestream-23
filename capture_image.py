# import necessary modules
from time import sleep
from picamera import PiCamera
from pynput import keyboard
from datetime import datetime

# set some constants
TIME_LAPSE =  5 # 5 Seconds between shots
TIME_LAPSE_PICTURES = 10 # Number of pictures to snap
BURST = 5 #set number of pics to take in burst mode
PATH = "/home/pi/Desktop/Picamera/captured/"

# set up the camera with a specific resolution
cam = PiCamera()
cam.resolution = (1024, 768)

# define a function to take a single picture
def take_pic():
    global cam, PATH
    
    # get the current date and time for the filename
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    file_name = date_time + ".jpg"
    
    # display the file name and start the camera preview
    print(file_name)
    cam.start_preview()
    
    # wait a couple seconds for the camera to adjust and then capture the image
    sleep(2)
    cam.capture(PATH+file_name)
    
    # stop the preview
    cam.stop_preview()

# define a function to take a burst of pictures
def take_burst():
    pass

# define a function for the time lapse mode
def time_lapse():
    # loop for the number of pictures specified in the constant TIME_LAPSE_PICTURES
    for i in range(TIME_LAPSE_PICTURES):
        # wait the specified time between pictures
        sleep(TIME_LAPSE)
        
        # get the current date and time to create a new folder for this time lapse set
        now = datetime.now()
        new_directory = now.strftime("%m-%d-%Y-%H:%M")
        file_path = PATH+new_directory
        
        # capture the image and display the number of the picture taken
        cam.capture('/{0:04d}.jpg'.format(i+1))
        print("shot {} taken".format(i+1))

# define a function to handle key press events
def on_press(key):
    #print(key)
    
    # if the 't' key is pressed, enter time lapse mode
    if key.char == 't':
        print("time lapse")
        time_lapse()
        
    # if the space bar is pressed, take a single picture
    if 'char' in dir(key): 
        if key == keyboard.Key.space:
            take_pic()

# create a listener for key press events
listener = keyboard.Listener(on_press=on_press)
listener.start()

# loop indefinitely to keep the program running
while True:
    pass