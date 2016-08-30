from flask import Flask
import requests
import operator
from bs4 import BeautifulSoup
from flask import render_template
from collections import OrderedDict

app = Flask(__name__)

@app.route("/")
def index():
        url = 'http://avalon.law.yale.edu/19th_century/gettyb.asp'
        response = requests.get(url)
        html = response.content

        soup = BeautifulSoup(html, "html.parser")
        paragraph = soup.find('p').get_text().lower()
        paragraph = paragraph.replace(',', '').replace('.', '').replace('\"', '').replace('--', ' ').replace('-', ' ')
        paragraph_list = paragraph.split()

        dictionary = {}

        for item in paragraph_list:
            if item not in dictionary:
                dictionary[item] = 1
            else:
                dictionary[item] = dictionary.get(item, 0) + 1


        #sort words by their frequencies and print out the top 10
        sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
        dictionary_sorted = OrderedDict()

        count = 0
        for k, v in reversed(sorted_dictionary):
            if count < 10:
                dictionary_sorted.setdefault(k, v)
                count += 1


        return render_template('index.html',
                               dictionary=dictionary,
                               dictionary_sorted=dictionary_sorted)

if __name__ == "__main__":
        #app.run(host="0.0.0.0", port=5000)
        app.run()