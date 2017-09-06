# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

# class UserAgentMiddleware(object):
#     def process_request(self, request, spider):
#         ua  = spider.settings.get('USER_AGENT_LIST')[0]
#         request.headers.setdefault('User-Agent', ua)

import os, tempfile, time, sys, logging
logger = logging.getLogger(__name__)

import dryscrape
import pytesseract
from PIL import Image

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')

class ThreatDefenceRedirectMiddleware(RedirectMiddleware):
    def _redirect(self, redirected, request, spider, reason):

        #if this isnt a threat defence redirect, just bypass this
        if not self.is_threat_defense_url(redirected.url):
            return super()._redirect(redirected, request, spider, reason)

        logger.debug(f'Threat defense triggered for {request.url}')
        request.cookies = self.bypass_threat_defense(redirected.url)
        request.dont_filter = True
        return request

        def is_threat_defense_url(self, url):
            return threat_defense.php in url
