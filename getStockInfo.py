#输入参数，获取某个商品的价格，库存并输出
#存储和比较，输出 ？

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
func.TIME_OUT = 5
func.RUN_MODE = 3

#url需要增加如 B00NHQGE04 商品id
amz_item  = [ 'http://www.amazon.com/Disney-Princess-Elsas-Sparkling-Castle/dp/',
              ['//*[@id="productTitle"]', 
              '//*[@id="priceblock_ourprice"]',
              '//*[@id="availability"]/span',
              
              '//*[@id="merchant-info"]',
              '//*[@id="merchant-info"]/a'] ]
           
 
 
#site = [page_url, [xpath list ]]
amz_com_bs = ['http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Building-Sets/zgbs/toys-and-games/166099011/ref=zg_bs_166099011_pg_1?_encoding=UTF8&pg=',
             [ '//*[@id="zg_centerListWrapper"]/div/div/div/a'
               '//*[@id="zg_centerListWrapper"]/div/div/div/div/strong'
               '//*[@id="zg_centerListWrapper"]/div/div/div/div/span' ]  ] 

 
amz_com_wishlist = ['http://www.amazon.com/gp/registry/wishlist/HNB27BLU3KRN/ie=UTF8&page=',
             [ '//*[@id="itemInfo_I38IFR4H2DG3WY"]/div/div[1]/div[1]/h5/a'
               '//*[@id="itemPrice_I38IFR4H2DG3WY"]'
               '//*[@id="zg_centerListWrapper"]/div/div/div/div/span' ]  ] 


#玩具z秒杀
z_cn_goldbox  = [ 'http://www.amazon.cn/gp/goldbox/ref=nav_cs_top_nav_gb27?gb_hero_f_102=p:1,c:647070051,s:available',
          ['//*[@id="result_0"]/div/div/div[1]/a/h2' ,
          '//*[@id="result_0"]/div/div[3]/div[1]/a/span',
          '//*[@id="result_0"]/div/div[3]/div[2]/a/span']  ]
 

 
          
                    
site_list = [ amz_item]
 

 

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
       #html = html.encode('UTF-8')
       tree = etree.HTML(html)
       idx = url_dict[url]
       result_list = []
       result_list.append(url)
       for xpath in xpath_list[idx] :
       	 r =  tree.xpath(xpath)
       	 if ( len(r) == 0):
       	 	 #print ("Empty result  extract from the url = %s, xpath   = %s\n " % (url, xpath ))    	 	 
       	 	 result_list.append("extract failed or not found!")
       	 	 continue
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
 	   
	
def search_output	(keywords_list ) :
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
	#keywords_list = getInput() 
	keywords_list = ['B00NHQGE04', 'B00GSN5H7E', 'B0063PKOL6', 'b00gsn5h2o','B00PE12ZJO',
	                'B00C9X58IU', 'B004P2HMNM', 'B003Q6BQOY','B00BFXP3G2', 'B00NHQGDZ0',
	                'B00NHQGGTI']
	search_output(keywords_list )
	 
	
