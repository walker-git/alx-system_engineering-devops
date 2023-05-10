#!/usr/bin/python3
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively retrieves hot posts in a subreddit, counts occurrences of
    keywords in the titles of those posts, and prints a sorted count of the
    keywords.

    subreddit (str): The name of the subreddit to search.
    word_list (List[str]): A list of keywords to search for.
    after (str): The value to pass as the "after" parameter in the Reddit API
        request, for pagination.
    counts (Dict[str, int]): A dictionary mapping keywords to their counts so far.
    """
    # If this is the first call to the function, initialize the counts dict
    if counts is None:
        counts = {}

    # If we've already counted all the words, return the final counts
    if not word_list:
        return counts

    # Get the first word in the list and remove it from the list
    word = word_list[0]
    word_list = word_list[1:]

    # If the word is empty or contains invalid characters, skip it
    if not word or not word.isalnum():
        return count_words(subreddit, word_list, after=after, counts=counts)

    # Make the API request to Reddit to get the hot posts in the subreddit
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100}
    if after:
        params['after'] = after
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    # If the subreddit is invalid or the request was unsuccessful, exit
    if response.status_code != 200:
        return

    # Parse the JSON response
    data = response.json()

    # If there are no posts left to process, return the final counts
    if not data['data']['children']:
        return counts

    # Loop through the posts and count occurrences of the word in the titles
    for post in data['data']['children']:
        title = post['data']['title'].lower()
        if word.lower() in title.split():
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

    # Recursively call the function with the remaining words and the "after" parameter
    return count_words(subreddit, word_list, after=data['data']['after'], counts=counts)


# Example usage: count_words('programming', ['react', 'python', 'java', 'javascript', 'scala', 'no_results_for_this_one'])

