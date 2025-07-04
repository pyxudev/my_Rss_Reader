import re
import feedparser

def removeHttpTag(str):
    return re.sub(re.compile('<.*?>'), '', str)


def main():
    keywords = ["your_keywords"]
    qiitaRssUrl = 'https://qiita.com/popular-items/feed.atom'
    qiitaData = feedparser.parse(qiitaRssUrl)
    for entry in qiitaData.entries:
        qiitaRss = f"Title:{entry.title}\nSummary:{removeHttpTag(entry.summary).replace(f'\n', '')[:110]}...\n{entry.links[0].href.replace(f'?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items', '')}"
        if any(keyword in qiitaRss for keyword in keywords):
            break

    cnpsRssUrl = 'https://connpass.com/explore/ja.atom'
    cnpsData = feedparser.parse(cnpsRssUrl)
    for entry in cnpsData.entries:
        cnpsRss = f"Title:{entry.title}\nSummary:{removeHttpTag(entry.summary).replace(f'\n', '')[:110]}...\n{entry.links[0].href.replace(f'?utm_campaign=recent_events&utm_source=feed&utm_medium=atom', '')}"
        if any(keyword in cnpsRss for keyword in keywords):
            break

    print(qiitaRss)
    print(cnpsRss)

if __name__ == "__main__":
    main()
