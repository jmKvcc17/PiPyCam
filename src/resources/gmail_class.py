from __future__ import print_function
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

# User imports
from resources import const_vars
from resources import logging_custom

logger = logging_custom.get_logger(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
EMAIL = const_vars.EMAIL


class GmailClass():
    def __init__(self):

        self.sender = 'me'
        self.email = EMAIL
        self.subject = 'PiCam Error'

        logger.info('Creating GMail object...')

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    # 'credentials.json', SCOPES)
                    'src/resources/email.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail',
                            'v1',
                            credentials=creds,
                            cache_discovery=False)

        logger.info('Gmail object created.')

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

          Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

          Returns:
        An object containing a base64 encoded email object.
        """

        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode()
        body = {'raw': b64_string}
        return body

    def send_message(self, service, user_id, message):
        """Send an email message.
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

        Returns:
        Sent Message.
        """
        try:
            message = (self.service.users().messages().send(userId=user_id,
                body=message).execute())
            print('Message ID: '.format(message['id']))
            return message
        except Exception as error:
            print('An error occured: {0}'.format(error))


    def send_email(self, message_body=None):

        if message_body is None:
            logger.warn('Error. Need message body for email.')
        else:
            message = self.create_message(
                self.sender,
                self.email,
                self.subject,
                message_body)

            self.send_message(self.service, self.sender, message)



