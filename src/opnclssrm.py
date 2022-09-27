# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep

from warnings import catch_warnings
# mes libs
import utils.mylog as mylog
import utils.str_utils as str_utils
import utils.file_utils as file_utils
from utils.mydecorators import _error_decorator, _trace_decorator
import utils.jsonprms as jsonprms
from utils.humanize import Humanize

import inspect
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from string import Template
from selenium.webdriver.common.keys import Keys

from dojs import Dojs
from utils.humanize import Humanize

class Bot:
      
        #def __init__(self):                
                

        def trace(self,stck):
                #print ("{0} ({1}-{2})".format(stck.function, stck.filename, stck.lineno))
                # print ("{0}".format(stck.function))
                self.log.lg("{0}".format(stck.function))
        
        def newtab(self,url):            
                self.driver.execute_script("window.open('{0}');".format(url))
                self.driver.switch_to.window(self.driver.window_handles[-1]) 

        @_trace_decorator        
        @_error_decorator()
        def getsessions(self):
                self.driver.get('https://openclassrooms.com/fr/mentorship/dashboard/booked-mentorship-sessions')
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, 'scheduled')))      
                self.dojs.get_events()                                  
                       
        

        @_trace_decorator        
        @_error_decorator()
        def login(self, login, password):
                
                self.driver.get("https://openclassrooms.com/fr/login")                        
                self.waithuman(2,5)                                          
                # accepter cookies
                #body > div:nth-child(16) > div.mainContent > div > div.pdynamicbutton > a.call
                        
                element = self.driver.find_element_by_id('fielduserEmail')
                element.send_keys (login)
                element = self.driver.find_element_by_id("continue-button")
                print("ici")
                element.click(); 
                print("avant field")
                element = self.driver.find_element_by_id('field_password')
                print("send_keys")
                element.send_keys (password)

        # init
        @_trace_decorator        
        @_error_decorator(do_raise=True)
        def init(self):                          
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
                options.add_argument(f"user-agent={self.jsprms.prms['user_agent']}")
                options.add_argument("--start-maximized")
                driver = webdriver.Chrome(executable_path=self.chromedriver_bin_path, options=options)
                # anti bot detection                
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                # resout le unreachable
                driver.set_window_size(1900, 1080)
                driver.implicitly_wait(self.jsprms.prms['implicitly_wait'])
                return driver
        
        @_trace_decorator        
        @_error_decorator()
        def remove_logs(self):
                keep_log_time = self.jsprms.prms['keep_log_time']
                keep_log_unit = self.jsprms.prms['keep_log_unit']
                self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
                file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)                        
                
        def initmain(self, jsonfile):              
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)                     
                        self.trace(inspect.stack()[0])                        
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)
                        self.chromedriver_bin_path = self.jsprms.prms['chromedriver']
                        self.test = self.jsprms.prms['test']
                        self.remove_logs()
                        self.log.lg("=Here I am=")                
                        self.driver = self.init()                              
                except Exception as e:
                        self.log.errlg(f"Wasted ! : {e}")
                        raise                         

        @_trace_decorator        
        @_error_decorator(do_raise=True)
        def testpath(self):
                self.driver.get('https://openclassrooms.com/fr/mentorship/dashboard/booked-mentorship-sessions')
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


        @_trace_decorator        
        @_error_decorator(do_raise=True)
        def template(self, login, password):               
                pass                                                         
        

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
                        self.initmain(jsonfile)

                        self.humanize = Humanize(self.trace, self.log, self.jsprms.prms['offset_wait'], self.jsprms.prms['wait'], self.jsprms.prms['default_wait'])
                        self.dojs = Dojs(self.trace, self.log, self.jsprms, self.driver, self.humanize)
                        #Test
                        # command="getsessions"                
                                
                        if (command=="simplyconnect"):   
                                self.driver.get('https://openclassrooms.com/fr/mentorship/dashboard/booked-mentorship-sessions')                        
                        if (command=="getsessions"):
                                self.getsessions()
                        if (command=="login"):   
                                self.login(self.jsprms.prms['login'],self.jsprms.prms['password'])  
                        
                        if (command=="dash"):          
                                self.driver.get('https://openclassrooms.com/fr/mentorship/dashboard/sessions')
                        if (command=="booked"):          
                                self.driver.get('https://openclassrooms.com/fr/mentorship/dashboard/booked-mentorship-sessions')
                 
                        if (command=="testpath"):
                                self.testpath()
                        input("wait 4 key")
                        # planifiées
                        # https://openclassrooms.com/fr/mentorship/dashboard/booked-mentorship-sessions
                        # à compléter
                        # https://openclassrooms.com/fr/mentorship/dashboard/sessions


                        #self.openmyadmin()    
                        #self.openbo()                 
                        
                        
                        ##)  

                        #ONGLETS
                        #driver.switch_to.window(driver.window_handles[-1])       

                except KeyboardInterrupt:
                        print("==>> Interrupted <<==")
                        self.driver.close()
                        pass
                except Exception as e:
                        print("==>> GLOBAL MAIN EXCEPTION <<==")
                        self.log.errlg(e)                       
                        return False
                finally:
                        self.driver.close()
                        print("==>> DONE <<==")


              
               
    

        
                

        

