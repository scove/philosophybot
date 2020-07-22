import requests
from bs4 import BeautifulSoup as bs
import sqlite3 

# check for <a class='next page'>
# for people with multiple pages grab the last number
# for people with no page grab the "Search does not contain results"
# eliminate quotes not by author name


def main():
  quoteNotFoundText = 'Sorry, no results matched your search.'
  baseUrl = 'https://www.goodreads.com/quotes/search?page=1&q=gustav+shpet'
  html_text = requests.get(baseUrl).text
  soup = bs(html_text, 'html.parser')
  contentDiv = soup.select('.leftContainer .mediumText') 
  
  #empty check
  if(quoteNotFoundText not in str(contentDiv)):
    #continue because there is a quote page

    #check if there are multiple pages

if __name__ == '__main__':
  main()






