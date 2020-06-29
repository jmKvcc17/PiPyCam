from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from resources import const_vars
from resources import gmail_class
from resources import logging_custom

GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = const_vars.CLIENT_SECRETS_PATH
logger = logging_custom.get_logger(__name__)


# Uploads a file to google drive
class DriveUp:

    def __init__(self,
        filePath=None,
        dir_queue=None,
        run_processes_bool=None):

        self.filePath = filePath
        self.drive = self.authorize()
        self.dir_queue = dir_queue
        self.run_processes_bool = run_processes_bool

        # Email send object
        self.gmail_object = gmail_class.GmailClass()

        self.email_bool = True

        self.num_uploaded = 0
        self.file_list = None

        # self.upload_files()

    def create_file_list(self):
        self.file_list = self.drive.ListFile(
            {'q': "'{0}' in parents and trashed=false".format(const_vars.FOLDER_ID)}
        ).GetList()

    def delete_files(self):

        if self.file_list is None:
            self.create_file_list()

        logger.info('Deleting drive images...')

        for f in self.file_list:
            f.Delete()

        self.file_list = None

        logger.info('Drive images deleted.')


    def num_files(self):

        if self.file_list is None:
            self.create_file_list()

        num_files = len(self.file_list)
        logger.info('Number of files on Google Drive: {0}'.format(num_files))

        return num_files

    def authorize(self):
        """
        Authorize with saved credentials
        """
         # vars
        user_creds = const_vars.USER_CREDS

        # Authorizes the program
        gauth = GoogleAuth()

        logger.info('STARTING AUTH')

        # try to load saved client credentials
        gauth.LoadCredentialsFile(user_creds)
        if gauth.credentials is None:
            #Authenticate with server
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh tokens
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()

        # Save credentials
        gauth.SaveCredentialsFile(user_creds)

        # create the auth google drive obj
        drive = GoogleDrive(gauth)

        return drive

    def upload_files(self):
        logger.info('Beginnging image path queue upload...')
        while self.run_processes_bool:


            new_file = self.dir_queue.get()
            file_name = new_file.strip(const_vars.MOTION_PATH)

            logger.info('Attempting file upload...')
            try:
                # Set image properties
                upFile = self.drive.CreateFile({'title': file_name,
                    'mimeType':const_vars.MIME_TYPE,
                    'parents': [{"id": const_vars.FOLDER_ID}]}
                )
                upFile.SetContentFile(new_file)
                # Upload the image
                upFile.Upload()

                if not self.email_bool:
                    self.email_bool = True

                self.num_uploaded += 1

                logger.info('Uploaded file: {0}'.format(new_file))
                logger.info('Number of images uploaded: {0}'.format(self.num_uploaded))
            except Exception as err:
                logger.warn(err)
                logger.warn('Could not upload file: {0}'.format(new_file))
                email_body = 'Could not upload file: {0}'.format(new_file)

                if self.email_bool:
                    self.gmail_object.send_email(message_body=email_body)
                    self.email_bool = False
