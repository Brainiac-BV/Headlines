import feedparser
from flask import Flask, render_template, request
import json
import urllib, urllib2


# app instantiation
app = Flask(__name__)

# set feed dictionary
RSS_FEED = {'deadspin': 'http://deadspin.com/rss',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}

# static routing implementation. would have to create one for each key in RSS_FEED
# @app.route('/')
# @app.route('/deadspin')
# def deadspin():
#    return get_news('deadspin')


# primary view function, implementing dynamic routing
@app.route('/')
# @app.route('/<publication>')
# remember to set default value for variable passed from url using parameter
# in view method when using dynamic routing
def get_news():
    query = request.args.get('publication')
    # search function. search parameters used as input to publication var
    if not query or query.lower() not in RSS_FEED:
        publication = 'deadspin'
    else:
        publication = query.lower()
    #weather_query = request.args.get('weather')
    feed = feedparser.parse(RSS_FEED[publication])
    first_article = feed['entries']
    weather = get_weather('london')
    return render_template('home.html', articles=first_article, weather_results=weather)


# grab weather data from openweather api
def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=0909f34b913d568cd0c529c8e464fea2'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description':parsed['weather'][0]['description'],'temperature':parsed['main']['temp'],'city':parsed['name']}

    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
