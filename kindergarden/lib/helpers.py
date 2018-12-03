# -*- coding: utf-8 -*-

from markdown2 import markdown as text2markdown

from pyramid.threadlocal import get_current_registry

from webhelpers2.html import escape, HTML, literal, url_escape
from webhelpers2.html.tags import *
from webhelpers2.text import truncate
from webhelpers2.html.tools import nl2br

from pytils.numeral import choose_plural, get_plural

from kindergarden.lib.paginate import page


def markdown(text):
    return text2markdown(text)
