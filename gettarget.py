#判断预定义的各个商品是否满足条件 （低价，有自营）


import codecs
import sys, time, Queue, urllib
import threading
from lxml import etree
from threading import Timer  

sys.path.append("../mymodule")
import func
import mt
 
func.SHOW_LOG = False
mt.MAX_THREADS_NUM = 3 #线程池大小
func.MAX_TRY_TIMES  = 3
func.TIME_OUT = 5
func.RUN_MODE = 3



#url需要增加如 B00NHQGE04 商品id
amz_item  = [ 'http://www.amazon.com/gp/product/',
               '//*[@id="merchant-info"]', 
               'Amazon.com' ,
               '//*[@id="priceblock_ourprice"]' ]	
               
 
		  	 
		  	 
		
 
class target(object): 
	      def __init__(self, _name, _url,
	                   xpath_stock = None, have_stock_patten = None, 
	                   xpath_price = None, low_price_value = None ):
	         self.name = _name
	         self.url  = _url
	         self.xpath_stock = xpath_stock
	         self.have_stock_patten = have_stock_patten
	         self.xpath_price = xpath_price
	         self.low_price_value = float(low_price_value)
	      
	      def Is_my_url( url ):
	         if self.url == url:
	            return True
	         else:
	         	  return False
	         	  
	      def get_url(self):
	         return self.url
	         
	      def judge_have_stock(self, html ):
	         if self.xpath_stock is None :
	         	  return False
	         tree = etree.HTML( html)
	         r_list = tree.xpath(self.xpath_stock)
	         if len(r_list) == 0 :
	         	  return False
	         if len(r_list) >  1 :
	            print("extract more than 1 stock result , target name is %s"% self.name)
	         self.stock_result = r_list[0].text.strip()
	         print("%s get stock result : %s " % (self.name, self.stock_result))
	         if self.have_stock_patten in self.stock_result : 	 
	         	  print("%s has stock now !" %  (self.name))       	          	  
	         	  return True
	         else :
	         	  return False
	            
	      def judge_have_low_price(self, html ):
	         if self.xpath_price is None :
	         	  return False	      
	         tree = etree.HTML( html)
	         r_list =tree.xpath(self.xpath_price)
	         if len(r_list) == 0 :
	         	  return False
         
	         if len(r_list) >  1 :
	            print("extract more than 1 price result , target name is %s"% self.name)
	         self.price_result = r_list[0].text.strip()
	         self.price_result = filter(lambda ch: ch in '0123456789.', self.price_result)
	         #self.price_result.strip(['$',"EUR", ' '])
	         print ("%s get price result : %s " %(self.name, self.price_result))
	         if float(self.price_result) <= float(self.low_price_value) : 	         	          	  
	         	  print("%s has low price now !" %  (self.name))       	          	  
	         	  return True
	         else :
	         	  return False 
	            

class targetlist(object):
	      def __init__(self):
	         self.targetlist = []	          
	         return
	         
	      def add_target( new_target ) :        
	         self.targetlist.append( new_target )	          
	         
	      def get_targe(url):
	         for target in self.targetlist:
	         	  if target.Is_my_url(url):
	         	  	 return target
	         return None
	         
def get_html_func(_url):
    resp = func.GetHttpContent ( _url )           
    if resp is None :
      func._print ("failed to get html .The url = %s \n"%(_url ))                  
    return resp
 

def mt_get_html_and_parser(url_dict, target_list ):    
    global target_event
    target_event.clear()
    print("\nRun at %s"%(time.strftime("%Y/%m/%d %H:%M:%S")))	    
    page_result_queue = Queue.Queue() 
    mt_create_queue_flag = False
    url_list = url_dict.keys()
    mt.runMT("x", get_html_func, url_list, mt_create_queue_flag, page_result_queue)
    #for every html got       
    while (not page_result_queue.empty()):
       url , html  =   page_result_queue.get() 
      #print html
       idx = url_dict[url]
       target = target_list[idx]      
       r1 = target.judge_have_stock(html)
       r2 = target.judge_have_low_price(html)
    target_event.set()
   
       
# 从输入得到参数
def getInput():
	keywords_list = []
	argc = len(sys.argv )
	if (argc > 1):
  	 for i in  range(1, argc) :
  	   keywords = urllib.quote( sys.argv[i]) #Replace special characters in string using the %xx escape.
  	   keywords_list.append(keywords)
	else:
  	 print(" I need a keywords! assumed one!")	
  	 keywords_list = ['10220']   	 
  	
	return keywords_list    


# 从输入得到参数
def getInput():
	keywords_list = []
	argc = len(sys.argv )
	if (argc > 1):
  	 for i in  range(1, argc) :
  	   keywords = urllib.quote( sys.argv[i]) #Replace special characters in string using the %xx escape.
  	   keywords_list.append(keywords)
	else:
  	 print(" Assumed  run every 10s  !")	
  	 keywords_list = ['10']   	 
	return keywords_list            
	
if __name__ == "__main__":
   argv_list = getInput()
   timer_interval = float(argv_list[0])

   target_list = []
   target1 = target('Snap Circuits SC-300', amz_item[0]+'B0000683A4',
                    amz_item[1], amz_item[2],
                    amz_item[3], '45.4')
   target_list.append(target1)
      	  	   
 
   idx = 0
   xpath_list = []		
   url_dict = {}
   for t in target_list :
         url =  t.get_url() 
         url_dict[url] = idx         
         idx = idx + 1
         
   target_event = threading.Event()
#   t=Timer(timer_interval, mt_get_html_and_parser, (url_dict, target_list  ))  
#   t.start()          
         
   while (True):      
       result = mt_get_html_and_parser(url_dict, target_list)
       time.sleep(float(timer_interval))

'''   
   while True:  
      time.sleep(timer_interval)
      target_event.wait()
      t=Timer(timer_interval, mt_get_html_and_parser, (url_dict, target_list  ))  
      t.start()    
      print 'main running'         	  
'''	      
	         
	             
	     
	         
	         
 
 
 
 

 





    	
