#注意访问外网比较慢，time_OUT要设置合适
import urllib2
import codecs
import sys, time
from lxml import etree
sys.path.append("../mymodule")
import mt,func	

func.USE_PROXY = True 
func.DEFAULT_PROXY_SERVER  =   "10.94.235.26:8080"
func.SHOW_LOG = False
func.RUN_MODE = 2

file_name = "amz.htm"
 
  
#amz_bestseller_page
amz_bestseller_page1_url = "http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Building-Sets/zgbs/toys-and-games/166099011/ref=zg_bs_166099011_pg_1?_encoding=UTF8&pg=1"
amz_bestseller_page2_url = "http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Building-Sets/zgbs/toys-and-games/166099011/ref=zg_bs_166099011_pg_2?_encoding=UTF8&pg=2"

amz_bs_url_list = [amz_bestseller_page1_url, amz_bestseller_page2_url]
xpath_ab_goods = '//*[@id="zg_centerListWrapper"]/div/div/div/a'
xpath_ab_price = '//*[@id="zg_centerListWrapper"]/div/div/div/div/strong'
xpath_ab_list_price = '//*[@id="zg_centerListWrapper"]/div/div/div/div/span'
xpath_ab_list = [ xpath_ab_goods, xpath_ab_price,  xpath_ab_list_price]

def extract(the_url,   xpath_ab_list):
    html = ''    
    try:
    	  html = func.GetHttpContent("GET", the_url)
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

    item1 = tree.xpath(xpath_ab_list[0])
    item2 =  tree.xpath(xpath_ab_list[1])
    item3 =  tree.xpath(xpath_ab_list[2])
   
    items_dict = dict(zip(item1, item2))
    
    item_no = 0
    print ( the_url )
    for goods_name ,   price in items_dict.iteritems():
    	item_no = item_no +1
     	print "%-3s %-50s \t %s" % ( item_no, goods_name.text, price.text)  
    	   
    
    

if __name__ == '__main__':
  
  for amz_bs_url in amz_bs_url_list :
    extract(amz_bs_url, xpath_ab_list)
    
     
