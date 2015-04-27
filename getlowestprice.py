#输入参数，获取各个url组合起来的结果并排序输出
#需要选择不同个数结果，比如可以定义秒杀价 amz_cn的输出不了？
#amzjp 编码错增加encode  gbk ignore参数  
#增加访问item的库存信息？
#价格汇率转换，日元还有问题 怀疑和rmb ￥ utf8后一样了，所以改在site里增加一个rate
import codecs
 
import sys, time, Queue, urllib
from lxml import etree

sys.path.append("../mymodule")
import func
import mt
func.USE_PROXY = False
func.SHOW_LOG = False
mt.MAX_THREADS_NUM = 10 #线程池大小
func.MAX_TRY_TIMES  = 3
func.TIME_OUT = 4
func.RUN_MODE = 3

currency_RMB = 1
currency_EUR = 6.7
currency_USD = 6.3
currency_JPN = 0.052
currency_GBR = 9.3


 
#search 结果
amz_com = ['http://www.amazon.com/s/url=search-alias%3Daps&field-keywords=',
              currency_USD,    #货币换算rmb   
             ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
            '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span',
            '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/span[2]' ,
             '//*[@id="result_0"]/div/div[2]/div/a']  ] 
 
 
 

 
z_cn  = [ 'http://www.amazon.cn/s/url=search-alias%3Daps&field-keywords=',
             currency_RMB,
          ['//*[@id="result_0"]/div/div[2]/div[1]/a/h2' ,
          '//*[@id="result_0"]/div/div[3]/div[1]/a/span',
          '//*[@id="result_0"]/div/div[3]/div[2]/a/span']  ]

yifan = ['http://www.yifanshop.com/search.php?keywords=',
           currency_RMB,   
          ['//*[@id="compareForm"]/div/ul/li/div/a',
          '//*[@id="compareForm"]/div/ul/li/div/font']          ]
          
amz_uk = ['http://www.amazon.co.uk/s/url=search-alias%3Daps&field-keywords=',
            currency_GBR, 
           ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
           '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span',
           '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/span[2]'] ]
                     
