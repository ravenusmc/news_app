#importing outside libraries for use in the project
from flask import Flask, session, redirect, url_for, escape, render_template, request
import requests

#Setting up Flask
app = Flask(__name__)

@app.route('/')
def login():
    url = "https://newsapi.org/v1/articles?source=techcrunch&apiKey=61d27504cb064eaf912be90e31803d5d"
    r = requests.get(url)
    response_dict = r.json()
    image = response_dict['articles'][0]['urlToImage']
    news_title = response_dict['articles'][0]['title']
    url = response_dict['articles'][0]['url']
    print(image)
    name = "Mike Hope"
    return render_template('index.html', title='Login Page')

#This line will actually run the app.
if __name__ == '__main__':
    app.run(debug=True)