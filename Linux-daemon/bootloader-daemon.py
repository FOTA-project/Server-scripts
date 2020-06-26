import pyrebase
import time
import subprocess
import threading
import RPi.GPIO as GPIO
import tkinter as tk
from ELF_Parser import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *


GPIO.cleanup()

ResetPin = 23
BootPin  = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(ResetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(ResetPin, GPIO.IN)
GPIO.setup(BootPin, GPIO.OUT)
GPIO.output(BootPin, GPIO.LOW)
#GPIO.output(ResetPin, GPIO.HIGH)

firebaseConfig = {
    "apiKey": "AIzaSyBgBFhNa6OnJCLbFTQW3vF_Cyz-rMyN4vU",
    "authDomain": "fota-server-b4148.firebaseapp.com",
    "databaseURL": "https://fota-server-b4148.firebaseio.com",
    "projectId": "fota-server-b4148",
    "storageBucket": "fota-server-b4148.appspot.com",
    "messagingSenderId": "774423425890",
    "appId": "1:774423425890:web:f506832444c3d30b2c323b",
    "measurementId": "G-2DE9D9TN6N"
};

email = r"fota_project_gp_iti@gmail.com"
password = r"12345@ITI"

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig);
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
user = auth.sign_in_with_email_and_password(email, password)
user = auth.refresh(user['refreshToken'])

user_uid = ''
user_tokenId = ''

local_file_download = r'file.elf'

INSTRUCTION_GET_PROGRESS_FLAG     = -1
#INSTRUCTION_COMM_TIMEOUT          = -2
INSTRUCTION_TERMINATE_ON_SUCCESS  = -3
INSTRUCTION_WRITE_MAX_REQUESTS    = -4
#INSTRUCTION_GET_PROGRESS_FLAG_ARB = -5

RPI_COMM_ERROR_SUCCESS                        =  0
RPI_COMM_ERROR_COULDNT_OPEN_UART              = -1
RPI_COMM_ERROR_COULDNT_OPEN_INFO_FILE         = -2
RPI_COMM_ERROR_COULDNT_OPEN_DATA_FILE         = -3
RPI_COMM_ERROR_COULDNT_OPEN_TEXT_FILE         = -4
RPI_COMM_ERROR_COULDNT_OPEN_INSTRUCTIONS_FILE = -5
RPI_COMM_ERROR_COULDNT_OPEN_PROGRESS_FILE     = -6
RPI_COMM_ERROR_ACK_TIMEDOUT                   = -7
RPI_COMM_ERROR_APP_SIZE_LARGE                 = -8

rpiCommError = 0

isTerminate = 0

# syncchronization semaphore
isTokenRefreshThreadActive = 0


def User_TokenRefresh_Thread():
    global user
    global isTokenRefreshThreadActive
    
    while True:
        isTokenRefreshThreadActive = 1
        user = auth.refresh(user['refreshToken']) # get a new token
        isTokenRefreshThreadActive = 0
        time.sleep(1800) # sleep 30min


def User_LifeRefresher_Thread():
    global user
    global user_uid
    global user_tokenId
    global isTokenRefreshThreadActive
    
    user_uid = user['userId']
    
    user_top_db = "users/" + user_uid
    
    prevLifeFlag = -1
    
    while True:
        # wait 200ms
        time.sleep(0.2)
        
        # we should attempt to get user data (uid, token) if it's being refreshed
        if isTokenRefreshThreadActive == 1:
            continue

        user_tokenId = user['idToken']
        
        # get LifeFlag flag from database
        LifeFlag = db.child(user_top_db + "/LifeFlag").get(user_tokenId).val()
        
        if LifeFlag == prevLifeFlag: # if no life change happened!
            continue
        
        # toggle the flag
        LifeFlag = LifeFlag ^ 1
        
        # update the previous flag indicator
        prevLifeFlag = LifeFlag
        
        # update the flag in database
        db.child(user_top_db).update({"LifeFlag" : LifeFlag}, user_tokenId)


def RPi_Comm_Thread():
    global rpiCommError
    global RPI_COMM_ERROR_SUCCESS

    rpiCommError = subprocess.call('./a')
    if rpiCommError != RPI_COMM_ERROR_SUCCESS:
        rpiCommError = rpiCommError- 256 # convert to signed
    #print("rpiCommError = %d" %(rpiCommError))


# user token refresher
tokenThreadHandle = threading.Thread(target = User_TokenRefresh_Thread)
tokenThreadHandle.daemon = True # set this thread as daemon so that sys.exit() won't be blocked
tokenThreadHandle.start()

time.sleep(2)

# user life flag refresher
lifeThreadHandle = threading.Thread(target = User_LifeRefresher_Thread)
lifeThreadHandle.daemon = True # set this thread as daemon so that sys.exit() won't be blocked
lifeThreadHandle.start()


