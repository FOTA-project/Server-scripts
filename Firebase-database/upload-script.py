import pyrebase
import sys


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

auth =firebase.auth()
email = input("enter your mail")
password = input("enter your password")
signin = auth.sign_in_with_email_and_password(email,password)
print("sigin in sucessufully")

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig);
storage = firebase.storage()
db = firebase.database()

db.update({"isNewElf": "1"})

local_file = argv[1]
cloud_file = r'test_folder/bootloader-dummy-app.elf'

# upload file
storage.child(cloud_file).put(local_file)

exit(0)

#print("Script finished")
