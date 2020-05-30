 
from sanic import Sanic
import sanic
import requests
import datetime
import json
from bs4 import BeautifulSoup
import logging
import se_parser

# Step one: parse homepage and collect questions 
home_page = "https://stackexchange.com/?pagesize=50"

app = Sanic()

@app.route('/')
async def test(request):
    return sanic.response.json({"text":se_parser.workflow()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)