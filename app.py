from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

#Set up Flask#
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Create results home page using data from Mongo
@app.route("/")
def root():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", space=mars)

#Trigger the scrape function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({},mars_data, upsert=True)
    #run the scrape function
    #mars = scrape_mars.scrape_info()

    #Update the Mongo database using update and upsert = True
    #mongo.db.collection.update({}, mars, upsert=True)

    #Redirect back to home page
    return redirect('/')

#Define behaviour
if __name__ == '__main__':
    app.run(debug = True)