#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Stefan van der Walt'
SITENAME = 'Stéfan van der Walt'
#SITESUBTITLE = ''
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Homepage', 'http://mentat.za.net/'),
#         ('scikit-image', 'https://scikit-image.org/'),
#         )

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
PLUGINS = ['summary'] # 'org_reader'

# Correctly grab slug
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'


# The following markdown extension will remove any comments
# of the form <!---   text -->   (note the three opening dashes)
# from article input.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                'plugins_md/comments'))
from mkdcomments import CommentsExtension

MARKDOWN = {
    'extensions': ['markdown.extensions.fenced_code',
                   'markdown.extensions.extra',
                   'markdown.extensions.sane_lists',
                   'markdown.extensions.smarty',
                   'markdown.extensions.toc',
                   'markdown.extensions.codehilite',
                   CommentsExtension()],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight',
                                           'linenums': False}
        }
    }

GITHUB_USER = 'stefanv'
TWITTER_USER = 'stefanvdwalt'
TWITTER_FOLLOW_BUTTON = True
SEARCH_BOX = True
#X_MIN_READ = True
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = [('Home', 'http://mentat.za.net/blog'),
             ('mentat.za.net', 'http://mentat.za.net'),
             ('scikit-image', 'http://skimage.org')]
