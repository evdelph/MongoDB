# MongoDB Pipeline Project Using Reddit Data

This repo will walk you through executing an end-to-end data pipeline using the Reddit API, MongoDB, MongoShell, and Jupyter Notebooks. 

## Getting Started

You will need the following to reproduce the work:

1. IU Jetstream Account OR MongoShell
2. Python 3.8 or greater
3. Reddit API Account
4. Files: mongo.py, credientials.py, and requirements.txt

### Setting up Reddit API and credentials.py

To utilize mongo.py, you will need to set-up a Twitter API account. Go to this link  [here](https://www.reddit.com/prefs/apps) and do the following:

1. Give your bot a name
2. Selected **script** for api type
3. Write a brief description
4. Click **create app**

You will have your **client id**, **client secret key**, and **user agent key** ready for use. The last step is to copy and paste your credentials in credentials.py as strings. You will need to do this manually.
```
client_id = "your client id"
client_secret = "your client secret"
user_agent = "your user agent"
```
Without this, you will be unable to utilize the API functionality in mongo.py, and data will not be retrieved.

### Setting up mongo shell

Reddit data will be be ingested via the API and stored in a MongoDB database. To run mongo commands, you will either need to use a VM with mongo shell pre-installed, or install mongo shell on your desktop. For the VM, I used IU Jetstream, but any VM will work. To install mongo shell on your personal device, follow the steps below:

1. Download mongo shell [here](https://www.mongodb.com/try/download/shell)
2. Add mongo shell binary to path (to be done in the command line)
```
touch ~/.bash_profile
open ~/.bash_profile
export PATH="<mongo-directory?.bin:$PATH" # type this into bash_profile
# save and exit file
source ~/.bash_profile
echo $PATH
```

To confirm, enter the "mongo" command in your command line. The following will appear if your installation and sourcing worked:
```
MongoDB shell version v4.4.5
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
```

## Running mongo.py

Below shows the arguments for running mongo.py
```
$ ./mongo.py --help
usage: mongo.py [-h] [--p P] r

This script takes in a subreddit handle (required) and destination path folder
(optional). This outputs a mongodb document.

positional arguments:
  r           subreddit

optional arguments:
  -h, --help  show this help message and exit
  --p P       destination path

```

The following fields are included in the output:

1. Post ID
2. Number of Comments
3. Post Created (Timestamp)
4. Post Score
5. Post Upvote Ratio
6. Post Ups
7. Post Downs
8. Post Title
9. Post Body
10. Replies

For this demostration, the subreddit cgrpMigraine was utilized.

**Run script without destination path**
Without the destination path specified, the JSON file will be outputted in your current working directory.
```
./mongo.py cgrpMigraine
```

**Run script with destination path**
With the destination path specified, the JSON file will be outputted in the path you entered
```
./mongo.py cgrpMigraine /users/Desktop
```

Successful completion of the script will result in the following message:
```
MongoDB Doc Located at C:\Users\evdelph\Desktop\I535\ProjectB\cgrpMigraine.json
```

## Utilizing MongoDB Database
A MongoDB database called Reddit has been created to on MongoDB Atlas. You will have the ability to create, delete, and edit existing collections in the database. To access the database run this following commands:
```
mongo "mongodb+srv://cluster0.c7slc.mongodb.net/Reddit" --username user --password ProjectB!
use Reddit
```
### Create a collection
It is assumed that there will be one collection for every subreddit. To create a collection, run the following command:
```
db.createCollection('yoursubreddit')

# Successful message

MongoDB Enterprise atlas-8fho22-shard-0:PRIMARY> db.createCollection('cgrpMigraine')
{
        "ok" : 1,
        "$clusterTime" : {
                "clusterTime" : Timestamp(1618077435, 1),
                "signature" : {
                        "hash" : BinData(0,"v1tomRMDk3jnGNKkzLqGHccpiX4="),
                        "keyId" : NumberLong("6937724079830990851")
                }
        },
        "operationTime" : Timestamp(1618077435, 1)
}

```

### Load JSON into database
Run the following commands to load your file as a collection.
```
# load cgrpMigraine.json data
var file = cat('cgrpMigraine.json')
var parsed_file = JSON.parse(file)
db.cgrpMigraine.insert(parsed_file)


# if successful
BulkWriteResult({
        "writeErrors" : [ ],
        "writeConcernErrors" : [ ],
        "nInserted" : 719,
        "nUpserted" : 0,
        "nMatched" : 0,
        "nModified" : 0,
        "nRemoved" : 0,
        "upserted" : [ ]
})

# Verify the entries loaded into the database
db.cgrpMigraine.count()
>> 719
```

### Basic Queries
MongoDB allows your to query based on key words. In this case, I was interested in finding out how many posts that mentioned the drug "aimovig" that received more that 15 likes. The query is shown below:
```
db.cgrpMigraine.find({body: /.*imovig.*/, score: {$gt: 15}}).count()
>>20
```
### Export Results
To export results, follow the format below:
```
# Basic structure
mongoexport --uri="mongodb+srv://cluster0.c7slc.mongodb.net/Reddit" --username user --password ProjectB!/
--collection=cgrpMigraine --query='' --fields field1,field2 --type csv --out yourfile.csv

# Output posts based on query
mongoexport --uri="mongodb+srv://cluster0.c7slc.mongodb.net/Reddit" --username user --password ProjectB!/
--collection=cgrpMigraine --query='{"body":{"$regex":".*imovig*.","$options":""},"score":{"$gt":15}}'/
--fields body,score --type csv --out posts.csv

# Output replies based on query
mongoexport --uri="mongodb+srv://cluster0.c7slc.mongodb.net/Reddit" --username user --password ProjectB! /
--collection=cgrpMigraine --query='{"body":{"$regex":".*imovig*.","$options":""},"score":{"$gt":15}}'/
--fields replies,score --type csv --out replies.csv

# Output all posts containing aimovig
mongoexport --uri="mongodb+srv://cluster0.c7slc.mongodb.net/Reddit" --username user --password ProjectB!/
--collection=cgrpMigraine --query='{"body":{"$regex":".*imovig*.","$options":""},"score":{"$gt":-1}}' /
--fields created_at,ups,upvote_ratio,downs,body --type csv --out timestamps.csv
```
The files post.csv and replies.csv are provided in the repo. I provided another file called `exploded_timestamps.csv`. I used [pyspark](https://spark.apache.org/docs/latest/api/python/index.html) create a dataframe of words from the post. It is recommended to use a VM for this step.

## Data Analysis and Visualization
The [RedditNLP.ipynb](https://github.com/evdelph/MongoDB/blob/main/Visualizations/RedditNLP.ipynb) notebook contains step by step instructions how to analyze exported Reddit data. In this example, I looked at frequent unigrams and bigrams over the three cgrp autoinjector medications: Aimovig, Ajovy, and Emgality. I also conducted LDA topic clustering.

The [RedditTimestamps.ipynb](https://github.com/evdelph/MongoDB/blob/main/Visualizations/RedditTimestamps.ipynb) notebook shows word usage over time. Visualizations include a Treemap, Heatmap, and Scatterplot.