amz_fr = ['http://www.amazon.fr/s/url=search-alias%3Daps&field-keywords=',
           currency_EUR,
          ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span']]
          
amz_jp = [ 'http://www.amazon.co.jp/s/url=search-alias%3Daps&field-keywords=',
          currency_JPN,
          ['//*[@id="result_0"]/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div[3]/div[1]/a/span']]

amz_de = [ 'http://www.amazon.de/s/url=search-alias%3Daps&field-keywords=',
           currency_EUR,
          ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span']]

amz_it = [ 'http://www.amazon.it/s/url=search-alias%3Daps&field-keywords=',
           currency_EUR, 
          ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span']]
          
                    
                    
site_list = [ z_cn, amz_com, yifan ,   amz_de, amz_fr, amz_jp, amz_uk, amz_it]
#site_list = [ amz_jp]


  

currency_dict= {'$':6.2, 'EUR':6.7, '￥':0.052, '£':9.3}


def judge_currency(str_price):	
		for c in currency_dict.keys() :
		  u_c = c.decode("utf8")
		  if u_c in str_price :
		  	 print(" c in str_price. %s %s "%(u_c, str_price))
		  	 return c
		return None
		
def _change_currency(str_price, c):
		  	 #if currency_dict.get(c) is None:         	  
		  	 #   return  str_price
		  	 u_c = c.decode("utf8")
		  	 str_price = str_price[len(u_c):].strip()
		  	 str_price = filter(lambda ch: ch in '0123456789,.~', str_price)		  	 
		  	 if c == "EUR"	:
		  	    str_price = str_price.replace(',','.')
		  	 elif c == '￥' :
		  	 	  str_price = str_price.replace(',','')  
		  	  
		  	 #print str_price
		  	 currency = float(str_price) * currency_dict[c]
		  	 #print str(currency)
		  	 return str(currency)
	 
def change_currency(str_price, c_rate):  
         if "EUR" in str_price:
	       	  str_price = str_price.replace(',','.') 
         str_price = filter(lambda ch: ch in '0123456789.', str_price)		  	 
         #print str_price
         currency = float(str_price) * c_rate
         #print str(currency)
         return str(currency)  
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
  
	print(" I will search %s keywords in %s sites " %(len(keywords_list), len(site_list)) )  
	return keywords_list


def get_html_func(_url):
    resp = func.GetHttpContent ( _url )           
    if resp is None :
      func._print ("failed to get html .The url = %s \n"%(_url ))                  
    return resp
 

def mt_get_html_and_parser(url_dict, xpath_list, currency_list):    
    page_result_queue = Queue.Queue() 
    mt_create_queue_flag = False
    url_list = url_dict.keys()
    mt.runMT("x", get_html_func, url_list, mt_create_queue_flag, page_result_queue)
    #for every url , 
    all_result_list = []     # other page    
    while (not page_result_queue.empty()):
       url , html  =   page_result_queue.get()
       #html = html.decode('UTF-8', 'replace') # for show in gbk in windows cmd shell
       tree = etree.HTML(html)
       idx = url_dict[url]
       result_list = []
       result_list.append(url)
       cur_rate = currency_list[idx]
       for i in range(len(xpath_list[idx])) :
       	 xpath = xpath_list[idx][i] 
       	 r_list =  tree.xpath(xpath)
       	 if ( len(r_list) == 0):
       	 	 print (" %s \n extract 0 result \n xpath   = %s\n " % (url, xpath ))    	  
       	 	 #result_list.append("extract failed or not found!")
       	 	 continue
       	 elif len(r_list) > 1 :
       	 	 print ("The number of results extract from the url = %s is %s   xpath = %s\n" % (url, len(r_list), xpath))
         for r in r_list:
       	   item =  r.text.strip()   
       	   #xpath 的第2开始都是价格要换算
       	   result_list.append(item)
       	   if i > 0 :
       	   	 item = "RMB " + change_currency(item, cur_rate)
       	   	 result_list.append(item)
       	   #c = judge_currency(item)
       	   #if c is not None :
       	   #   item = item + " = RMB " + _change_currency(item, c) 	         	        
       if (len(result_list))  > 1 :#+ len(xpath_list[idx]) : #complete extract
          all_result_list.append(result_list)
    return   all_result_list
    	
def output ( 	all_result_list ):
	#change to float for compare  . 4: is to del RMB
	try:
	   all_result_list.sort(key = lambda x:float(x[3][4:])) 
	except Exception , e:
	   print( "failed on all_result_list  sort.  Exception %s "%(e))

	for result_list in all_result_list:
 	   print(" %s " % (result_list[0]))
 	   for i in  range(1,len(result_list)) : 	   	   
 	   	  try:
		        print(" %-20s \t" % (str(result_list[i].encode("GBK", 'ignore')))) #encode		    
 	   	  except Exception , e:
		        print( " Exception ! encode  %s "%(result_list[i]))
		    	
		    #print(" %-20s \t" % ( result_list[i] ) )
 	   print("\n")		          
    
	
def search_output	(keywords_list) :
  for keywords in keywords_list :
      print("start search keywords %s" % keywords)
      url_dict = {}
      idx = 0
      xpath_list = []		
      currency_list = []
      for site in site_list : # every site
         url =  ( site[0] + keywords )		  
         url_dict[url] = idx
         currency_list.append(site[1])
         xpath_list.append(site[2])		  
         idx = idx + 1
      all_result_list = mt_get_html_and_parser(url_dict, xpath_list,currency_list)
      output(all_result_list)
	
   

if __name__ == '__main__':
	#reload(sys)
	#sys.setdefaultencoding('utf-8')
	keywords_list = getInput()
	search_output(keywords_list)
	 
	
