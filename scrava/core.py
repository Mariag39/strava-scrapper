import requests,pickle
import http
from bs4 import BeautifulSoup
import os
import json
from pathlib import Path
import tempfile

class StravaSpider:
    start_url = 'https://www.strava.com/login'
    url_session = 'https://www.strava.com/session'
    CSRF_H = 'x-csrf-token'
    USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}
    csrf_token = None


    def __init__(self):
        self.sess = self.__create_sess()
        self.cookies = None

    def __create_sess(self):
        ''' Create session with request '''
        session = requests.Session()
        return session


    def __store_response(self, response):
        ''' Get csrf-token to put in headers when login'''
        self.response = response
        self.soup = BeautifulSoup(response.text, 'lxml')
        meta = self.soup.find('meta',attrs={'name':'csrf-token'})
        if meta:
            self.csrf_token = meta['content']
        
        return response

    def login(self,email, password):
        ''' Get data from login url and send it to session url as authentication'''
        self.logout()
        response = self.sess.get(self.start_url,headers=StravaSpider.USER_AGENT, allow_redirects=True)
        self.__store_response(response)
        soup = BeautifulSoup(response.content, 'lxml')
        token = soup.find_all('input',{
            'name': 'authenticity_token'})[0].get('value')
        utf8 = soup.find_all('input',
                             {'name': 'utf8'})[0].get('value').encode('utf-8')
        
        log_data = {
            'utf8': utf8,
            'email': email,
            'password': password,
            'authenticity_token': token,
        }
        
        csrf_header = {}
        if self.csrf_token: csrf_header[StravaSpider.CSRF_H] = self.csrf_token

        headers = {**StravaSpider.USER_AGENT, **csrf_header}

        self.sess.post(StravaSpider.url_session,headers=headers,data=log_data,allow_redirects=False)
        if response.status_code == 302 and response.headers['Location'] == StravaSpider.start_url:
            raise Exception
        
        # Keep cookies in temp dir to use them later
        self.cookies = self.sess.cookies.get_dict()
        self.cookies = requests.utils.dict_from_cookiejar(self.sess.cookies)  # turn cookiejar into dict
        Path(tempfile.gettempdir() + "cookies.json").write_text(json.dumps(self.cookies))
        self.__check_login()

        return response

    def __check_login(self):
        ''' Check login was successfull '''
        res = self.sess.get("https://www.strava.com/onboarding",headers=StravaSpider.USER_AGENT,allow_redirects=True)
        soup = BeautifulSoup(res.content,'html.parser')
        try:
            assert("logged-in" in res.text)
        except Exception as e:
            print('Not logged in')

    def logout(self):
        self.sess.cookies.clear()
        self.sess.close()
