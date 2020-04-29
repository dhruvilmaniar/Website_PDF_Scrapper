import requests
import os
import subprocess
import shutil
import sys
import logging
from datetime import datetime

from bs4 import BeautifulSoup

from .loggerSetup import get_logger

class UniFetchNotifications():

    def __init__(self, link, destination):

        self.link = link
        self.destFolder = destination
        self.connected = False
        self.textFilePath = os.path.join(self.destFolder,'Notifications.txt')
        self.fetchLogsFilePath = os.path.join(self.destFolder, 'FetchLogs.log')
        self.notifications = {}
        self.pdfLinks = []

        logger.debug(f"Text File Path : {self.textFilePath}")

        if not os.path.isfile(self.fetchLogsFilePath):
            with open(self.fetchLogsFilePath, 'w'): pass


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


            self.latestNotificationDate = datetime.strptime(next(iter(self.notifications.keys())), '%d-%b-%Y')
            logger.info("Notifications fetched successfully..")
        else:
            logger.warning("Please check your connections.")

    @property
    def printNotificationsAll(self):

        # logger.debug(self.notifications.items())
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

        with open(self.fetchLogsFilePath, 'w') as f:
            f.write(next(iter(self.notifications.keys())))
            logger.info(f"Last Seen date Updated to {next(iter(self.notifications.keys()))}")


    @property
    def printNotificationsUpdates(self):

        with open(self.fetchLogsFilePath, 'r') as f:

            lastReadDateStr = f.readline().rstrip('\n')
            if lastReadDateStr == '':
                lastReadDateStr = "01-Jan-2020"
                logger.info("No last seen date found.")
                logger.info("Showing all notifications from beginnig of the year...")
            lastReadDate = datetime.strptime(lastReadDateStr, '%d-%b-%Y')

        difference = (self.latestNotificationDate - lastReadDate).days

        if difference>=7:

            for date,values in self.notifications.items():
                logger.debug(datetime.strptime(date, '%d-%b-%Y'), lastReadDate, (datetime.strptime(date, '%d-%b-%Y') - lastReadDate).days)

                # -1 so that we can see the last seen notification also.
                if ((datetime.strptime(date, '%d-%b-%Y') - lastReadDate).days >= -1):
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

        else:

            logger.info("No new notifications.")

        with open(self.fetchLogsFilePath, 'w') as f:
            f.write(next(iter(self.notifications.keys())))
            logger.info(f"Last Seen date Updated to {next(iter(self.notifications.keys()))}")

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



if __name__ == '__main__':

    args = sys.argv

    CWD = os.getcwd()
    dest_local_folder_name = 'Data'
    DESTINATION = os.path.join(CWD,dest_local_folder_name)
    UNIVERSITY_LINK = "http://gtu.ac.in/"
    LOG_FILE_PATH = os.path.join(DESTINATION, 'UniversityFetch.log')

    if not os.path.isdir(DESTINATION):
        logger.info("Destination folder does not exist... Creating new one...")
        os.mkdir(DESTINATION)
        logger.info(f"New folder created as : {DESTINATION}")

    logger = get_logger(__name__, LOG_FILE_PATH)
    logger.info("Program Started...")

    logger.debug(LOG_FILE_PATH)

    sess = UniFetchNotifications(UNIVERSITY_LINK, DESTINATION)
    sess.fetchNotifications()
    if args[1] == '1':
        logger.info("Showing output to the console only..")
        sess.printNotificationsUpdates
    elif args[1] == '2':
        logger.info("Showing all the notifications to the console only...")
        sess.printNotificationsAll
    elif args[1] == '3':
        logger.info("Showing output to a text file..")
        sess.generateTextFile
    elif args[1] == '4':
        logger.info("Downloading all the PDF files..")
        # sess.generateTextFile
        sess.getPdfFiles
