#!/usr/bin/env python

# imports
import credentials as creds 
import re
import praw
import prawcore
import argparse
import json
import os

class RedditClient(object):

    def __init__(self,subreddit,path):
        """
        Take in subreddit and make API call
        """
        # class takes in subreddit handle and destination path
        self.subreddit = subreddit
        self.path = path

        # credentials
        self.client_secret = creds.client_secret
        self.user_agent = creds.user_agent
        self.client_id = creds.client_id

        # instantiate reddit instance
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent=self.user_agent)

        # make api call
        self.posts = None
        
        try:
            self.posts = self.reddit.subreddit(self.subreddit).hot(limit=10)
            print(f'API Call Successful!')
        except:
            print(f'Sorry, {self.subreddit} does not exist. Please try again.')


    def cleanse_data(self,data):
        """
        Remove white spaces and extra characters
        """
        pattern = r'[\/\n\'""]'
        return re.sub(pattern,"", data.strip(), flags=re.UNICODE)

    def create_mongodb_docs(self):
        """
        Converts api output into mongodb document format
        """
        print(f'Creating MongoDB Docs.................')
        mongo_docs = []

        for post in self.posts:

            comments = []
            comment_docs = {}

            # cleanse text body
            body = self.cleanse_data(post.selftext)

            # iterate to store comments in json format
            i = 0
            for comment in post.comments:

                i += 1
                comment_ = self.cleanse_data(comment.body)
                comment_docs['comment_'+str(i)] = comment_
            
            comments.append(comment_docs)

        # append all components to mongodb_doc
        mongo_docs.append(
        {'id': post.id,
        'num_comments': post.num_comments,
        'created_at': post.created,
        'score': post.score,
        'title': post.title,
        'body': body,
        'replies':comments}
    )

        return mongo_docs

    def output_mongodoc(self):
        """
        Execute and export mongodoc
        """
        # get mongodb output
        mongodoc_output = self.create_mongodb_docs()

        # set outputfile to subreddit
        filepath = self.path+"\\"+self.subreddit+".json"
        with open(filepath,'w') as outfile:
            json.dump(mongodoc_output,outfile)
        
        print(f'MongoDB Doc Located at {filepath}')

if __name__ == "__main__":

    # set up parser
    parser = argparse.ArgumentParser(description="This script takes in a subreddit handle (required) and destination path folder (optional). This outputs a mongodb document.")
    parser.add_argument('r',help='subreddit')
    parser.add_argument('--p',help='destination path')
    args = parser.parse_args()

    # set destination path
    dest_path = None
    if not args.p:
        dest_path = os.getcwd()
    else:
        dest_path = args.p

    client = RedditClient(args.r,dest_path)
    client.output_mongodoc()