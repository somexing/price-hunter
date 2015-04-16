#  coding:utf8
import sys
import datetime
sys.path.append("../mymodule")
import bbs, re, func 

TEST_MODE = 1 

SITE = 'amazon'
PAGE_URL_FIRST =  'http://www.amazon.com/s/ref=sr_pg_2?rh=n%3A165793011%2Ck%3ALEGO&page=1&keywords=LEGO&ie=UTF8&qid=1423726198'
PAGE_URL_prefix = 'http://www.amazon.com/s/ref=sr_pg_2?rh=n%3A165793011%2Ck%3ALEGO&page='
PAGE_URL_postfix = '&keywords=LEGO&ie=UTF8&qid=1423726198'
TOPIC_URL_prefix = ''
TOPIC_URL_postfix = ''

urllist = [PAGE_URL_FIRST, PAGE_URL_prefix, PAGE_URL_postfix, TOPIC_URL_prefix, TOPIC_URL_postfix]
#每页列表的标题匹配
#str_topic_re = r'<li id="result_(.*?)/li>'
#str_topic_re = r'<h2 class="a-size-base s-inline s-access-title a-text-normal">(.*?)</span>'
str_topic_re = r'<h2 class="a-size-base .*"(.*?)</span>'

#每个帖子内容列表匹配
 
str_content_re = ''
str_cleanhtml_re =  r'<[^>]+>|(\\r)|(\\n)'
#FixPageBBSCrawl不需要，BBSCrawl需要
str_nextpage_re = r'<li id="result_(.*?)</li>'    

re_strlist = [str_topic_re, str_content_re, str_cleanhtml_re, str_nextpage_re]

#最大页码
MAX_PAGE_IDX = 100
#test option
func.USE_PROXY = True

func.SHOW_LOG = False
func.TIME_OUT = None
func.USE_COOKIE = 0
#func.PROXY_SERVER  =   "10.42.170.85:808"
#func.PROXY_SERVER  =   "10.204.80.103:8080"
func.PROXY_SERVER  =   "10.94.235.26:8080"

bbs.printmode = False
bbs.printHTMLMode = False
bbs.debugmode = False




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
