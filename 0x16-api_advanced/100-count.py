#!/usr/bin/python3
import requests
from collections import Counter

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = Counter()
    if after == '':
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")
        return
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": "100", "after": after}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for post in data['data']['children']:
            title = post['data']['title'].lower()
            for word in word_list:
                if f" {word.lower()} " in f" {title} ":
                    counts[word.lower()] += 1
        after = data['data']['after']
        count_words(subreddit, word_list, after, counts)
    else:
        print(f"Error: {response.status_code}")


