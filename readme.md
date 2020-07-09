# Description
E-commerce mock-up written in Django. 
Check it out at http://market.encina.xyz !

# Powered by
* Django
* Bootstrap
* Owl Carousel
* AOS library
* Deployed in Google Cloud
* Statics served from AWS S3
* Emails sent with Sendgrid

# Using locally
## Environment variables
Set up the following environment variables in a .env file at the root folder:

* SECRET_KEY
* STORE_OWNER_EMAIL
* SENDGRID_API_KEY
* SQLITE=(any string)

If you want to use AWS S3:
* AWS=(any string)
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME

If you want to use Google Cloud SQL (e.g. Postgres), don't set up SQLITE and do set up the following:

* DB_CONNECTION_NAME
* DB_NAME
* DB_USER
* DB_PASSWORD

And then run the following commands on a terminal to set up the proxy

    chmod +x cloud_sql_proxy
    ./cloud_sql_proxy -instances="YOUR_PROJECT_INSTANCE"=tcp:5432

# Pre-loading the database
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py loaddata market_project/fixtures/default_data.json

