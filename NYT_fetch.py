import requests
import time
import json
from os import makedirs, chdir
from os.path import join
from bs4 import BeautifulSoup


def fetch_list():
    # set NYT parameters
    NYT_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "NYT")
    makedirs(NYT_folder, exist_ok=True)
    NYT_key = "1fb9687f82a34c079f072106f8d57845"
    NYT_endpoint = "http://api.nytimes.com/svc/archive/v1/"
    # call to the NYT archive to get a whole month's list of articles (April)
    NYT_url = NYT_endpoint + "2018/4" + ".json?api-key=" + NYT_key
    go_get_it = requests.get(NYT_url)
    ok_got_it = go_get_it.json()
    NYT_file = join(NYT_folder, "April2018" + ".json")
    with open(NYT_file, 'w') as f:
        print("Writing to", NYT_file)
        f.write(json.dumps(ok_got_it, indent=2))
    # call to the NYT archive to get a whole month's list of articles (May)
    NYT_url = NYT_endpoint + "2018/5" + ".json?api-key=" + NYT_key
    go_get_it = requests.get(NYT_url)
    ok_got_it = go_get_it.json()
    NYT_file = join(NYT_folder, "May2018" + ".json")
    with open(NYT_file, 'w') as f:
        print("Writing to", NYT_file)
        f.write(json.dumps(ok_got_it, indent=2))
    return


def scrape_individual_articles():
    NYT_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "NYT")
    chdir(NYT_folder)
    with open('April2018.json', 'r') as April_articles:
        obj_April = json.load(April_articles)
    with open('May2018.json', 'r') as May_articles:
        obj_May = json.load(May_articles)
    NYT_links = []
    for doc in obj_April['response']['docs']:
        NYT_links.append(doc['web_url'])
    for doc in obj_May['response']['docs']:
        NYT_links.append(doc['web_url'])
    for x in range(9700, 9803):
        time.sleep(2)
        get_one_article = requests.get(NYT_links[x])
        one_article = BeautifulSoup(get_one_article.text, 'html.parser')
        # extract the NYT article title and remove non-text elements from it
        title = one_article.select("h1[itemprop='headline']")
        clean_title = []
        for t in title:
            t.attrs = None
            temp = str(t)
            tag_from = temp.find("<")
            tag_to = temp.find(">") + 1
            while (tag_from >= 0 and tag_to >= 0):
                temp = temp[:tag_from] + temp[tag_to:]
                tag_from = temp.find("<")
                tag_to = temp.find(">") + 1
            clean_title.append(temp)
        # extract the NYT article body and remove non-text elements from it
        inside = one_article.find_all("p", {"class": "css-1i0edl6 e2kc3sl0"})
        clean_body = []
        for i in inside:
            i.attrs = None
            temp = str(i)
            tag_from = temp.find("<")
            tag_to = temp.find(">") + 1
            while (tag_from >= 0 and tag_to >= 0):
                temp = temp[:tag_from] + temp[tag_to:]
                tag_from = temp.find("<")
                tag_to = temp.find(">") + 1
            clean_body.append(temp)
        try:
            article_file = join(NYT_folder, "article" + str(x) + ".html")
            with open(article_file, 'w') as f:
                f.write(get_one_article.text)
            article_file = join(NYT_folder, "article" + str(x) + ".txt")
            with open(article_file, 'w') as f:
                for s in clean_title:
                    f.write(str(s) + '\n')
                for s in clean_body:
                    f.write(str(s) + '\n')
        except:
            pass
    return
