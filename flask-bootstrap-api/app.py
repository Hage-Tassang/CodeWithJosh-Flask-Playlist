from flask import Flask,request,render_template
import requests
#creating a seperate api key from main file
from config import NEWS_API_KEY


#create a flask app

app =  Flask(__name__)

#common struc but we will be building single page web app
#Home / About / Contact /Pricing
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)