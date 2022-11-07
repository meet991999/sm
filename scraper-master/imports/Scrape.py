from bs4 import BeautifulSoup
import requests


class scrape:

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer" : "https://www.google.com/"
    }

    def __init__(self, URL):
        self.URL = URL  # The URL we want to scrape

        self.request = requests.get(self.URL, headers=self.headers)  # Make a request to see the source code of the url

        # Maybe add some error checking

        self.soup = BeautifulSoup(self.request.text, "html.parser")  # Make bs4 object

        # Store h1 tag, title, and metadata.
        self.h1 = self.getH1()
        self.title = self.getTitle()
        self.metaDescription = self.getMetaDescription()
        self.content = self.getContent()

    # Get first H1 of page
    def getH1(self):
        return self.soup.find("h1").text if self.soup.find("h1").text != None else "N/A"

    # Get title of the page
    def getTitle(self):
        return self.soup.title.text if self.soup.title.text != None else "N/A"

    # Get the meta description of the page
    def getMetaDescription(self):
        return self.soup.find('meta', attrs={'name': 'description'}).attrs["content"] if self.soup.find('meta', attrs={'name': 'description'}) != None else "N/A"

    # Get all the h2, h3 and p tags
    def getContent(self):
        tags = ["h2", "h3", "p"]
        return self.soup.find_all(tags)

        
if __name__ == "__main__":
    scraper = scrape(r"https://github.com/")
    scraper.getContent()
