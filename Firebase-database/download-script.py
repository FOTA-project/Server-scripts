import pyrebase

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

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig);
storage = firebase.storage()
db = firebase.database()

isNewElf = db.child("isNewElf").get().val()

if isNewElf == "0":
   exit(0)

db.update({"isNewElf": "0"})

local_file_download = r'bootloader-dummy-app.elf'
cloud_file = r'test_folder/bootloader-dummy-app.elf'

# download file
storage.child(cloud_file).download(local_file_download)

exit(1)

#print("Script finished")
