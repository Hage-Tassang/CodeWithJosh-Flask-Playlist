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
    query = request.args.get("query","latest")
    sort_by = request.args.get('sortBy', 'popularity')
    trending = f"https://newsapi.org/v2/everything?q={sort_by}&apiKey={NEWS_API_KEY}"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    response2 = requests.get(trending)
    trends = response2.json()
    news_data = response.json()
    #print(news_data)
    
    articles = news_data.get('articles',[])
    filtered_articles =  [article for article in articles if "Yahoo" not in article['source']['name'] and "BBC" not in article['source']['name'] and "removed" not in article['source']['name'].lower()]
    return render_template("index.html",articles=filtered_articles, query = query,trends = trends) 

if __name__ == "__main__":
    app.run(debug=True)

