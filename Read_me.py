# 1) compare most common words across sources, e.g. check what words are typical of the source!!!
# 2) then take all article stats and turn them into source stats!!!
# 3) add tf-idf!!!
# 4) add word length distribution as one of the stats!
# 5) add all kinds of visualisations!


# Guardian -
# Got full articles from April and May 2018, organised in multiple pages.
# Note that there's a different restructuring function.
# Should download data from June/July 2018 to align with other sources.
# Later also need to restructure when I start NLP.
# Guardian_fetch.guardian_fetch()
# Guardian_fetch.guardian_save_articles()
# bit_of_cleaning("guardian")
#
# NYT -
# Got full list of nearly 10000 articles from April and May, with a separate function for fetching the full articles.
# May need to continue to June/July to align with other sources.
# NYT_fetch.fetch_list()
# NYT_fetch.scrape_individual_articles()
# bit_of_cleaning("NYT")
# Later also need to restructure when I start NLP.
#
# News API -
# Got data from: usa-today, metro, the-telegraph, daily-mail, independent, cnn, bbc-news, reuters, al-jazeera-english,
# breitbart-news.
# I got up to 100 articles per day for 1 month (100/day is the limit), ending around June 14-20 depending on the source.
# Then I scraped full articles, basedon the different DOM of each source.
# Should get another month later!
# source_name = "metro"
# News_API_fetch.fetch_list(source_name)
# source_links = News_API_fetch.list_links(source_name)
# News_API_fetch.scrape_individual_articles(source_name, source_links)
# bit_of_cleaning(source_name)
#
# FT -
# There's a developer API which I didn't pay much attention to coz I have enough source. Possibly get back to it.
