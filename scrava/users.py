import requests,pickle
import http
from bs4 import BeautifulSoup
import os
import json
from pathlib import Path
import tempfile

class UserSpider:

    URL_ATHLETE = 'https://www.strava.com/athletes/'
    URL_SEARCH = "https://www.strava.com/athletes/search?text="
    URL_SEARCH_MORE = "https://www.strava.com/athletes/search?page="
    USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}


    def __init__(self):

        self.session = self._create_sess()
        self.cookies = None
        self.name = None
        self.output = None
        

    def _create_sess(self):
        ''' Create session and load cookies got in previous login '''
        session = requests.Session()
        
        if(Path(tempfile.gettempdir() + "cookies.json").is_file()):
            self.cookies = json.loads(Path(tempfile.gettempdir() + "cookies.json").read_text())  
            self.cookies = requests.utils.cookiejar_from_dict(self.cookies)
            session.cookies.update(self.cookies)
        else:
            raise Exception()
        return session
    
    def __check_response(self, response):
        ''' Check requests are authenticated '''
        response.raise_for_status()
        if "class='logged-out" in response.text:
            raise Exception()
        return response
    
    def _get(self,url):
        ''' GET requests '''
        res = self.session.get(url,headers=UserSpider.USER_AGENT,allow_redirects=True)
        self.__check_response(res)
        return res.content
    
    def athelete_response(self,data_response):
        ''' Use bs4 to get desired elements from response '''
        soup = BeautifulSoup(data_response,'html.parser')
        results = soup.find_all('script',type='application/ld+json')
        athlete = None
        for a in results:
            if 'Person' in a.text:
                athlete = a
        json_object = json.loads(athlete.text)
        name = json_object['name']
        description = json_object['description']
        image = json_object['image']
        data = {
            'name': name,
            'description': description,
            'image': image
        }

        print(data)

        return data

    
    def user_search(self,name:str,output):
        ''' GET results from search '''
        self.name = name
        self.output = output
        data_res = self._get(self.URL_SEARCH + name)
        to_json = self.__data_former(data_res)
        if self.output:
            self.__json_to_file(to_json,self.output)

    def __data_former(self,result):
        ''' Create search output with name and id '''
        soup = BeautifulSoup(result,'html.parser')
        res = soup.find_all("a", class_="athlete-name-link")
        search_res = []

        for a in res:
            data = {
                'name': a.string,
                'id': a.get("data-athlete-id")
            }
            search_res.append(data)

        if len(search_res) == 0:
            print("--- No more results ---")
        else: 
            for i in search_res:
                print(i)
        
        return search_res


    def next_page(self,page):
        ''' Move to the page provided '''
        data_res = self._get(self.URL_SEARCH_MORE + str(page) + "&text=" + self.name)
        print("----- Page " + page + " -----")
        to_json = self.__data_former(data_res)
        if self.output:
            self.__json_to_file(to_json,self.output)
        
            
    def athlete_info(self, list_id:str, output, file=False):
        ''' Get user info '''
        atheletes = []
        ids = []
        if file:
            with open(list_id,"r") as f:
                for x in f.readlines():
                    ids.append(x)
        else:
            ids = list_id
            ids = ids.split(',')
            

        for i in ids:
            print(i)
            data_file = self._get(self.URL_ATHLETE + i)
            ath = self.athelete_response(data_file)
            atheletes.append(ath)
        if output:
            self.__json_to_file(atheletes,output)
    
    def __json_to_file(self,ath_list,output):
        ''' Dump Json to file provided '''
        with open(output, "w") as file:
            json.dump(ath_list, file)


