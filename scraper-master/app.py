import os
from datetime import date
from copy import deepcopy
from urllib.parse import urldefrag
from docx import Document
from docx.shared import Pt
import imports.Scrape as Scrape
import imports.Doc as Doc
from flask import Flask, jsonify, render_template, request, send_file, send_from_directory
from flask_cors import CORS
from Semrush import Semrush

app = Flask(__name__)
CORS(app)

def getURLs(urls):
    """
    Correctly format the URLS inputted from the website

    Returns:
    ========
        r : list
            A list of all the URLS
    """

    r = []

    t = urls.split(", ")
    for i in t:
        if i == '' or i == ' ': continue
        r.append(i)
    print(r)
    return r

@app.route("/download")
def download():
    path = 'D:/Meet/scraper-master/web/html/files/2022-11-04/a.docx'
    return send_file(path, as_attachment=True)



def getContent(urls):
    """
    Get the content for all rows

    Returns:
    ========
        content : list
            correnctly formatted list of the first few rows in the content doc
        onPage : list
            correctly formatted list of the onpage content from the website.
    """

    global s

    with open("key.txt", "r") as f: key = f.read().strip()

    content = []
    onPage = []
    semrush = Semrush.semrush(key)

    for url in urls:
        s = Scrape.scrape(url)
        semrushContent = semrush.getContent(url)

        content.append([s.h1, s.URL, s.title, s.metaDescription, semrushContent[1], semrushContent[0]])

        onPage.append(s.getContent())

    return content, onPage


@app.route("/url", methods=["POST"])
def createDoc():
    """
    Create a doc with URLS given by user
    """

    global doc

    inputJson = request.get_json(force=True)  # Get the JSON from the user
    #print(dict(inputJson))
    URLS = getURLs(inputJson["text"])  # Get the URLs from the JSON
    content, onPage = getContent(URLS)  # Get the content
    print(content)

    doc = Doc.document(len(URLS))  # Create our doc

    # Put content in the doc
    doc.insertContent(content)
    doc.insertFormatedContent(onPage)
    # b = send_from_directory(app.config['D:/Meet/scraper-master/web/html/files/2022-11-04'], 'a.docx', as_attachment=True)


    return jsonify({"text":content})

@app.route("/path", methods=["POST"])
def saveFile():
    """
    Save the doc
    """


    directory_date_folder = str(date.today())
    print(directory_date_folder)
    parent_dir_for_date = "D:/Meet/scraper-master/web/html/files/"
    path_new_date = os.path.join(parent_dir_for_date, directory_date_folder)


    for i in os.listdir(parent_dir_for_date):
        if i==directory_date_folder:

            inputJson = request.get_json(force=True)  # Get JSON from user
            PATH = inputJson["text"]  # Get the path
            doc.save("D:/Meet/scraper-master/web/html/files/"+directory_date_folder+"/"+str(PATH))
            return inputJson


        else:
            os.mkdir(path_new_date)
            inputJson = request.get_json(force=True)  # Get JSON from user
            PATH = inputJson["text"]  # Get the path

            doc.save("D:/Meet/scraper-master/web/html/files/"+directory_date_folder+"/"+str(PATH))

            return inputJson






    #inputJson = request.get_json(force=True)  # Get JSON from user
    #PATH = inputJson["text"]  # Get the path

    #doc.save("D:/scraper-master/scraper-master/web/html/files/"+directory_date_folder+str(PATH))
    #return inputJson

