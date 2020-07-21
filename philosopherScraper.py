import time
import requests
from bs4 import BeautifulSoup as bs
import sqlite3

#after _ (A-C)
philoBaseUrl = 'https://en.wikipedia.org/wiki/List_of_philosophers_'
bioBaseUrl = 'https://en.wikipedia.org/wiki/'

letterList = ['(A-C)', '(D-H)', '(I-Q)', '(R-Z)']


philosopherNameList = []
underScoreNameList = []

nameBioDict = {}
purgeList = []

conn = sqlite3.connect('philosophybot.db')
c = conn.cursor()

def main():

  for element in letterList:
    html_text = requests.get(philoBaseUrl+element).text
    soup = bs(html_text, 'html.parser')
    contentDiv = soup.select('#mw-content-text ul li a')

    for a in contentDiv:
      name = a.getText()
      if(len(name) > 1):
        modName = name.replace(" ", "_")
        underScoreNameList.append(modName)
        philosopherNameList.append(name) 


  del philosopherNameList[0:5]
  del underScoreNameList[0:5]

  #check for div and h2

  nameCount = 0
  f = open("purgeList.txt" , 'w+')
  for name in underScoreNameList:
    tempUrl = 'https://en.wikipedia.org/wiki/'+name
    print(tempUrl)
    tempList = []
    bioPage = requests.get(tempUrl).text
    soup2 = bs(bioPage, 'html.parser')

    bio = soup2.select('#mw-content-text .mw-parser-output p')
    count = 0
    for p in bio:
      if(count> 0):
        break
      else:
        tempList.append(p.getText())
        count+=1
    try:
      if(len(tempList[0]) <=1):
        f.write(name)
      else:
        newString = tempList[0].replace('\n', '')
        #tuple to add to db
        dataToAdd = [(name, newString)]
        print(dataToAdd)
        c.executemany("INSERT INTO philosophers VALUES (?,?)", dataToAdd)
        nameBioDict[philosopherNameList[nameCount]] = newString
    except:
     print("no bio " + name)
     philosopherNameList.pop(nameCount)
     underScoreNameList.remove(name)

    nameCount+=1
    time.sleep(0.5)
  conn.commit()
  f.close()
  print(nameBioDict)

if __name__ == '__main__':
  main()
