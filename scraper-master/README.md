# Scraper

This program is to fill a content dock for given urls

## Dependancies

For pip:
```shell
pip install Flask
pip install beautifulsoup4
pip install python-docx
pip install docx
pip install html_to_json
pip install pycopy-copy
```

For pip3:
"""shell
pip3 install Flask
pip3 install beautifulsoup4
pip3 install python-docx
pip3 install docx
pip3 install html_to_json
pip3 install pycopy-copy
"""

## Setting up the application
In order to use this, you need to change a few lines in a few files.

### Put in your Semrush API key
1. Create a file called key.txt in the main project directory.
2. Paste your Semrush API key in the folder and make sure there are no newlines or spaces.

## Running the application
1. To run the application, first open a terminal or command prompt window in the project directory and type ```flask run```.
2. Next, copy the file path of web/html/index.html and paste it into chrome.

If something goes wrong, check both the website console by hitting f2 and the python console.

## Using the application
### The first page
![Alt text](img/Page1.png?raw=true "Page-1")
When you first open the site, this is what you will see. Here, paste in all of the URLs you want to scrape and click the "Submit" button

Next you'll be taken to a loading page, here your doc is being created and filled. Just wait until the next page loads

### The last page
![Alt text](img/Page2.png?raw=true "Page-2")
Here, paste the path you want to save the doc to including the doc name, for example: ```c:/path/to/doc/docname.docx``` (Remember to use '/' instead of '\'). Then click "Save File" and
you're done! The site will reload and you can close the page and stop the flask server.

## Issues
If you have any issues, please post in the issues tab on this repo. If you do, please remember to post the entire error message and where it came from (chrome console or flask console).
