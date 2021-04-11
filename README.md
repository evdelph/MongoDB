# MongoDB Pipeline Project Using Reddit Data

This repo will walk you through executing an end-to-end data pipeline using the Reddit API, MongoDB, MongoShell, and Jupyter Notebooks. 

## Getting Started

You will need the following to reproduce the work:

1. IU Jetstream Account OR MongoShell
2. Python 3.8 or greater
3. Reddit API Account
4. Files: mongo.py, credientials.py, and requirements.txt

### Setting up Reddit API and credentials.py

To utilize mongo.py, you will need to set-up a Twitter API account. Fill out this form [here](https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform).

From the API set-up step, you will need a **client id key**,**client secret key**, and **user agent key**. In credentials.py, update the file by manually writing in credentials:
```
client_id = "your client id"
client_secret = "your client secret"
user_agent = "your user agent"
```
Without this, you will be unable to utilize the API functionality in mongo.py, and data will not be retrieved.

### Setting up mongoshell

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
