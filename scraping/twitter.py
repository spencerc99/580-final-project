import requests
import time
import base64
from dotenv import load_dotenv
import os
import tweepy
import re
from pathlib import Path  # python3 only
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

program_start_time = time.time()

client_key = os.getenv("TWITTER_API_KEY")
client_secret = os.getenv("TWITTER_API_SECRET_KEY")

# key_secret = "{}:{}".format(client_key, client_secret).encode('ascii')
# b64_encoded_key = base64.b64encode(key_secret)
# b64_encoded_key = b64_encoded_key.decode('ascii')


auth = tweepy.OAuthHandler(client_key, client_secret)

api = tweepy.API(auth)

# base_url = "https://api.twitter.com"
# auth_url = f'{base_url}/oauth2/token'

# auth_headers = {
#     'Authorization': f'Basic {b64_encoded_key}',
#     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
# }

# auth_data = {
#     'grant_type': 'client_credentials'
# }

# auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# auth_resp.raise_for_status()
# access_token = auth_resp.json()['access_token']

# req_headers = {
#     'Authorization': f'Bearer {access_token}'
# }

# print("ACCESS TOKEN:", access_token)


# search_params = {
#     'q': 'General Election',
#     'result_type': 'recent',
#     'count': 2
# }

# search_url = '{}1.1/search/tweets.json'.format(base_url)

# search_resp = requests.get(
#     search_url, headers=req_headers, params=search_params)

# print(search_resp.json())
sleep_backoff = 2


def get_tweets_by_user(user_id, count=3200):
    """
    GET statuses/user_timeline
    see reference: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html,

    user_id : id of the user to retrieve tweets from
    count   : int indicating number of tweets to retreive, must be <= 3200
    """
    resp = api.user_timeline(user_id, count=count)
    return resp


def get_tweet_by_id(tweet_id):
    resp = api.get_status(tweet_id)
    return resp


def write_data(file, user_id, data):
    file.write(f'{user_id}: {data}\n')


def gather_data(user_ids, start_line=0):
    """
    Gather data from intended handles
    """
    with open("../data/ira_tweet_data", "w") as f:
        for i, user_id in enumerate(user_ids[start_line:]):
            user_id = user_id.strip()
            print(f'Gathering data for user {i}: {user_id}')
            try:
                data = get_tweets_by_user(user_id)
                # TODO: store somewhere (file, actual DB?)
                write_data(f, user_id, data)
                print(data)
            except tweepy.error.TweepError as e:
                # error on HTTP request, log error
                print(e)
                with open(f'{program_start_time}_errored_users', 'a') as error_file:
                    error_file.write(f'{user_id}\n')
                time.sleep(2)


def gather_data_by_tweet_ids(tweet_ids, start_line=0):
    global sleep_backoff
    with open("../data/normal_user_data", "w") as f:
        f.write("tweet_id,content,language\n")
        for i, tweet_id in enumerate(tweet_ids[start_line:]):
            tweet_id = tweet_id.strip()
            print(f"gathering data for tweet {i}: {tweet_id}")
            try:
                data = get_tweet_by_id(tweet_id)
                processed_content = re.sub(
                    ',', ' ', re.sub('\n', ' ', data.text))
                f.write(f"{tweet_id},{processed_content},{data.lang}\n")
            except tweepy.error.TweepError as e:
                print(e)
                if type(e) is tweepy.error.RateLimitError:
                    time.sleep(sleep_backoff)
                    sleep_backoff *= 2
                with open(f'{program_start_time}_errored_users', 'a') as error_file:
                    error_file.write(f'{tweet_id}\n')


def main():
    # Gather data for known Russian accounts
    # with open('../data/ira_handles_june_2018.txt') as f:
    #     gather_data(f.readlines())

    # Gather data for known regular accounts
    with open("../data/election-data-sample.txt") as f:
        gather_data_by_tweet_ids(f.readlines())


if __name__ == "__main__":
    main()
