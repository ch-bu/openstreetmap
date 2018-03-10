# OpenStreetMap project from Udacity

A project for the data science nanodegree from Udacity. The project uses
data munging techniques to wrangle a dataset from the [OpenStreetMap database](https://www.openstreetmap.org/).
For this project I chose the [city of Freiburg](https://en.wikipedia.org/wiki/Freiburg_im_Breisgau).

## Installation

1. [Install MongoDB](https://docs.mongodb.com/manual/installation/)
2. [Install pymongo for python](https://api.mongodb.com/python/current/installation.html)
3. Create mongodb directory: `mkdir mongodb`
4. Run mongodb: `mongod --dbpath ./mongdb`
5. Insert data into database: `python3 scripts/osm_to_mongo.py freiburg_sample.osm`
6. Run Jupyter Notebook: `jupyter notebook project_description.ipynb`
7. If you change the notebook you can export the notebook to html via: `jupyter nbconvert --to html project_description.ipynb`

## Files

* **project_description.ipynb**: A jupyter notebook that is the basis for the html file
* **freiburg.osm**: The whole map (87MB)
* **freiburg_sample.osm**: A subset of freiburg.osm
* **scripts/osm_to_mongo.py**: A script that audits the data and puts it into the mongo database
* **scripts/query.py**: They queries used in the juypter notebook in a standalone python script
