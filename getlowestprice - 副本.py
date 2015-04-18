﻿#输入参数，获取各个url组合起来的结果并排序输出
#输出结果有多个的话如何办？
import codecs
 
import sys, time, Queue
from lxml import etree

sys.path.append("../mymodule")
import func
import mt
func.USE_PROXY = False
func.SHOW_LOG = False
mt.MAX_THREADS_NUM = 3 #线程池大小
func.MAX_TRY_TIMES  = 3
func.TIME_OUT = 5
func.RUN_MODE = 3


amz_com = ['http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=',
             ['//*[@id="result_0"]/div/div/div/div[2]/div[1]/a/h2',
            '//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span']  ]

z_cn  = [ 'http://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=',
          ['//*[@id="result_0"]/div/div/div[1]/a/h2' ,
          '//*[@id="result_0"]/div/div/div[1]/a/span']  ]
          
yifan = ['http://www.yifanshop.com/search.php?keywords=',
          ['//*[@id="compareForm"]/div/ul/li/div/a',
          '//*[@id="compareForm"]/div/ul/li/div/font']   ]

site_list = [amz_com, z_cn, yifan ]
 



# 从输入得到参数
def getInput():
  if (len(sys.argv )  >  1):
  	 keywords = sys.argv[1]
  else:
  	 print(" I need a keywords! assumed one!")	
  	 keywords = '10220'   	 
  #转义	 ?
  print(" I will search %s in %s sites " %(keywords, len(site_list)) )  
  return keywords


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
       tree = etree.HTML(html)
       idx = url_dict[url]
       result_list = []
       result_list.append(url)
       for xpath in xpath_list[idx] :
       	 r =  tree.xpath(xpath)
       	 if ( len(r) == 0):
       	 	 print ("Empty result  extract from the url = %s " % (url ))    	 	 
       	 	 break
       	 elif len(r) > 1 :
       	 	 print ("The number of results extract from the url = %s is %s" % (url, len(r)))
       	 item =  r[0].text.strip()   

       	 result_list.append(item)
       if (len(result_list))  > 1 :#+ len(xpath_list[idx]) : #complete extract
          all_result_list.append(result_list)
    return   all_result_list
    	
         
    
	
def search	(keywords) :
	idx = 0
	url_dict = {}
	xpath_list = []
	for site in site_list :
		  url =  ( site[0] + keywords )		  
		  url_dict[url] = idx
		  xpath_list.append(site[1])		  
		  idx = idx + 1
	all_result_list = mt_get_html_and_parser(url_dict, xpath_list)
	return all_result_list
	
def output ( 	all_result_list ):
	all_result_list.sort(key = lambda x:x[2])

	for result_list in all_result_list:

 	   if len(result_list) == 3 :
		    print(" %s\n %s-20 \t %s " % (result_list[0], result_list[1], result_list[2]))
 	   elif len(result_list) == 2:
		    print(" %s\n %s-20 \t   " % (result_list[0], result_list[1])) 
	 
 	   print("\n")		    

if __name__ == '__main__':
	keywords = getInput()
	all_result_list = search(keywords)
	output(all_result_list)
	
