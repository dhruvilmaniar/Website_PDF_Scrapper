from bs4 import BeautifulSoup
import requests
import os


class UniversityFetchData():

    def __init__(self, link, destination):

        self.link = link
        self.destFolder = destination
        self.connected = False
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

            self.notifications = {}

            for item in notificationPanel.find_all('li', class_='marquee'):

                temp = item.find_all('p')
                self.notifications[temp[0].text.strip('\r\n').strip()] = temp[1].text
            print("Notifications fetched successfully..")
        else:
            print("Please check your connections.")

    @property
    def printNotifications(self):

        for date, title in self.notifications.items():

            print()
            print("############################################################")
            print(f"Date : \t{date}")
            print(f"Notification : \t{title}")
            print("############################################################")
            print()


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
