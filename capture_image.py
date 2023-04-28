from time import sleep
from picamera import PiCamera
from pynput import keyboard
from datetime import datetime


TIME_LAPSE =  5 # 5 Seconds between shots
TIME_LAPSE_PICTURES = 10 # Number of pictures to snap

BURST = 5 #set number of pics to take in burst mode
PATH = "/home/pi/Desktop/Picamera/captured/"

cam = PiCamera()
cam.resolution = (1024, 768)




def take_pic():
    global cam, PATH
    
    now = datetime.now()
    
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    file_name = date_time + ".jpg"
    
    print(file_name)
    
    cam.start_preview()
    sleep(2)
    cam.capture(PATH+file_name)
    cam.stop_preview()
    
def take_burst():
    
    pass


def time_lapse():
    
    for i in range(TIME_LAPSE_PICTURES):
    
        sleep(TIME_LAPSE)
        now = datetime.now()
        new_directory = now.strftime("%m-%d-%Y-%H:%M") #each time lapse set gets its own folder
        file_path = PATH+new_directory
        cam.capture('/{0:04d}.jpg'.format(i+1))
        print("shot {} taken".format(i+1))
    

    
    


def on_press(key):
    #print(key)
    

        
    if key.char == 't':
        print("time lapse")
        time_lapse()
        
        
    if 'char' in dir(key): 
        if key == keyboard.Key.space:
            take_pic()
        
    
     
    
       
     
  

listener = keyboard.Listener(on_press=on_press)
listener.start()


while True:
    pass