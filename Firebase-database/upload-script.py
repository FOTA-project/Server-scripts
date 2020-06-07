import pyrebase
import sys
from pathlib import Path


argv = sys.argv
argc = len(argv)

if argc != 2:
   exit(1)

# upload
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
user = auth.sign_in_with_email_and_password(email, password)
user = auth.refresh(user['refreshToken']) # optional

db = firebase.database()
storage = firebase.storage()

user_uid = user['userId']
user_tokenId = user['idToken']

local_file = argv[1]
cloud_file = "users/" + user_uid + "/file.elf"
isNewElf_flag = "users/" + user_uid + "/STM32"

# upload file
storage.child(cloud_file).put(local_file, user_tokenId)

# update isNewElf flag in database
db.child(isNewElf_flag).update({"isNewElf" : 1}, user_tokenId)

exit(0)

#print("Script finished")
