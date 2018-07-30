import os
from os import chdir
from os.path import join
import pandas as pd
import Guardian
import NYT
import News_API
import boto3


def bit_of_cleaning (source):
    source_folder = join ("C:\\Users\yaron.hollander", "Documents", "fakenews", str(source).capitalize())
    chdir(source_folder)
    files_to_check = [f for f in os.listdir('.')]
    for f in files_to_check:
        the_size = os.stat(f).st_size
        if (the_size < 1000):
            os.remove(f)
            print ("The size of ", f, "was", the_size, ", so I got rid of the bastard.")
        else:
            print("The size of ", f, "was", the_size, ". I like them biiig.")
    # The bit below is for a problem I had with "the telegraph" only.
    if source=="the-telegraph":
        files_to_check = [f for f in os.listdir('.') if f.endswith(".txt")]
        for f in files_to_check:
            with open(f, 'r') as the_file:
                the_text = the_file.read().rstrip()
                if (the_text.endswith("...")):
                    print("File ", f, "was incomplete, so I will get rid of the bastard.")
                    the_file.close()
                    os.remove(f)
                else:
                    print("File ", f, "is cool.")


def fetch_articles():
    Guardian.guardian_fetch()
    Guardian.guardian_save_articles()
    bit_of_cleaning("guardian")
    NYT.fetch_list()
    NYT.scrape_individual_articles()
    bit_of_cleaning("NYT")
    source_name = "bbc-news"
    # source_name = "al-jazeera-english"
    # source_name = "the-telegraph"
    # source_name = "breitbart-news"
    # source_name = "usa-today"
    # source_name = "metro"
    # source_name = "daily-mail"
    # source_name = "independent"
    # source_name = "cnn"
    # source_name = "reuters"
    News_API.fetch_list(source_name)
    source_links = News_API.list_links(source_name)
    News_API.scrape_individual_articles(source_name, source_links)
    bit_of_cleaning(source_name)


def upload_to_s3(sources):
    client = boto3.client('s3')
    bucket_name = 'fakenewsproject'
    for s in sources:
        source_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews", str(s).capitalize())
        source_nickname = s.replace("-", "").replace("the", "").lower()[:3]
        chdir(source_folder)
        files = [f for f in os.listdir('.') if f.endswith(".txt")]
        for one_file in files:
            with open(one_file, 'r') as f:
                file_body = f.read()
            file_name = source_nickname + one_file.replace("article", "")
            client.put_object (Body = file_body, Bucket=bucket_name, Key=file_name)
            print ("Uploading", file_name)


def stats_of_s3_files(sources):
    count = 0
    size = 0
    s_nicknames = [s.replace("-", "").replace("the", "").lower()[:3] for s in sources]
    count_by_source = pd.DataFrame (columns=['count'], index=s_nicknames)
    for s in s_nicknames:
        count_by_source.loc[s, 'count'] = 0
    my_bucket = boto3.resource('s3').Bucket('fakenewsproject')
    for file in my_bucket.objects.all():
        print ("Looking at ", file.key)
        count += 1
        s = file.key[:3]
        count_by_source.loc[s, 'count'] += 1
        size += file.size
    print ("***********************************************************************")
    print (count_by_source)
    print ("***********************************************************************")
    print ("Total files in the bucket:", count)
    print ("Total size in MB:", size/1000000)
    print ("***********************************************************************")
