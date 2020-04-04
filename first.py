from bs4 import BeautifulSoup
import requests
import os


source = requests.get('http://gtu.ac.in/').text

soup = BeautifulSoup(source, 'lxml')

AnnList = soup.find('ul', class_='list-aggregate')

# headings = AnnList.find_all('p')
# # headings = {}
# print(headings)

notifications = {}

for i in AnnList.find_all('li', class_='marquee'):


    it = i.find_all('p')

    # for i in it:
    print()
    print(it[1].a['href'])
    print("#########")
    # notifications[it[0].text.strip('\r\n').strip()] = it[1].text

# for i,j in notifications.items():

#     print(f"Date : \t{i}")
#     print(f"Notification : \t{j}")
#     print()
