import requests
from bs4 import BeautifulSoup as bs
import sqlite3 

# check for <a class='next page'>
# for people with multiple pages grab the last number
# for people with no page grab the "Search does not contain results"
# eliminate quotes not by author name


def main():
  quoteNotFoundText = 'Sorry, no results matched your search.'
  nextPageText = 'next'
  authorName = 'Shankara'
  baseUrl = 'https://www.goodreads.com/quotes/search?page=1&q=adi+shankara'
  html_text = requests.get(baseUrl).text
  soup = bs(html_text, 'html.parser')
  contentDiv = soup.select('.leftContainer .mediumText') 
  
  #empty check
  if(quoteNotFoundText not in str(contentDiv)):
    #continue because there is a quote page

    #check if there are multiple pages
    soup2 = bs(html_text, 'html.parser')
    nextPage = soup.select('.leftContainer div div .next_page')

    if(nextPageText not in str(nextPage)):
      #GET QUOTES
      soup4 = bs(html_text, 'html.parser')
      quoteList = soup.select('.leftContainer .quote .quoteText')
      quoteListLength = len(quoteList)
      for i in range(0, quoteListLength):
        #author check
        quote = quoteList[i].getText().split('\n    ―\n  \n')
        if(authorName in quote[1]):
          quoteClean1 = quote[0].replace('\n      ', '')
          print(quoteClean1)


    else:
      #grab the last number so we can loop pages
      soup3 = bs(html_text, 'html.parser')
      pageList = soup.select('.leftContainer div div a')
      lastPageNum = int(pageList[-2:][0].getText())

      for i in range(1,lastPageNum+1):
        pass
        #GET QUOTES

if __name__ == '__main__':
  main()






