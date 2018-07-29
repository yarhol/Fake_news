import requests
import time
import json
import os
from os import makedirs, chdir
from os.path import join
from bs4 import BeautifulSoup


def fetch_list():
    # set NYT parameters
    NYT_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "NYT")
    makedirs(NYT_folder, exist_ok=True)
    NYT_key = "1fb9687f82a34c079f072106f8d57845"
    NYT_endpoint = "http://api.nytimes.com/svc/archive/v1/"
    # call to the NYT archive to get a whole month's list of articles (June)
    NYT_url = NYT_endpoint + "2018/6" + ".json?api-key=" + NYT_key
    go_get_it = requests.get(NYT_url)
    ok_got_it = go_get_it.json()
    NYT_file = join(NYT_folder, "June2018" + ".json")
    with open(NYT_file, 'w') as f:
        print("Writing to", NYT_file)
        f.write(json.dumps(ok_got_it, indent=2))
    # call to the NYT archive to get a whole month's list of articles (July)
    NYT_url = NYT_endpoint + "2018/7" + ".json?api-key=" + NYT_key
    go_get_it = requests.get(NYT_url)
    ok_got_it = go_get_it.json()
    NYT_file = join(NYT_folder, "July2018" + ".json")
    with open(NYT_file, 'w') as f:
        print("Writing to", NYT_file)
        f.write(json.dumps(ok_got_it, indent=2))
    return


def scrape_individual_articles():
    NYT_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "NYT")
    chdir(NYT_folder)
    saved_articles = [a for a in os.listdir('.') if a.endswith(".txt")]
    existing_articles = [int(a.replace('article', '').replace(".txt", '')) for a in saved_articles]
    last_article = max (existing_articles)
    last_article = max (last_article, 0)
    print (str(str(last_article)) + " NYT articles already saved.")
    with open('June2018.json', 'r') as articles_month1:
        obj_month1 = json.load(articles_month1)
    with open('July2018.json', 'r') as articles_month2:
        obj_month2 = json.load(articles_month2)
    NYT_links = []
    for doc in obj_month1 ['response']['docs']:
        NYT_links.append(doc['web_url'])
    for doc in obj_month2 ['response']['docs']:
        NYT_links.append(doc['web_url'])
    print (str(len(NYT_links)) + " new NYT articles.")
    for x in range(6000, 8428):
        time.sleep(5)
        try:
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
            article_number = x + last_article
            article_file = join(NYT_folder, "article" + str(article_number) + ".html")
            with open(article_file, 'w') as f:
                f.write(get_one_article.text)
            article_file = join(NYT_folder, "article" + str(article_number) + ".txt")
            with open(article_file, 'w') as f:
                for s in clean_title:
                    f.write(str(s) + '\n')
                for s in clean_body:
                    f.write(str(s) + '\n')
        except:
            pass
    return
