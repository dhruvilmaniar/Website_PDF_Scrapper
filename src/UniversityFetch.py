from bs4 import BeautifulSoup
import requests
import os


class UniversityFetchData():

    def __init__(self, link, destination):

        self.link = link
        self.destFolder = destination
        self.connected = False
        self.textFilePath = os.path.join(self.destFolder,'Notifications.txt')
        self.notifications = {}
        self.pdfLinks = []
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
                self.notifications[temp[0].text.strip('\r\n').strip()] = temp[1].text
            print("Notifications fetched successfully..")
        else:
            print("Please check your connections.")

    @property
    def printNotifications(self):

        for index, date in enumerate(self.notifications):

            print()
            print("#"*75)
            print(f"Date \t\t: \t{date}")
            print(f"Notification \t: \t{self.notifications[date]}")
            print(f"PDF Link \t: \t{self.pdfLinks[index]}")
            print("#"*75)
            print()

    @property
    def generateTextFile(self):

        print("Writing the text file...")
        with open(self.textFilePath, 'w') as f:

            for date, title in self.notifications.items():

                f.write(f'{date} : \t{title}')
                f.write('\n\n')

        print("Done writing the text file...")


    def getPdfFiles(self):

        print("Getting PDF names...")







if __name__ == '__main__':

    CWD = os.getcwd()
    DATA = os.path.join(os.path.split(CWD)[0],'Data')
    UNIVERSITY_LINK = "http://gtu.ac.in/"

    if not os.path.isdir(DATA):
        print("No folder named Data found. Creating new one...")
        os.mkdir(DATA)

    sess = UniversityFetchData(UNIVERSITY_LINK, DATA)
    sess.fetchNotifications()
    sess.printNotifications
    # sess.generateTextFile
