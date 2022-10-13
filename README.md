# Reddit in portuguese (ETL)
Backend server to extract, load and transform data of subreddits from Brazil and Portugal

This project is developed in Django and its objective is to extract historical data from subreddits whose main language is Portuguese, and store this data in a Postgresql database hosted on Heroku.

![img](img/backend.png)

Extracts were performed using the PRAW library, the Reddit API and the Pushshift API to capture historical data.

The generated dataset was summarized in a CSV file available on [Kaggle](https://kaggle.com/datasets/5c88220933ffba84019a6163d019ab90bfbe89d13253482e14cfca4626cb38af).

Some access keys were used, if you want to adapt this repository to another project, you will need to create an .env file with information about access keys, databases and django-specific information.

```
.env

# Reddit auth
REDDITUSER=''
REDDITKEY=''
REDDITID=''

# Django
SECRET_KEY=''
DEBUG=

# Database
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''
```
