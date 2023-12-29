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
        

    def _create_sess(self):

        session = requests.Session()
        
        if(Path("../files/cookies.json").is_file()):
            self.cookies = json.loads(Path("../files/cookies.json").read_text())  
            self.cookies = requests.utils.cookiejar_from_dict(self.cookies)
            session.cookies.update(self.cookies)
        else:
            raise Exception()
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
        results = soup.find_all('script',type='application/ld+json')
        athlete = None
        for a in results:
            if 'Person' in a.text:
                athlete = a
        print(athlete)
        json_object = json.loads(athlete.text)
        name = json_object['name']
        description = json_object['description']
        image = json_object['image']
        data = {
            'name': name,
            'description': description,
            'image': image
        }
        
        return data
            
    def athlete_info(self, list_id:str, output, file=None):
        atheletes = []
        if file != None:
            list_id = []
            with open(file,"r") as f:
                for x in f.readlines():
                    list_id.append(x)
        else:
            list_id = list_id.split(',')
        
        for i in list_id:
            print(i)
            data_file = self._get(self.URL_ATHLETE,i)
            atheletes.append(data_file)
        self.__json_to_file(atheletes,output)
    
    def __json_to_file(self,ath_list,output):
        with open(output, "w") as file:
            json.dump(ath_list, file)

