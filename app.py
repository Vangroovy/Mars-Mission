from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Set up Flask#
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Create results home page using data from Mongo
@app.route("/")
def root():
    destination_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=destination_data)

#Trigger the scrape function
@app.route("/scrape")
def scrape():

    #run the scrape
    MarsData = scrape_mars.scrape_info()

    #Update the Mongo database using update and upsert = True
    mongo.db.collection.update({}, MarsData, upsert=True)

    #Redirect back to home page
    return redirect('/')

#Define behaviour
if __name__ == '__main__':
    app.run(debug = True)