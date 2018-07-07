# import Guardian_fetch
# import NYT_fetch
# import News_API_fetch
# from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import os
from os import makedirs, chdir
from os.path import join
from textblob import TextBlob, Word
import seaborn


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
    # files_to_check = [f for f in os.listdir('.') if f.endswith(".txt")]
    # for f in files_to_check:
    #     with open(f, 'r') as the_file:
    #         the_text = the_file.read().rstrip()
    #         if (the_text.endswith("...")):
    #             print("File ", f, "was incomplete, so I will get rid of the bastard.")
    #             the_file.close()
    #             os.remove(f)
    #         else:
    #             print("File ", f, "is cool.")


#sources = ["Jetro", "Retro"]
sources = ["Bbc-news", "Reuters", "Al-jazeera-english", "The-telegraph", "Breitbart-news", "NYT", "Guardian", "Usa-today", "Metro", "Daily-mail",
           "Independent", "Cnn"]

source_words = []
#article_stats = []
#article_words = [] # I've created this list but not used it yet! **********
#source_words_wide = []
outputs_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews")
#full_output = ""
# levels of analysis: word > sentence > article > source


def collate_words():
    words_output_file = join(outputs_folder, "words_output.csv")
    articles_completed_file = join(outputs_folder, "completed.csv")
    stop_words = set(stopwords.words('english'))
    percentage_completed_per_source = 0
    completed_articles_input = open(articles_completed_file, 'r')
    articles_to_skip = pd.read_csv(completed_articles_input, header=None, engine='python')
    completed_articles_input.close()
    articles_to_skip.columns = ['source', 'file']
    for source_name in sources:
        source_folder = join ("C:\\Users\yaron.hollander", "Documents", "fakenews", str(source_name).capitalize())
        chdir(source_folder)
        article_files = [f for f in os.listdir('.') if f.endswith(".txt")]
        articles_per_source = len(article_files)
        articles_completed_per_source = 0
        articles_to_skip_per_source = [a for a in articles_to_skip if a['source']==source_name]
        for f in article_files:
            if f not in articles_to_skip_per_source['file']:
                article_text = open (f, 'r').read()
                words_filthy = TextBlob(article_text).words
                words_dirty = [w.lower().replace("'", "").replace(".", "").replace(",", "") for w in words_filthy]
                words_messy = [w for w in words_dirty if not w in stop_words]
                words_ok = [Word(w).lemmatize() for w in words_messy if len(w)>1]
                words_clean = [w for w in words_ok if not w in [source_name, "bbc", "also", "got", "get", "nt", "ve", "year", "say", "one", "two",
                                                                "first", "last", "would", "new", "day", "like", "back", "could", "make", "go"]]
                #store_text = regex.sub ('[\t\n\r\f\v]', ' ', str(article_text))
                #article_stats.append({'source': source_name, 'file': f, 'tot_len': len(words_filthy), 'text': store_text})
                for w in words_clean:
                    #word_exists_by_source = len ([x for x in article_words if x['source'] == source_name and x['file'] == f
                    #                    and x['word'] == w])
                    word_exists_anywhere = len ([x for x in source_words if x['source'] == source_name and x['word'] == w])
                    #if word_exists_by_source == 0:
                    #    article_words.append({'source': source_name, 'file': f, 'word': w, 'count': 1})
                    #else:
                    #    [x for x in article_words if x['source']==source_name and x['file'] == f
                    #     and x['word'] == w][0]['count'] += 1
                    if word_exists_anywhere == 0:
                        source_words.append({'source': source_name, 'word': w, 'freq': 1})
                    else:
                        [x for x in source_words if x['source']==source_name and x['word'] == w][0]['freq'] += 1
                words_output = open (words_output_file, 'w+') # re-writing the whole file after each article to make it usable even when it doesn't finish
                words_output.write("source,word,freq\n")
                for x in source_words:
                    if x['freq'] > 4:
                        words_output.write(str(x['source']) + "," + str(x['word']) + "," + str(x['freq']) + "\n")
                words_output.close()
            completed_articles_output = open(articles_completed_file, 'a+')
            completed_articles_output.write(str(source_name) + "," + str(f) + "\n")
            #sentences = article_text.sentences
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['sentences'] = len(sentences)
            #sentence_length = []
            #sentence_polarity = [] # polarity range is from -1 to 1
            #sentence_subjectivity = [] # subjectivity range is from 0 to 1
            #for s in sentences:
            #    sentence_length.append(len(s.words))
            #    sentence_polarity.append(s.polarity)
            #    sentence_subjectivity.append(s.subjectivity)
            #length20 = np.percentile (sentence_length, 20)
            #length80 = np.percentile (sentence_length, 80)
            #polarity20 = np.percentile (sentence_polarity, 20)
            #polarity80 = np.percentile (sentence_polarity, 80)
            #subjectivity20 = np.percentile (sentence_subjectivity, 20)
            #subjectivity80 = np.percentile (sentence_subjectivity, 80)
            # later maybe build a whole probability distribution function with more than just these two bins, so that later we can calcualte the
            # chance that a new article comes from that distribution?
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['length20'] = length20
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['length80'] = length80
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['polarity20'] = polarity20
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['polarity80'] = polarity80
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['subjectivity20'] = subjectivity20
            #[x for x in article_stats if x['source'] == source_name and x['file'] == f][0]['subjectivity80'] = subjectivity80
            articles_completed_per_source += 1
            percentage_displayed = percentage_completed_per_source
            percentage_completed_per_source = int(100*articles_completed_per_source/articles_per_source)
            if percentage_completed_per_source != percentage_displayed:
                print (source_name + ": " + str(percentage_completed_per_source) + "% completed")
        # total_words_per_source = sum ([w['freq'] for w in source_words if w['source'] == source_name])
        # for s in source_words:
        #     if s['source'] == source_name:
        #         s['freq'] = s['freq'] / total_words_per_source

    #source_words.sort(key=lambda x: x['count'], reverse=True)
    #source_words.sort(key=lambda x: x['word'])
    #pivot source_words into a wide format???

    # for a in article_stats:
    #     full_output += str(a['source']) + " " + str(a['file']) + ": " + str(a['tot_len']) + " words, " + str(a['sentences']) + " sentences, "
    #     full_output += "words/sen 20 perc " + str("{:.1f}".format(a['length20'])) + " 80 perc " + str("{:.1f}".format(a['length80'])) + ", "
    #     full_output += "polarity 20 perc " + str("{:.3f}".format(a['polarity20'])) + " 80 perc " + str("{:.3f}".format(a['polarity80'])) + ", "
    #     full_output += "subjectivity 20 perc " + str("{:.3f}".format(a['subjectivity20']))
    #     full_output += " 80 perc " + str("{:.3f}".format(a['subjectivity80'])) + "\n"


def heatmap():
    input_folder = join("C:\\Users\yaron.hollander", "Documents", "fakenews")
    source_words_file = join (outputs_folder, "outputs.csv")
    source_words_long = pd.read_csv (source_words_file, header=0, engine='python')
    source_words_wide = pd.pivot_table(source_words_long, index='word', columns='source', values='freq', fill_value=0)
    source_words_wide ['sum'] = source_words_wide.sum (axis=1, numeric_only=True)
    source_words_show = source_words_wide.sort_values (by='sum', ascending=False).head(25)
    #print (source_words_show)
    source_words_show = source_words_show.drop('sum', 1)
    # normalise columns!
    word_heatmap = seaborn.heatmap (source_words_show, annot=True)
    figure_file = join(outputs_folder, "heatmap.png")
    word_heatmap.figure.savefig (figure_file)


collate_words()
#heatmap()
