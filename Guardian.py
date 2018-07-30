import requests
import json
import os
from os import makedirs, chdir
from os.path import join
from datetime import date, datetime


def guardian_fetch():
    # set guardian parameters
    guardian_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "Guardian")
    makedirs(guardian_folder, exist_ok=True)
    chdir(guardian_folder)
    guardian_key = "a810307c-6f4d-4870-963f-ccd0f6e123bc"
    guardian_endpoint = "http://content.guardianapis.com/search"
    guardian_parameters = {
        'from-date': date(2018, 6, 1),
        'to-date': date(2018, 7, 23),
        'order-by': 'oldest',
        'show-fields': 'all',
        'page-size': 200,
        'api-key': guardian_key
    }
    # check files created previously
    files = [f for f in os.listdir('.') if f.endswith(".json")]
    existing_pages = [int(f.replace('page', '').replace(".json", '')) for f in files]
    last_page = max (existing_pages)
    last_page = max (last_page, 1)
    # initial call to the guardian, to get the number of pages
    go_get_it = requests.get(guardian_endpoint, guardian_parameters)
    ok_got_it = go_get_it.json()
    total_pages = ok_got_it["response"]["pages"]
    print("Total pages:", total_pages)
    # now get each page with a separate call
    for page_index in range(1, total_pages + 1):
        guardian_parameters['page'] = page_index
        go_get_it = requests.get(guardian_endpoint, guardian_parameters)
        ok_got_it = go_get_it.json()
        guardian_file = join(guardian_folder, "page" + str(last_page + page_index) + ".json")
        with open(guardian_file, 'w') as f:
            print("Writing to", guardian_file)
            f.write(json.dumps(ok_got_it, indent=2))
    return


def guardian_save_articles():
    guardian_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "Guardian")
    chdir(guardian_folder)
    files = [f for f in os.listdir('.') if f.endswith(".json")]
    saved_articles = [a for a in os.listdir('.') if a.endswith(".txt")]
    existing_articles = [int(a.replace('article', '').replace(".txt", '')) for a in saved_articles]
    last_page = max (existing_articles)
    article_id = max (last_page, 0)
    from_date = date(2018, 6, 1)
    to_date = date(2018, 7, 23)
    for one_file in files:
        with open(one_file, 'r') as the_file:
            one_page = json.load(the_file)
            print ("Looking at ", str(one_file))
            all_content = one_page["response"]["results"]
            for one_article in all_content:
                try:
                    articleDate = datetime.strptime (one_article["webPublicationDate"], "%Y-%m-%dT%H:%M:%SZ").date()
                    within_range = from_date <= articleDate <= to_date
                    if within_range:
                        article_id += 1
                        headline = one_article["fields"]["headline"]
                        trailText = one_article["fields"]["trailText"]
                        articleBody = one_article["fields"]["bodyText"]
                        everything = headline + "\n" + trailText + "\n" + articleBody
                        article_file = join(guardian_folder, "article" + str(article_id) + ".txt")
                        with open(article_file, 'w') as a:
                            a.write(everything)
                except:
                    pass
    return
