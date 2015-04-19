﻿#输入参数，获取各个url组合起来的结果并排序输出
#需要选择不同个数结果，比如可以定义秒杀价 amz_cn的输出不了？
#amzjp 编码错增加encode  gbk ignore参数  

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


amz_com = ['http://www.amazon.com/s/url=search-alias%3Daps&field-keywords=',
             ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
            '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span',
            '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/span[2]' ]  ] 

z_cn  = [ 'http://www.amazon.cn/s/url=search-alias%3Daps&field-keywords=',
          ['//*[@id="result_0"]/div/div/div[1]/a/h2' ,
          '//*[@id="result_0"]/div/div[3]/div[1]/a/span',
          '//*[@id="result_0"]/div/div[3]/div[2]/a/span']  ]

yifan = ['http://www.yifanshop.com/search.php?keywords=',
          ['//*[@id="compareForm"]/div/ul/li/div/a',
          '//*[@id="compareForm"]/div/ul/li/div/font']          ]
          
amz_uk = ['http://www.amazon.co.uk/s/url=search-alias%3Daps&field-keywords=',
           ['//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span',
           '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/span[2]'] ]
                     
amz_fr = ['http://www.amazon.fr/s/url=search-alias%3Daps&field-keywords=',
          ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span']]
          
amz_jp = [ 'http://www.amazon.co.jp/s/url=search-alias%3Daps&field-keywords=',
          ['//*[@id="result_0"]/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div[3]/div[1]/a/span']]

amz_de = [ 'http://www.amazon.de/s/url=search-alias%3Daps&field-keywords=',
          ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
          '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span']]
          
                    
site_list = [ z_cn, amz_com, yifan ,   amz_de, amz_fr, amz_jp, amz_uk]
site_list_simple = [ z_cn,    yifan ,    amz_jp]
 

 

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
 

def mt_get_html_and_parser(url_dict, xpath_list):    
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
       for xpath in xpath_list[idx] :
       	 r =  tree.xpath(xpath)
       	 if ( len(r) == 0):
       	 	 #print ("Empty result  extract from the url = %s, xpath   = %s\n " % (url, xpath ))    	 	 
       	 	 result_list.append("extract failed or not found!")
       	 	 break
       	 elif len(r) > 1 :
       	 	 print ("The number of results extract from the url = %s is %s ,, xpath = %s\n" % (url, len(r), xpath))
       	 
       	 item =  r[0].text.strip()   

       	 result_list.append(item)
       if (len(result_list))  > 1 :#+ len(xpath_list[idx]) : #complete extract
          all_result_list.append(result_list)
    return   all_result_list
    	
def output ( 	all_result_list ):
	#all_result_list.sort(key = lambda x:x[2])

	for result_list in all_result_list:
 	   print(" %s " % (result_list[0]))
 	   for i in  range(1,len(result_list)) : 	   	   
		    print(" %-20s \t" % (str(result_list[i].encode("GBK", 'ignore'))) )#encode 问题		    
		    #print(" %-20s \t" % ( result_list[i] ) )
 	   print("\n")		          
    
	
def search_output	(keywords_list) :
  for keywords in keywords_list :
      print("start search keywords %s" % keywords)
      url_dict = {}
      idx = 0
      xpath_list = []		
      for site in site_list :
         url =  ( site[0] + keywords )		  
         url_dict[url] = idx
         xpath_list.append(site[1])		  
         idx = idx + 1
      all_result_list = mt_get_html_and_parser(url_dict, xpath_list)
      output(all_result_list)
	
   

if __name__ == '__main__':
	#reload(sys)
	#sys.setdefaultencoding('utf-8')
	keywords_list = getInput()
	search_output(keywords_list)
	 
	