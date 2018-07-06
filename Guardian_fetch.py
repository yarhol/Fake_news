import requests
import json
import os
from os import makedirs, chdir
from os.path import join
from datetime import date


def guardian_fetch():
    # set guardian parameters
    guardian_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "Guardian")
    makedirs(guardian_folder, exist_ok=True)
    guardian_key = "a810307c-6f4d-4870-963f-ccd0f6e123bc"
    guardian_endpoint = "http://content.guardianapis.com/search"
    guardian_parameters = {
        'from-date': date(2018, 4, 1),
        'to-date': date(2018, 5, 31),
        'order-by': 'oldest',
        'show-fields': 'all',
        'page-size': 200,
        'api-key': guardian_key
    }
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
        guardian_file = join(guardian_folder, "page" + str(page_index) + ".json")
        chdir(guardian_folder)
        with open(guardian_file, 'w') as f:
            print("Writing to", guardian_file)
            f.write(json.dumps(ok_got_it, indent=2))
    return


def guardian_save_articles():
    guardian_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", "Guardian")
    chdir(guardian_folder)
    files = [f for f in os.listdir('.') if f.endswith(".json")]
    article_id = 0
    for one_file in files:
        with open(one_file, 'r') as the_file:
            one_page = json.load(the_file)
            all_content = one_page["response"]["results"]
            for one_article in all_content:
                try:
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
