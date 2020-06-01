# Server-scripts
A collection of scripts related to the server holding the .ELF file

## Server link: [Firebase](https://console.firebase.google.com/project/fota-server-b4148/)

## References
[Firebase docs](https://firebase.google.com/docs/guides)

## Install [Pyrebase](https://github.com/thisbejim/Pyrebase)
1. Uninstall everything 1st to avoid old versions errors
   ```bash
   sudo pip uninstall -y gax-google-logging-v2
   sudo pip uninstall -y google-gax
   sudo pip uninstall -y gax-google-pubsub-v1
   sudo pip uninstall -y requests
   sudo pip uninstall -y python_jwt
   sudo pip uninstall -y python-jwt
   sudo pip uninstall -y gcloud
   sudo pip uninstall -y pycryptodome
   sudo pip uninstall -y requests-toolbelt
   sudo pip uninstall -y jws
   sudo pip uninstall -y grpc-google-pubsub-v1
   sudo pip uninstall -y google-auth
   sudo pip uninstall -y grpc-google-logging-v2
   sudo pip uninstall -y oauth2client
   sudo pip uninstall -y googleapis-common-protos
    
   sudo pip3 uninstall -y gax-google-logging-v2
   sudo pip3 uninstall -y google-gax
   sudo pip3 uninstall -y gax-google-pubsub-v1
   sudo pip3 uninstall -y requests
   sudo pip3 uninstall -y python_jwt
   sudo pip3 uninstall -y python-jwt
   sudo pip3 uninstall -y gcloud
   sudo pip3 uninstall -y pycryptodome
   sudo pip3 uninstall -y requests-toolbelt
   sudo pip3 uninstall -y jws
   sudo pip3 uninstall -y grpc-google-pubsub-v1
   sudo pip3 uninstall -y google-auth
   sudo pip3 uninstall -y grpc-google-logging-v2
   sudo pip3 uninstall -y oauth2client
   sudo pip3 uninstall -y googleapis-common-protos
   ```
2. Uninstall previous installations of the Pyrebase package
   ```bash
   sudo pip uninstall -y pyrebase
   sudo pip3 uninstall -y pyrebase
   ```
3. Upgrade `pip`
   ```bash
   python2 -m pip install --upgrade pip
   python3 -m pip install --upgrade pip
   ```
4. Install Pyrebase for Python 3
   ```bash
   sudo pip3 install pyrebase
   ```
