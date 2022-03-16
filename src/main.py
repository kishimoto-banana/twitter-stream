import abc
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime

import tweepy
from tweepy.tweet import Tweet as tweepyTweet


@dataclass
class Tweet:
    id: str
    text: str
    language: str
    created_at: datetime


class TweetRepository(abc.ABC):
    @abc.abstractclassmethod
    def write_tweet(self, tweet: Tweet):
        raise NotImplementedError


class TweetSqlite(TweetRepository):
    def __init__(self):
        self.conn = sqlite3.connect("data/tweet.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY AUTOINCREMENT, tweet_id TEXT, text TEXT, language Text, tweeted_at TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )

    def write_tweet(self, tweet: Tweet):
        self.cur.execute(
            "INSERT INTO tweets(tweet_id, text, language, tweeted_at) values(?, ?, ?, ?)",
            (tweet.id, tweet.text, tweet.language, tweet.created_at),
        )
        self.conn.commit()


class TweetStream(tweepy.StreamingClient):
    def __init__(self, bearer_token: str, tweet_repo: TweetRepository):
        super().__init__(bearer_token)
        self.tweet_repo = tweet_repo

    def on_tweet(self, stream_tweet: tweepyTweet):
        tweet = Tweet(
            id=stream_tweet.id,
            text=stream_tweet.text,
            language=stream_tweet.lang,
            created_at=stream_tweet.created_at,
        )
        try:
            self.tweet_repo.write_tweet(tweet)
        except Exception as e:
            print(f"database: {e}")

    def on_errors(self, errors):
        print(errors)


def main():
    bearer_token = os.environ["BEARER_TOKEN"]
    tweet_repo = TweetSqlite()
    listener = TweetStream(bearer_token, tweet_repo)
    try:
        print("listen stream")
        listener.sample(tweet_fields=["created_at", "lang"], place_fields=["geo"])
    except Exception as e:
        print(e)
    finally:
        tweet_repo.conn.close()


if __name__ == "__main__":
    main()
