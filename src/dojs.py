import os
import json
from string import Template
from utils.mydecorators import _error_decorator
import utils.file_utils as file_utils
from datetime import datetime, timedelta
import inspect


class Dojs:

        def __init__(self, trace, log, jsprms, driver, humanize, urls):
                self.trace = trace
                self.log = log
                self.jsprms = jsprms                
                self.driver = driver
                self.humanize = humanize
                self.urls = urls
                self.root_app = os.getcwd()
        
        @_error_decorator()
        def get_events(self):        
                self.trace(inspect.stack())
                url = Template(self.urls.get_url('events')).substitute(api=self.urls.get_url('api'), id=str(self.jsprms.prms['my_id']))                           
                token_key = self.jsprms.prms['token_key']
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}events.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(url=url, tokenkey=token_key)
                # print (scrpt)
                res = self.driver.execute_script(scrpt)
                file_utils.str_to_textfile("resultevents.json", json.dumps(res))
                return res
                
        @_error_decorator()
        def get_sessions(self):
                self.trace(inspect.stack())                                                   
                date_filter = f'{(datetime.now()- timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%S")}Z'
                url = Template(self.urls.get_url('sessions')).substitute(api=self.urls.get_url('api'), id=str(self.jsprms.prms['my_id']), dateafter=date_filter)                  
                # {"date":"2022-09-27T15:44:00"},
                # print(url)
                #url = url.replace('[date]',date_filter)                              
                token_key = self.jsprms.prms['token_key']
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}sessions.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(url=url, tokenkey=token_key)
                # print (scrpt)
                # input("wait 4 key")
                res = self.driver.execute_script(scrpt)
                file_utils.str_to_textfile("resultsessions.json", json.dumps(res))
                return res
                        
        @_error_decorator()
        def get_mentorings(self, id_mentoring):    
                self.trace(inspect.stack())              
                url = Template(self.urls.get_url('mentorings')).substitute(api=self.urls.get_url('api'), id_mentoring=id_mentoring)                
                token_key = self.jsprms.prms['token_key']
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}mentorings.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(url=url, tokenkey=token_key)
                # print (scrpt)
                res = self.driver.execute_script(scrpt)
                file_utils.str_to_textfile("resultmentorings.json", json.dumps(res))
                return res
        
                
        @_error_decorator()
        def login(self, login, password):
                self.trace(inspect.stack())
                urlbase = Template(self.urls.get_url('login')).substitute(base=self.urls.get_url('base'))
                self.driver.get(urlbase)
                url = Template(self.urls.get_url('login_check')).substitute(base=self.urls.get_url('base'))
                
                self.humanize.wait_human(5, 2)
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}login.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(login=login, password=password, url=url, urlbase=urlbase,
                                                sec_ch_ua=self.jsprms.prms['sec_ch_ua'].replace('#','\\"'))
                # print (scrpt)
                res = self.driver.execute_script(scrpt)
                # print (f"Resultat = {res}")