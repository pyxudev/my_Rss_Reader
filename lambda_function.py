import re
import feedparser
import requests
import json

keywords = [<your_keywords>]
qiitaRssUrl = 'https://qiita.com/popular-items/feed.atom'
cnpsRssUrl = 'https://connpass.com/explore/ja.atom'

def sendMessageToJuniorChennel(content):
    url = "https://discord.com/api/channels/<your_channel>/messages"

    payload = {
        "content": content
    }
    headers = {
        "Authorization": "Bot <your_bot_token>",
        "Content-Type": "application/json"
    }

    requests.post(url, json=payload, headers=headers)

def removeHttpTag(str):
    return re.sub(re.compile('<.*?>'), '', str)

def listUpFeed(entry, atomLink):
    rssContent = f"**{entry.title}**\n> {removeHttpTag(entry.summary).replace(f'\n', '')[:110]}...\n{entry.links[0].href.replace(atomLink, '')}"
    if any(keyword in rssContent for keyword in keywords):
        sendMessageToJuniorChennel(rssContent)

def lambda_handler(event, context):
    itemCount = 0

    rssdict = {
        "qiitaData": [qiitaRssUrl, '?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items', '---Qiita 記事---'],
        "cnpsData": [cnpsRssUrl, '?utm_campaign=recent_events&utm_source=feed&utm_medium=atom', '---Connpass イベント---']
    }

    try:
        for key in rssdict:
            data = rssdict[key]
            rssdata = feedparser.parse(data[0])
            atomLink = data[1]
            itemType = data[2]
            itemCount = 0

            for entry in rssdata.entries:
                if itemCount == 0:
                    sendMessageToJuniorChennel(itemType)
                itemCount =+ 1
                listUpFeed(entry, atomLink)
        
        return {
            'statusCode': 200,
            'body': json.dumps("Succeed")
        }
    except Exception as e:
        return {
            'statusCode': 502,
            'body': json.dumps(str(e))
        }
