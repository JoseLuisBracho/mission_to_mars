# Modules
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from dbconfig import pwd

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri=(f'mongodb+srv://JoseLuisBracho:{pwd}@joseluis-nu3ar.mongodb.net/test'))

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape/")
def scrape_fun():
    from scrape_mars import scrape
    # Run the scrape function
    mars = scrape()   # Function that returns a dict scrape

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)