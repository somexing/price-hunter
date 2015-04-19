#输入参数，获取各个非查询网站得来的结果并输出
#存储和比较，输出

import codecs
 
import sys, time, Queue, urllib
from lxml import etree

sys.path.append("../mymodule")
import func
import mt
func.USE_PROXY = False
func.SHOW_LOG = True
mt.MAX_THREADS_NUM = 10 #线程池大小
func.MAX_TRY_TIMES  = 3
func.TIME_OUT = 5
func.RUN_MODE = 3

 
#site = [page_url, [xpath list ]]
amz_com_bs = ['http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Building-Sets/zgbs/toys-and-games/166099011/ref=zg_bs_166099011_pg_1?_encoding=UTF8&pg=',
             [ '//*[@id="zg_centerListWrapper"]/div/div/div/a'
               '//*[@id="zg_centerListWrapper"]/div/div/div/div/strong'
               '//*[@id="zg_centerListWrapper"]/div/div/div/div/span' ]  ] 

 
amz_com_wishlist = ['http://www.amazon.com/gp/registry/wishlist/HNB27BLU3KRN/ie=UTF8&page=',
             [ '//*[@id="itemInfo_I38IFR4H2DG3WY"]/div/div[1]/div[1]/h5/a'
               '//*[@id="itemPrice_I38IFR4H2DG3WY"]'
               '//*[@id="zg_centerListWrapper"]/div/div/div/div/span' ]  ] 



z_cn_goldbox  = [ ' ',
          ['//*[@id="result_0"]/div/div/div[1]/a/h2' ,
          '//*[@id="result_0"]/div/div[3]/div[1]/a/span',
          '//*[@id="result_0"]/div/div[3]/div[2]/a/span']  ]
 


smzdm_fx_lego = ['http://search.smzdm.com/?c=faxian&s=lego',
          ['/html/body/section/ul[2]/li[1]/div[2]/h2/a/span[1]',
          '/html/body/section/ul[2]/li[1]/div[2]/h2/a/span[2]'],   
          ['/html/body/section/ul[2]/li[2]/div[2]/h2/a/span[1]',
          '/html/body/section/ul[2]/li[2]/div[2]/h2/a/span[2]']]
          
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
          
                    
site_list = [ smzdm_fx_lego]
 

 

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
		    print(" %-20s \t" % (result_list[i]))
 	   print("\n")		          
    
	
def search_output	( ) :
 
      
      url_dict = {}
      idx = 0
      xpath_list = []		
      for site in site_list :
         url =  ( site[0]   )		  
         url_dict[url] = idx
         xpath_list.append(site[1])		  
         idx = idx + 1
      all_result_list = mt_get_html_and_parser(url_dict, xpath_list)
      output(all_result_list)
	
   

if __name__ == '__main__':
	#keywords_list = getInput()
	search_output( )
	 
	
