 
import urllib2
import codecs
import sys, time
from lxml import etree
sys.path.append("../mymodule")
import mt,func	

func.USE_PROXY = False
func.DEFAULT_PROXY_SERVER  =   "10.94.235.26:8080"
func.SHOW_LOG = True
func.RUN_MODE = 3


file_name = "amz.htm"
 
  
#amz_bestseller_page
amz_bestseller_page1_url = "http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Building-Sets/zgbs/toys-and-games/166099011/ref=zg_bs_166099011_pg_1?_encoding=UTF8&pg=1"
amz_bestseller_page2_url = "http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Building-Sets/zgbs/toys-and-games/166099011/ref=zg_bs_166099011_pg_2?_encoding=UTF8&pg=2"

amz_bs_url_list = [amz_bestseller_page1_url, amz_bestseller_page2_url]
xpath_ab_goods = '//*[@id="zg_centerListWrapper"]/div/div/div/a'
xpath_ab_price = '//*[@id="zg_centerListWrapper"]/div/div/div/div/strong'
xpath_list_price = '//*[@id="zg_centerListWrapper"]/div/div/div/div/span'
xpath_list = [ xpath_ab_goods, xpath_ab_price,  xpath_list_price]



amz_com_url_list  = ['http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=lego 10220']
amz_com_xpath_list =        [ '//*[@id="result_0"]/div/div/div/div/div/a/h2',
            '//*[@id="result_0"]/div/div/div/div/div/div/div/a/span']

z_cn_url_list  = [ 'http://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=10220']
z_cn_xpath_list = ['//*[@id="result_0"]/div/div/div[1]/a/h2' ,
          '//*[@id="result_0"]/div/div/div[1]/a/span']
          
yifan_url_list  = [ 'http://www.yifanshop.com/search.php?keywords=10220']
yifan_xpath_list = [       '//*[@id="compareForm"]/div/ul/li/div/a',
          '//*[@id="compareForm"]/div/ul/li/div/font']







def extract(the_url,   _xpath_list):
    html = ''    
    try:
    	  html = func.GetHttpContent(the_url)
    	  #f = open(file_name, 'w')
    	  #f.write(html)
    	  #f.close
    	  #html = open(file_name).read()#.decode(decoding)  
    	  #print html
    except:
        pass
    
    if html is None:
    	return
    tree = etree.HTML(html)

    item1 = tree.xpath(_xpath_list[0])
    item2 =  tree.xpath(_xpath_list[1])
    #item3 =  tree.xpath(xpath_list[2])
 
    items_dict = dict(zip(item1, item2))
    
    item_no = 0
    print ( the_url )
    for goods_name ,   price in items_dict.iteritems():
    	item_no = item_no +1
     	print "%-3s %-30s \t %s" % ( item_no, goods_name.text, price.text)  
    	   
    
    

if __name__ == '__main__':
  
 
  for url in z_cn_url_list :
    extract(url, z_cn_xpath_list)
    
     
