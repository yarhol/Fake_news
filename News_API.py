import time
import requests
import json
import os
from os import makedirs, chdir
from os.path import join
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup


def fetch_list(source):
    source_folder = join ("C:\\Users\yaron.hollander", "Documents", "fakenews", str(source).capitalize())
    makedirs(source_folder, exist_ok=True)
    chdir(source_folder)
    files = [f for f in os.listdir('.') if f.endswith(".json")]
    existing_pages = [int(f.replace(str(source).capitalize(), '').replace('page',
                                                                          '').replace('-0', '').replace('-','').replace(".json",'')) for f in files]
    last_page = max (existing_pages)
    last_page = max (last_page, 1)
    News_API_key = "2002eb6e56094c7d81ffff25d23d8ee8"
    News_API_endpoint = "https://newsapi.org/v2/everything?"
    from_date = date(2018, 6, 27)
    to_date = date(2018, 7, 25)
    for n in range(int ((to_date - from_date).days)):
        fetch_date = from_date + timedelta(n)
        source_url = News_API_endpoint + "from=" + str(fetch_date) + "&to=" + str(fetch_date) + "&sources="
        source_url += str(source) + "&pageSize=100&page=1&language=en" + "&apiKey=" + News_API_key
        go_get_it = requests.get(source_url)
        ok_got_it = go_get_it.json()
        source_file = join(source_folder, str(source).capitalize() + "-" + str(last_page + n + 1) + ".json")
        with open(source_file, 'w') as f:
            print("Writing to", source_file)
            f.write(json.dumps(ok_got_it, indent=2))
    return


def list_links(source):
    source_links = []
    source_folder = join ("C:\\Users\yaron.hollander", "Documents", "fakenews", str(source).capitalize())
    chdir(source_folder)
    source_files = [f for f in os.listdir('.') if (f.endswith(".json") and int(datetime.fromtimestamp(os.path.getmtime(f)).month)==7)]
    for one_file in source_files:
        with open(one_file, 'r') as the_file:
            today = json.load(the_file)
        for doc in today['articles']:
            source_links.append(doc['url'])
    for l in source_links:
        print (l)
    print (len(source_links), "in total.")
    return source_links


def get_title(source, one_article):
    the_title = {
        "usa-today": one_article.find_all("h1", {"class" : ["title", "article__headline"]}),
        "metro": one_article.find_all("h1", {"class": "post-title clear"}),
        "the-telegraph": one_article.find_all("h1", {"class": "headline__heading"}),
        "bbc-news": one_article.find_all("h1", {"class": "story-body__h1"}),
        "daily-mail": one_article.find_all("h1"),
        "cnn": one_article.find_all("h1", {"class": ["pg-headline", "article-title speakable"]}),
        "independent": one_article.find_all("h1", {"class": "headline"}),
        "reuters": one_article.find_all("h1", {"class": ["headline_2zdFM", "ArticleHeader_headline"]}),
        "al-jazeera-english": one_article.find_all("h1", {"class": ["post-title", "heading-story"]}),
        "breitbart-news": one_article.find_all("h1"),
        "bloomberg": one_article.find_all("h1", {"class": "lede-text-v2__hed"}),
        "mirror": one_article.select("h1[itemprop='headline name']")
    }
    return the_title.get(source, "")


def get_inside(source, one_article):
    the_inside = {
        "usa-today": one_article.select("div.article-wrapper p, div.articleBody p"),
        "metro": one_article.select("div.article-body > p"),
        "the-telegraph": one_article.select("div.article-body-text p"),
        "bbc-news": one_article.select("div.story-body__inner p"),
        "daily-mail": one_article.select("div[itemprop='articleBody'] p"),
        "cnn": one_article.select("div[class*='element-raw'], p[class*='zn-body__paragraph'], div#storytext h2, "
                                  "div[class*='zn-body__paragraph'], div#storytext p"),
        "independent": one_article.select("div.body-content p"),
        "reuters": one_article.select("div.body_1gnLA p, div.StandardArticleBody_body p"),
        "al-jazeera-english": one_article.select("h2.standfirst, div.main-article-body p, div.article-body p"),
        "breitbart-news": one_article.select("div.entry-content h2, div.entry-content p"),
        "bloomberg": one_article.select("div[class*='body-copy-v2'] p"),
        "mirror": one_article.select("div.article-body p")
    }
    return the_inside.get(source, "")


def scrape_individual_articles(source, source_links):
    source_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", str(source).capitalize())
    chdir(source_folder)
    files = [f for f in os.listdir('.') if f.endswith(".txt")]
    existing_articles = [int(f.replace('article', '').replace(".txt", '')) for f in files]
    last_article = max (existing_articles)
    articles_already_saved = max (last_article, 1)
    already_saved_in_this_round = len([f for f in os.listdir('.') if (f.endswith(".html") and
                                                                      int(datetime.fromtimestamp(os.path.getmtime(f)).month)==7)])
    article_number = articles_already_saved
    article_number_in_this_round = 0
    sleep_time = 5
    for link in source_links:
        article_number_in_this_round += 1
        print("Checking link number", article_number_in_this_round, " from ", link)
        if ((article_number_in_this_round > already_saved_in_this_round) & (not link.endswith('mp4'))):
            article_number += 1
            print("Saving as article number", article_number)
            time.sleep(sleep_time)
            get_one_article = requests.get(link)
            one_article = BeautifulSoup(get_one_article.text, 'html.parser')
            title = get_title(source, one_article)
            clean_title = []

            for t in title:
                t.attrs = None
                temp = str(t).replace("\n\n","\n").replace("\n"," ").replace("  "," ").replace("\n ","\n")
                tag_from = temp.find("<")
                tag_to = temp.find(">") + 1
                while (tag_from >= 0 and tag_to >= 0):
                    temp = temp[:tag_from] + temp[tag_to:]
                    tag_from = temp.find("<")
                    tag_to = temp.find(">") + 1
                clean_title.append(temp)
            inside = get_inside(source, one_article)
            clean_body = []
            for i in inside:
                i.attrs = None
                temp = str(i).replace("\n\n","\n").replace("  "," ").replace("\n ","\n")
                tag_from = temp.find("<")
                tag_to = temp.find(">") + 1
                while (tag_from >= 0 and tag_to >= 0):
                    temp = temp[:tag_from] + temp[tag_to:]
                    tag_from = temp.find("<")
                    tag_to = temp.find(">") + 1
                clean_body.append(temp)

            article_file = join(source_folder, "article" + str(article_number) + ".html")
            with open(article_file, 'w') as f:
                try:
                    f.write(get_one_article.text)
                except:
                    f.write(str(get_one_article.text.encode("utf-8")))

            article_file = join (source_folder, "article" + str(article_number) + ".txt")
            with open(article_file, 'w') as f:
                for s in clean_title:
                    try:
                        f.write(str(s) + '\n')
                    except:
                        f.write(str(s.encode("utf-8")) + '\n')
                for s in clean_body:
                    try:
                        f.write(str(s) + '\n')
                    except:
                        f.write(str(s.encode("utf-8")) + '\n')

    return
