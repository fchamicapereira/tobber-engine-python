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
import re
from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin

import dryscrape
import pytesseract
from PIL import Image

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')

class ThreatDefenceRedirectMiddleware(RedirectMiddleware):

    def __init__(self, settings):
        super(ThreatDefenceRedirectMiddleware, self).__init__(settings)

        # start xvfb to support headless scraping
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        self.dryscrape_session = dryscrape.Session(base_url='https://rarbg.is')

    def bypass_threat_defense(self, url=None):

        # only navigate if any explicit url is provided
        if url:
            self.dryscrape_session.visit(url)

        if 'defence=1' in self.dryscrape_session.url():
            print self.dryscrape_session.xpath('//script')[0]

            #value_sk = re.search('value_sk = \\\'([a-zA-Z0-9]*)',self.dryscrape_session.xpath('//script')[0]).group(1)
            #print 'value_sk=',value_sk

            #ref_cookie = 'rarbg.is'
            #print 'ref_cookie=',ref_cookie

            #url = 'https://rarbg.is/threat_defence.php?defence=2&sk='+value_sk+'&ref_cookie='+ref_cookie+'&r=65217491'
            #self.wait_for_redirect(url)


        # solve the captcha if there is one
        captcha_images = self.dryscrape_session.xpath('//img[contains(@src,"captcha")]')

        print 'captcha:', captcha_images

        if len(captcha_images) > 0:
            return self.solve_captcha(captcha_images[0])

        # click on any explicit retry links
        retry_links = self.dryscrape_session.css('a[href *= threat_defense]')
        if len(retry_links) > 0:
            return self.bypass_threat_defense(retry_links[0].get_attr('href'))

        # otherwise, we're on a redirect page so wait for the redirect and try again
        return self.wait_for_redirect()
        return self.bypass_threat_defense()

    def solve_captcha(self, img, width=1280, height=800):

        # take a screenshot of the page
        self.dryscrape_session.set_viewport_size(width, height)
        filename = tempfile.mktemp('.png')
        self.dryscrape_session.render(filename, width, height)

        # inject javascript to find the bounds of the captcha
        js = 'document.querySelector("img[src *= captcha]").getBoundingClientRect()'
        rect = self.dryscrape_session.eval_script(js)
        box = (int(rect['left']), int(rect['top']), int(rect['right']), int(rect['bottom']))

        # solve the captcha in the screenshot
        image = Image.open(filename)
        os.unlink(filename)
        captcha_image = image.crop(box)
        captcha = pytesseract.image_to_string(captcha_image)
        print 'Solved the captcha:', captcha

        # submit the captcha
        input = self.dryscrape_session.xpath('//input[@id = "solve_string"]')[0]
        input.set(captcha)
        button = self.dryscrape_session.xpath('//button[@id = "button_submit"]')[0]
        url = self.dryscrape_session.url()
        button.click()

        # try again if it we redirect to a threat defense URL
        #if self.is_threat_defense_url(self.wait_for_redirect(url)):
        #    return self.bypass_threat_defense()

        # otherwise return the cookies as a dict
        cookies = {}
        for cookie_string in self.dryscrape_session.cookies():
            if 'domain=rarbg.is' in cookie_string:
                key, value = cookie_string.split(';')[0].split('=')
                cookies[key] = value
        return cookies

    def wait_for_redirect(self, url = None, wait = 10):
        url = url or self.dryscrape_session.url()

        for i in range(int(wait)):
            time.sleep(wait)
            if self.dryscrape_session.url() != url:
                return self.dryscrape_session.url()

        #return self.dryscrape_session.url()

        print 'Maybe', self.dryscrape_session.url(), 'isn\'t a redirect URL?'

        return {
        }
        #raise Exception('Timed out on the threat defense redirect page.')

    def _redirect(self, redirected, request, spider, reason):

        #if this isnt a threat defence redirect, just bypass this
        if not self.is_threat_defense_url(redirected.url):
            return super(ThreatDefenceRedirectMiddleware, self)._redirect(redirected, request, spider, reason)

        print 'Threat defense triggered for', request.url
        print 'Redirected url:', redirected.url

        #request.cookies = self.bypass_threat_defense(redirected.url)
        #request.dont_filter = True
        return redirected

    def is_threat_defense_url(self, url):
        return 'threat_defense.php' in url or 'threat_defence.php' in url

    def process_response(self, request, response, spider):

        if (request.meta.get('dont_redirect', False) or
            response.status in getattr(spider, 'handle_httpstatus_list', []) or
            response.status in request.meta.get('handle_httpstatus_list', []) or
            request.meta.get('handle_httpstatus_all', False)):

            return response

        allowed_status = (301, 302, 303, 307, 308)

        print 'HEY'
        print response

        if 'Location' not in response.headers or response.status not in allowed_status:
            return response

        location = safe_url_string(response.headers['location'])

        redirected_url = urljoin(request.url, location)

        if response.status in (301, 307, 308) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        redirected = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(redirected, request, spider, response.status)
