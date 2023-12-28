import requests,pickle
import http
from bs4 import BeautifulSoup
import os
import json
from pathlib import Path

class UserSpider:

    URL_ATHLETE = 'https://www.strava.com/athletes/'
    USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}


    def __init__(self):

        self.session = self._create_sess()
        self.cookies = None
        self.id = ['56868533','17154043','5952380']
        

    def _create_sess(self):

        session = requests.Session()
        
        if(Path("cookies.json").is_file()):
            self.cookies = json.loads(Path("cookies.json").read_text())  # save them to file as JSON
            self.cookies = requests.utils.cookiejar_from_dict(self.cookies)  # turn dict to cookiejar
            session.cookies.update(self.cookies)  # load cookiejar to current session
        
        return session
    
    def __check_response(self, response):
        response.raise_for_status()
        if "class='logged-out" in response.text:
            raise Exception()
        return response
    
    def _get(self,url,id):

        res = self.session.get(url + id,headers=UserSpider.USER_AGENT,allow_redirects=True)
        self.__check_response(res)
        soup = BeautifulSoup(res.content,'html.parser')
        athlete = soup.find_all('script',type='application/ld+json')
        json_object = json.loads(athlete[1].text)
        name = json_object['name']
        description = json_object['description']
        image = json_object['image']
        data = {
            'name': name,
            'description': description,
            'image': image
        }
        
        return data
            
    def athlete_info(self):
        atheletes = []
        for i in self.id:
            data_file = self._get(self.URL_ATHLETE,i)
            atheletes.append(data_file)
        self.__json_to_file(atheletes)
    
    def __json_to_file(self,ath_list):
        with open("users_data.json", "w") as file:
            json.dump(ath_list, file)



user = UserSpider()
user.athlete_info()