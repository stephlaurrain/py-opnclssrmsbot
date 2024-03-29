# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime, timedelta
from time import sleep
import inspect

from warnings import catch_warnings
# mes libs
import utils.mylog as mylog
import utils.str_utils as str_utils
import utils.file_utils as file_utils
from utils.mydecorators import _error_decorator
import utils.jsonprms as jsonprms
from utils.humanize import Humanize
from dojs import Dojs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from string import Template
from selenium.webdriver.common.keys import Keys
from utils.urls import Urls

class Bot:
      
        #def __init__(self):                
                

        def trace(self,tracestk):
                #print ("{0} ({1}-{2})".format(stck.function, stck.filename, stck.lineno))                
                self.log.lg(f"{tracestk[0].function}")
                #res=''
                #for trace in tracestk:
                #        res += f"{trace.function} - "
                #        self.log.lg(f"{res}")
        
        def newtab(self,url):            
                self.driver.execute_script("window.open('{0}');".format(url))
                self.driver.switch_to.window(self.driver.window_handles[-1]) 

        
        @_error_decorator()
        def getsession_by_id(self, id_session, sessions):
                self.trace(inspect.stack())
                for session in sessions:
                        # print(f"#{id_session}# / #{session['id']}#")
                        if str(session['id']) == id_session:
                                return session
        
        @_error_decorator()
        def getsessions(self):    
                self.trace(inspect.stack())                            
                url_dashboard = Template(self.urls.get_url('dashboard')).substitute(base=self.urls.get_url('base'))
                self.driver.get(url_dashboard)
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, 'scheduled')))      
                limit = self.jsprms.prms['mentoring_nb']
                offset_hour = self.jsprms.prms['offset_hour']
                date_filter = (datetime.now()- timedelta(hours=offset_hour)).strftime("%Y-%m-%dT%H:%M:%S")
                # print(date_filter)
                events = self.dojs.get_events()
                # print(events)                
                def sort_by_key(list):
                        return list['startDate']
                events=sorted(events,key=sort_by_key, reverse=False)  
                tpl_report = f"{self.root_app}{os.path.sep}data{os.path.sep}tpl{os.path.sep}report.tpl"     
                tpl_message = f"{self.root_app}{os.path.sep}data{os.path.sep}tpl{os.path.sep}message.tpl"       
                cpt = 0
                resrep =''
                for event in events:                        
                        truedate = datetime.strptime(event['startDate'].replace('+0000',''),"%Y-%m-%dT%H:%M:%S")
                        truedate = truedate + timedelta(hours=offset_hour)
                        truedate_as_str = truedate.strftime("%d-%m-%Y à %H:%Mh")
                        if datetime.now() <= truedate:
                                full_session_id = event['id'].rsplit('-', 1)
                                session_type = full_session_id[0]
                                id_session = full_session_id[1]
                                print(session_type)
                                #print(id_session) # print(event['type']) # print(event['startDate']) # print(truedate)
                                student = event['attendees'][0]                        
                                print(student['displayName']) 
                                print(student['email'])
                                print(student['firstName']) 
                                print(student['lastName'])                                                        
                                sessions = self.dojs.get_sessions()
                                session = self.getsession_by_id(id_session, sessions)
                                
                                # print(session['videoConference']['id'] ) 
                                visio_id = session['videoConference']['id']                           
                                visio_url = Template(self.urls.get_url('meet')).substitute(base=self.urls.get_url('base'),id=visio_id)                                
                                with open(tpl_report, 'r') as f:                                                                        
                                        reptmpl = Template(f.read())
                                        with open(tpl_message, 'r') as f:                                                                        
                                                messtmpl = Template(f.read())
                                                resmess = messtmpl.substitute(student, event_type=event['type'], visio_url=visio_url, truedate=truedate_as_str)
                                                # print(resmess)
                                        resrep += reptmpl.substitute(message=resmess)

                                if cpt == limit:
                                         break;
                                cpt +=1
                        res_file = f"{self.root_app}{os.path.sep}data{os.path.sep}results.txt"
                        with open(res_file, "w") as text_file:
                                text_file.write(resrep)
                ## self.driver.execute_script(f"window.open('file:{res_file}','_blank');");
                ## self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') 
                self.driver.get(f'file:{res_file}')
                # You can use (Keys.CONTROL + 't') on other OSs


        @_error_decorator()        
        def login(self, login, password):
                self.trace(inspect.stack())
                url = Template(self.urls.get_url('login')).substitute(base=self.urls.get_url('base'))
                self.driver.get(url)                        
                self.waithuman(2,5)                                          
                # accepter cookies
                #body > div:nth-child(16) > div.mainContent > div > div.pdynamicbutton > a.call
                        
                element = self.driver.find_element(By.ID, 'fielduserEmail')
                element.send_keys (login)
                element = self.driver.find_element(By.ID, "continue-button")
                print("ici")
                element.click(); 
                print("avant field")
                element = self.driver.find_element(By.ID, 'field_password')
                print("send_keys")
                element.send_keys (password)

        # init        
        @_error_decorator(do_raise=True)
        def init(self):    
                self.trace(inspect.stack())                      
                options = webdriver.ChromeOptions()
                if (self.jsprms.prms['headless']):
                        options.add_argument("--headless")
                #else:
                options.add_argument("user-data-dir=./chromeprofile")
                # anti bot detection
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                # pi / docker
                if (self.jsprms.prms['box']):
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--disable-gpu")
                        prefs = {"profile.managed_default_content_settings.images": 2}
                        options.add_experimental_option("prefs", prefs)                
                options.add_argument("--start-maximized")
                # driver = webdriver.Chrome(executable_path=self.chromedriver_bin_path, options=options)
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)        
                # anti bot detection                
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                # resout le unreachable
                driver.set_window_size(1900, 1080)
                driver.implicitly_wait(self.jsprms.prms['implicitly_wait'])
                return driver
        
        
        @_error_decorator()
        def remove_logs(self):
                self.trace(inspect.stack())
                keep_log_time = self.jsprms.prms['keep_log_time']
                keep_log_unit = self.jsprms.prms['keep_log_unit']
                self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
                file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)                        
                
        def initmain(self, jsonfile):              
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)                     
                        self.trace(inspect.stack())                        
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)
                                        
                        self.test = self.jsprms.prms['test']
                        self.remove_logs()
                        self.log.lg("=Here I am=")                
                        self.driver = self.init()                              
                except Exception as e:
                        self.log.errlg(f"Wasted ! : {e}")
                        raise                         

        
        @_error_decorator(do_raise=True)
        def testpath(self):
                self.trace(inspect.stack())
                url = Template(self.urls.get_url('dashboard')).substitute(base=self.urls.get_url('base')) 
                self.driver.get(url)
                mypath=input("Enter xpath : ")
                while mypath !="":
                        try:
                                #mypath='//section[@id="scheduled"]/section/ol/li/a/div[4]/a'
                                elements =self.driver.find_elements(By.XPATH,mypath)
                                print(f"hopla {str(elements[0])}")
                                href=elements[0].get_attribute('href')
                                print(f'href={href}')
                        except Exception as e:
                                print(e)  
                        mypath=input("Enter xpath : ")

        def main(self, command="",jsonfile="", param2="", param3=""):
                try:
                        # InitBot
                        # args
                        if command == "":
                                nb_args = len(sys.argv)
                                command = "test" if (nb_args == 1) else sys.argv[1]
                                # fichier json en param
                                jsonfile = "default" if (nb_args < 3) else sys.argv[2].lower()                                
                                param1 = "default" if (nb_args < 4) else sys.argv[3].lower()
                                param2 = "default" if (nb_args < 5) else sys.argv[4].lower()
                                param3 = "default" if (nb_args < 6) else sys.argv[5].lower()      
                                print("params=", command, jsonfile, param1, param2)
                        # logs
                        print(command)  
                        # self.initmain(jsonfile)
                        self.humanize = Humanize(self.trace, self.log, self.jsprms.prms['offset_wait'], self.jsprms.prms['wait'], self.jsprms.prms['default_wait'])
                        self.urls = Urls(self.jsprms.prms['urls'])                        
                        self.dojs = Dojs(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.urls)

                       
                        #Test
                        # command="getsessions"                
                        if (command=="simplyconnect"):   
                                url = Template(self.urls.get_url('dashboard')).substitute(base=self.urls.get_url('base'))   
                                # print(url)
                                self.driver.get(url)
                        if (command=="getsessions"):
                                try :
                                        self.getsessions()
                                except:
                                        pass
                                        # self.driver.close()
                        if (command=="login"):   
                                # self.login(self.jsprms.prms['login'],self.jsprms.prms['password'])  
                                self.dojs.login(self.jsprms.prms['login'],self.jsprms.prms['password'])  
                        if (command=="dash"):
                                url = Template(self.urls.get_url('dashboard')).substitute(base=self.urls.get_url('base'))
                                self.driver.get(url)
                        if (command=="booked"):          
                                url = Template(self.urls.get_url('dashboard')).substitute(base=self.urls.get_url('base'))  
                                self.driver.get(url)
                        if (command=="testpath"):
                                self.testpath()                    
                        input("wait 4 key")
                        # planifiées
                        # https://openclassrooms.com/fr/mentorship/dashboard/booked-mentorship-sessions
                        # à compléter
                        # https://openclassrooms.com/fr/mentorship/dashboard/sessions
                        ##)  

                        #ONGLETS
                        #driver.switch_to.window(driver.window_handles[-1])       

                except KeyboardInterrupt:
                        print("==>> Interrupted <<==")
                        
                        pass
                except Exception as e:
                        print("==>> GLOBAL MAIN EXCEPTION <<==")
                        self.log.errlg(e)                       
                        return False
                finally:
                        # self.driver.close()
                        print("==>> DONE <<==")
