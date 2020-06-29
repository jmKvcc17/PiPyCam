import json

with open('/etc/PiPyCam.json') as config_file:
    config = json.load(config_file)

MOTION_PATH = '/var/lib/motion/'  # Path to where motion stores pictures

USER_CREDS = 'src/resources/mycreds.txt'  # Path to user credentials

CLIENT_SECRETS_PATH = 'src/resources/client_secrets.json'

LOG_DIR = '/var/log/PiPyCam'

EMAIL = config['EMAIL']

FOLDER_ID = config['FOLDER_ID']  # id for the picture folder

MIME_TYPE = 'image/jpeg'




