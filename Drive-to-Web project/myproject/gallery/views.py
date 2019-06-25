from django.shortcuts import render
from django.http import HttpResponse

# modules needed for google drive authentication
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def home (request):
    # return render(request, 'index.html',{'name':'jagan'})
    # return render(request,'home.html',{'name':'https://drive.google.com/embeddedfolderview?id=1ALxcKlINVfUWFMcALOTtB4IswVok1X5W#grid'})

    myDict = {}
    def main():
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
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
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        image_links = []
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                # condition to match the pubic folder of my drive
                if item['name']=='My_images':
                    myDict['folderLink']=("https://drive.google.com/embeddedfolderview?id="+ item['id'] +"#grid")
                    
                    # to extract the file id of all images inside the public folder
                    query = "'{}' in parents".format(item['id'])
                    children = service.files().list(q=query, 
                        fields='nextPageToken, files(id, name)').execute() # accessing the child images of 'Images' folder.

                    images_files = children['files'] # list of all the images
                    for i in images_files:
                        # appending the urls into a list image_link by creating url using Id
                        image_links.append('https://drive.google.com/uc?export=view&id={}'.format(i['id'])) 
            # appendinng the image link list into dictionary and returning to the function
            myDict['image_links']=image_links
            return(myDict)
            
    # rendering the urls
    return render(request,'home.html',{'imgLink':main()['image_links'],'folderLink':main()['folderLink']})


