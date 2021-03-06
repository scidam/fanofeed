# -*- coding: utf-8 -*-
# Create your views here.

from django.template.loader import render_to_string
from django.http import HttpResponse
import feedparser
from django.views.decorators.cache import cache_page
from .settings import FEED_URLS
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
import ssl


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def return_block(request, objs):
    if objs:
        return HttpResponse(render_to_string('feeddata.html', {'objs': objs}),
                            content_type='text/plain')
    else:
        return HttpResponse('', content_type='text/plain')


def parse_by_url(url):
    try:
        objs = []
        data = feedparser.parse(url)
        for item in data['entries']:
            objs.append({'title': strip_tags(item['title']),
                         'published': feedparser._parse_date(item['published']),
                         'link': item['link']})
            objs.sort(key=lambda x: x['published'])
            objs = objs[::-1]
    except:  # everything can happened here
        objs = []
    return objs


@cache_page(FEED_URLS[0][3])
def ras_parser(request):
    objs = parse_by_url(FEED_URLS[0][0])
    return return_block(request, objs[:FEED_URLS[0][-1]])


@cache_page(FEED_URLS[1][3])
def minobr_parser(request):
    objs = parse_by_url(FEED_URLS[1][0])
    return return_block(request, objs[:FEED_URLS[1][-1]])
