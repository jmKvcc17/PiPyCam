from pydrive.auth import GoogleAuth

try:
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
except Exception as err:
    print(err)

