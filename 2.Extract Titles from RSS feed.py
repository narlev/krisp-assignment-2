import feedparser

google_news_url = "https://news.google.com/news/rss"


def get_headlines(rss_url):
    # feedparser for extracting RSS
    feed = feedparser.parse(rss_url)
    titles = [entry.title for entry in feed.entries]

    return titles


print(get_headlines(google_news_url))
