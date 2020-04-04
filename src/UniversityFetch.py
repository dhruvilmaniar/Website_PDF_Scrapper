import requests
import os
import subprocess
import shutil
from bs4 import BeautifulSoup


class UniversityFetchData():

    def __init__(self, link, destination):

        self.link = link
        self.destFolder = destination
        self.connected = False
        self.textFilePath = os.path.join(self.destFolder,'Notifications.txt')
        self.notifications = {}
        self.pdfLinks = []

        if not os.path.isdir(destination):
            print("Destination folder does not exist... Creating new one...")
            os.mkdir(destination)

        self.checkConnection()

    def checkConnection(self):

        checkConnected = requests.get(self.link).status_code
        self.connected = True if checkConnected == 200 else False
        if not self.connected:
            print("Unable to connect. Please check your connection.")

    def fetchNotifications(self):

        if self.connected:
            soup = BeautifulSoup(requests.get(self.link).text, 'lxml')
            notificationPanel = soup.find('ul', class_='list-aggregate')

            for item in notificationPanel.find_all('li', class_='marquee'):

                temp = item.find_all('p')
                self.pdfLinks.append(temp[1].a['href'])

                if not (temp[0].text.strip('\r\n').strip()) in self.notifications.keys():
                    self.notifications[temp[0].text.strip('\r\n').strip()] = []

                self.notifications[temp[0].text.strip('\r\n').strip()].append(temp[1].text)
                self.notifications[temp[0].text.strip('\r\n').strip()].append(temp[1].a['href'])

            print("Notifications fetched successfully..")
        else:
            print("Please check your connections.")

    @property
    def printNotifications(self):

        for date,values in self.notifications.items():

            print()
            print("#"*75)
            print(f"Date \t\t: \t{date}")
            print(f"Notification \t: \t{values[0]}")
            print(f"PDF Link \t: \t{values[1]}")
            print("#"*75)
            print()

    @property
    def generateTextFile(self):

        print("Writing the text file...")
        with open(self.textFilePath, 'w') as f:

            for date, values in self.notifications.items():

                f.write(f'{date} : \t{values[0]}\n')
                f.write(f'PDF Link : \t{values[1]}')
                f.write('\n\n\n')

        print("Done writing the text file...")
        subprocess.call(['notepad.exe', self.textFilePath])

    @property
    def getPdfFiles(self):

        print("Getting PDF names...")

        for date, values in self.notifications.items():

            print()
            print("#"*75)
            print(f"Fetching pdf {date}.pdf...")
            with requests.get(values[1], stream=True) as r:
                with open(os.path.join(self.destFolder, f"{date}.pdf"), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print(f"File {date}.pdf saved.")
            print("#"*75)
            print()



if __name__ == '__main__':

    CWD = os.getcwd()
    dest_local_folder_name = 'Data'
    DESTINATION = os.path.join(os.path.split(CWD)[0],dest_local_folder_name)
    UNIVERSITY_LINK = "http://gtu.ac.in/"

    sess = UniversityFetchData(UNIVERSITY_LINK, DESTINATION)
    sess.fetchNotifications()
    sess.printNotifications
    sess.generateTextFile
    sess.getPdfFiles
