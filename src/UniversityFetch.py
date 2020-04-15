import requests
import os
import subprocess
import shutil
import sys
import logging

from bs4 import BeautifulSoup

# from . import loggerSetup


class UniFetchNotifications():

    def __init__(self, link, destination):

        self.link = link
        self.destFolder = destination
        self.connected = False
        self.textFilePath = os.path.join(self.destFolder,'Notifications.txt')
        self.notifications = {}
        self.pdfLinks = []

        logger.debug(f"Text File Path : ",self.textFilePath)

        if not os.path.isdir(self.destFolder):
            logger.info("Destination folder does not exist... Creating new one...")
            os.mkdir(self.destination)
            logger.info(f"New folder created as : {self.destFolder}")

        self.checkConnection()

    def checkConnection(self):

        checkConnected = requests.get(self.link).status_code
        self.connected = True if checkConnected == 200 else False
        if not self.connected:
            logger.warning("Unable to connect. Please check your connection.")

    def fetchNotifications(self):

        if self.connected:
            soup = BeautifulSoup(requests.get(self.link).text, 'lxml')
            notificationPanel = soup.find('ul', class_='list-aggregate')

            for item in notificationPanel.find_all('li', class_='marquee'):

                temp = item.find_all('p')


                if not (temp[0].text.strip('\r\n').strip()) in self.notifications.keys():
                    self.notifications[temp[0].text.strip('\r\n').strip()] = []

                self.notifications[temp[0].text.strip('\r\n').strip()].append(temp[1].text)

                try:
                    self.pdfLinks.append(temp[1].a['href'])
                    self.notifications[temp[0].text.strip('\r\n').strip()].append(temp[1].a['href'])
                except TypeError:
                    self.notifications[temp[0].text.strip('\r\n').strip()].append("PDF Not provided in the Notifications.")


            logger.info("Notifications fetched successfully..")
        else:
            logger.warning("Please check your connections.")

    @property
    def printNotifications(self):

        logger.debug(self.notifications.items())
        for date,values in self.notifications.items():

            i = 0
            while(i<len(values)):
                print()
                print("#"*75)
                print(f"Date \t\t: \t{date}")
                print(f"Notification \t: \t{values[i]}")
                print(f"PDF Link \t: \t{values[i+1]}")
                print("#"*75)
                print()
                i+=2


    @property
    def generateTextFile(self):

        logger.info("Writing the text file...")
        with open(self.textFilePath, 'w') as f:

            for date, values in self.notifications.items():

                i = 0
                while (i<len(values)):
                    f.write(f'{date} : \t{values[i]}\n')
                    f.write(f'PDF Link : \t{values[i+1]}')
                    f.write('\n\n\n')
                    i+=2;

        logger.info("Done writing the text file...")
        subprocess.call(['notepad.exe', self.textFilePath])

    @property
    def getPdfFiles(self):

        logger.info("Getting PDF names...")

        for date, values in self.notifications.items():

            i = 0
            while (i<len(values)):
                print()
                print("#"*75)
                print(f"Fetching pdf {date}.pdf...")
                if ('http' in values[i+1]):
                    # logger.debug(values[i+1])
                    with requests.get(values[i+1], stream=True) as r:
                        with open(os.path.join(self.destFolder, f"{date}_{i}.pdf"), 'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                    print(f"File {date}.pdf saved.")
                    print("#"*75)
                    print()
                else:
                    print("There's no valid PDF link for this notification.")
                    print("#"*75)
                    print()
                i+=2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] : %(name)s - %(levelname)s - %(message)s')

cnsl_handler = logging.StreamHandler()
cnsl_handler.setLevel(logging.INFO)
cnsl_handler.setFormatter(formatter)

file_handler = logging.FileHandler('FetchData.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logger.addHandler(cnsl_handler)
logger.addHandler(file_handler)

logger.info("Program Started...")




if __name__ == '__main__':

    args = sys.argv

    CWD = os.getcwd()
    dest_local_folder_name = 'Data'
    DESTINATION = os.path.join(os.path.split(CWD)[0],dest_local_folder_name)
    UNIVERSITY_LINK = "http://gtu.ac.in/"

    sess = UniFetchNotifications(UNIVERSITY_LINK, DESTINATION)
    sess.fetchNotifications()
    if args[1] == '1':
        sess.printNotifications
    elif args[1] == '2':
        sess.generateTextFile
    elif args[1] == '3':
        # sess.generateTextFile
        sess.getPdfFiles
