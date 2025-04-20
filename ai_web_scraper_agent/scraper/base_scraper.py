import requests
from bs4 import BeautifulSoup

def scrape_hacker_news():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []
    for item in soup.select(".titleline > a"):
        titles.append(item.get_text())

    return titles
def scrape_quotes():
    url = "http://quotes.toscrape.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []
    for quote in soup.select(".quote"):
        text = quote.select_one(".text").get_text()
        author = quote.select_one(".author").get_text()
        quotes.append(f"{text} - {author}")
    return quotes
