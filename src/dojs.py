import os
import json
from string import Template
from utils.mydecorators import _error_decorator, _trace_decorator
import utils.file_utils as file_utils
from datetime import datetime, timedelta
        
from utils.urls import get_url
class Dojs:

        def __init__(self, trace, log, jsprms, driver, humanize):
                self.trace = trace
                self.log = log
                self.jsprms = jsprms                
                self.driver = driver
                self.humanize = humanize
                self.root_app = os.getcwd()

        @_trace_decorator    
        @_error_decorator()
        def get_events(self):                              
                url_api = get_url(self.jsprms.prms['urls'],"api")
                url_events = get_url(self.jsprms.prms['urls'],"events")                                
                url = url_events.replace('[api]',url_api).replace('[id]', str(self.jsprms.prms['my_id']))                                
                token_key = self.jsprms.prms['token_key']
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}events.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(url=url, tokenkey=token_key)
                # print (scrpt)
                res = self.driver.execute_script(scrpt)
                file_utils.str_to_textfile("resultevents.json", json.dumps(res))
                return res
        
        @_trace_decorator    
        @_error_decorator()
        def get_sessions(self):                              
                url_api = get_url(self.jsprms.prms['urls'],"api")
                url_events = get_url(self.jsprms.prms['urls'],"sessions")                                
                url = url_events.replace('[api]',url_api).replace('[id]', str(self.jsprms.prms['my_id']))  
                # {"date":"2022-09-27T15:44:00"},
                date_filter = (datetime.now()- timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%S")
                url = url.replace('[date]',date_filter)                              
                token_key = self.jsprms.prms['token_key']
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}sessions.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(url=url, tokenkey=token_key)
                # print (scrpt)
                input("wait 4 key")
                res = self.driver.execute_script(scrpt)
                file_utils.str_to_textfile("resultsessions.json", json.dumps(res))
                return res
                
        @_trace_decorator    
        @_error_decorator()
        def get_mentorings(self, id_mentoring):                              
                url_api = get_url(self.jsprms.prms['urls'],"api")
                url_events = get_url(self.jsprms.prms['urls'],"mentorings")                                                
                url = url_events.replace('[api]',url_api).replace('[id]', str(self.jsprms.prms['my_id']))                                
                url = url.replace('[id_mentoring]',id_mentoring)
                token_key = self.jsprms.prms['token_key']
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}mentorings.js"
                with open(jsfile, 'r') as f:
                        ctc = Template(f.read())
                        scrpt = ctc.substitute(url=url, tokenkey=token_key)
                # print (scrpt)
                res = self.driver.execute_script(scrpt)
                file_utils.str_to_textfile("resultmentorings.json", json.dumps(res))
                return res
        
     