while True:
    time.sleep(0.4) # sleep 0.4 sec = 400 ms
    
    # we should attempt to get user data (uid, token) if it's being refreshed
    if isTokenRefreshThreadActive == 1:
        continue
    
    user_uid = user['userId']
    user_tokenId = user['idToken']

    cloud_file = "users/" + user_uid + "/file.elf"

    user_db = "users/" + user_uid + "/STM32"

    # get isNewElf flag from database
    isNewElf = db.child(user_db + "/isNewElf").get(user_tokenId).val()

    if isNewElf == 0: # if no new ELF file loop back again
       continue

    # download file
    storage.child(cloud_file).download(local_file_download, user_tokenId)

    # reset isNewElf flag in database
    db.child(user_db).update({"isNewElf" : 0}, user_tokenId)
    
    # parse the downloaded file
    ParseElfFile(r'file.elf')

    # create last-progress.txt
    lastProgressFile = open('last-progress.txt', 'w')
    lastProgressFile.close()
    
    # create progress.txt
    progressInstructionFile = open('progress.txt', 'w')
    progressInstructionFile.close()
    
    progressInstructionFile = open('progress.txt', 'rb')
    progressInstructionFile.seek(0, 0)
    
    # ask the user if they want to apply the update
    # create a hidden tkinter window to be used for user consent on  new update
    # source: https://runestone.academy/runestone/books/published/thinkcspy/GUIandEventDrivenProgramming/02_standard_dialog_boxes.html
    ask_for_update_window = tk.Tk()
    ask_for_update_window.withdraw()

    userAcceptedUpdate = messagebox.askyesno("New software update", "There's a new software update, it's highly recommended to apply it, do you want to continue ?", parent = ask_for_update_window)
    
    # destroy the window because it's kept even if the user pressed anything
    ask_for_update_window.destroy()

    # update isUserAcceptedUpdate flag in database so the GUI could continue
    db.child(user_db).update({"isUserAcceptedUpdate" : int(userAcceptedUpdate)}, user_tokenId)
    
    if userAcceptedUpdate == False: # if user denied the update
        db.child(user_db).update({"lastErrorCode" : RPI_COMM_ERROR_SUCCESS}, user_tokenId)
        progressInstructionFile.close()
        continue

    # spawn updating progress window
    updatingWindow = tk.Tk(className = ' Updating progress ')
    updatingWindow.geometry("525x85")
    updatingWindow.resizable(0, 0) # don't allow resizing in the x or y direction

    updatingLabel = Label(updatingWindow, text = "Applying new update...", font = ('', 18), justify = CENTER)
    extraLine = Label(updatingWindow, text = " ", font = ('arial', 8))

    updatingWindowProgress = Progressbar(updatingWindow, orient = 'horizontal', length = 500, mode = 'determinate')
    updatingWindowProgress['value'] = 0

    updatingLabel.pack()
    extraLine.pack()
    updatingWindowProgress.pack()

    updatingWindow.update_idletasks()

    # call RPi communicator
    commThreadHandle = threading.Thread(target = RPi_Comm_Thread)
    commThreadHandle.start()
    
    # set BOOT1 pin to 1
    GPIO.output(BootPin, GPIO.HIGH)
    
    # do reset sequence
    GPIO.setup (ResetPin, GPIO.OUT)
    GPIO.output(ResetPin, GPIO.LOW)
    time.sleep(0.001) # 1ms
    GPIO.setup(ResetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # wait 5ms, then clear BOOT1 pin
    time.sleep(0.005) # 5ms
    GPIO.output(BootPin, GPIO.LOW)
   
    elfProgress = db.child(user_db + "/elfProgress").get(user_tokenId).val()

    maxRequsets = 0
    currentProgress = 0

    while isTerminate == 0:
        line = progressInstructionFile.readline().decode('utf-8').strip()
        #print("line = %s\n" %(line))
        
        if line == '':
            time.sleep(0.001 * 50) # 50ms
            #print("line is empty")
            #progressInstructionFile.seek(-len(prevLine), 2)
            continue
        
        if int(line[:2], 10) == INSTRUCTION_TERMINATE_ON_SUCCESS:
            isTerminate = 1
            #print("isTerminate = 1\n")
        elif int(line[:2], 10) == INSTRUCTION_WRITE_MAX_REQUESTS:
            maxRequsets = int(line.split()[1], 10)
            db.child(user_db).update({"elfProgressMaxRequest" : maxRequsets}, user_tokenId)
            #print("INSTRUCTION_WRITE_MAX_REQUESTS, %d\n" %(int(line.split()[1], 10)))
        elif int(line[:2], 10) == INSTRUCTION_GET_PROGRESS_FLAG:
            # goto position of requests count, and fill it from server
            #print("writing old progress = %d\n" %(elfProgress))
            lastProgressFile = open('last-progress.txt', 'r+')
            lastProgressFile.seek(0)
            lastProgressFile.write("00%d\n" %(elfProgress))
            #print("done\n")
            lastProgressFile.close()
        else: # normal +ve number
            currentProgress = int(line, 10)
            db.child(user_db).update({"elfProgress" : currentProgress}, user_tokenId)
            updatingWindowProgress['value'] = 100 * currentProgress / maxRequsets
            updatingWindow.update_idletasks()
            #print("normal number, %d\n" %(int(line, 10)))
    
    progressInstructionFile.close()
    updatingWindow.destroy()
    isTerminate = 0
    
    flashingFinalStatusWindow = tk.Tk()
    flashingFinalStatusWindow.withdraw()

    if rpiCommError == RPI_COMM_ERROR_SUCCESS:
        db.child(user_db).update({"lastErrorCode" : RPI_COMM_ERROR_SUCCESS}, user_tokenId)
        messagebox.showinfo("Update succeeded", "Successfully applied the new update!")
    else:
        userWantsToReport = messagebox.askyesno("Update failed", "There was an error during the update (error code = %d), send a report ?" %(rpiCommError), parent = flashingFinalStatusWindow)
        if userWantsToReport:
            db.child(user_db).update({"lastErrorCode" : rpiCommError}, user_tokenId)
        else:
            db.child(user_db).update({"lastErrorCode" : RPI_COMM_ERROR_SUCCESS}, user_tokenId)

    # destroy the window because it's kept even if the user pressed anything
    flashingFinalStatusWindow.destroy()

    #####commThreadHandle.stop() #############

