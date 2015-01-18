#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Stefan van der Walt'
SITENAME = 'Stéfan van der Walt'
SITESUBTITLE = 'What I talk about when I talk about coding'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Homepage', 'http://mentat.za.net/'),
         ('scikit-image', 'https://scikit-image.org/'),
         )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Porting from Octopress to Pelican
# From https://jakevdp.github.io/blog/2013/05/07/migrating-from-octopress-to-pelican/
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
STATIC_PATHS = ['images', 'figures', 'downloads']

THEME = 'theme/pelican-octopress-theme'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['liquid_tags.img', 'liquid_tags.video', 'liquid_tags.include_code',
           'liquid_tags.notebook']
