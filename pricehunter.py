#  coding:utf8
'''
用例1 获取所有最新降价的产品名称和价格
1 外部输入多个URL和匹配内容正则表达式，文件名 filename_all.cfg
2 读入之前保存的产品名称和价格 old_price_id_list
2 调用多线程获取每个URL得到网页内容并用对应的正则解出结果 new_price_id_list
3 对比 old_price_id_list，如果有降低则进行报告和记录


用例2 获取输入的某产品名称的最低价格
0 外部输入产品关键字  id
1 外部读入多个查询的URL和匹配内容正则表达式 filename_qry.cfg
2 读入之前保存的产品名称和价格 price_id_list
2.1 组合URL得到查询URL 
3 调用多线程获取每个URL得到网页内容并用对应的正则解出结果  new_price_id_list
4 对比  old_price_id_list，如果新访问到了最低的结果，如果有降低则进行报告和记录






'''
import sys
import datetime
sys.path.append("../mymodule")
import bbs, re, func 

TEST_MODE = 1 



SITE = 'amazon'
 
if __name__ == '__main__':
    if TEST_MODE ==1 :
      MAX_PAGE_IDX = 1  
    filename= 'lego'+datetime.date.today().strftime('%Y%m%d')+'.txt'
    fp = open(filename,'w')
    re1 = re.compile( str_topic_re )
    re2 = None #re.compile( str_content_re, re.S )
    re3 = re.compile( str_cleanhtml_re )
    re4 = re.compile( str_nextpage_re )
    relist = [re1, re2, re3, re4]
    amz = bbs.FixPageBBSCrawl()
    amz.init_argv(urllist,  relist,  fp , MAX_PAGE_IDX )
          
    urllist = [PAGE_URL_FIRST, PAGE_URL_prefix, PAGE_URL_postfix, TOPIC_URL_prefix, TOPIC_URL_postfix]  
        
    amz.OpenBBSTopicList1(urllist )

    fp.flush()
        
    fp.close() 
