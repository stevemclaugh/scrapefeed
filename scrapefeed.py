from flask import Flask
from flask import request
from flask import render_template
import jinja2
import random
from bs4 import BeautifulSoup
import urllib2
from datetime import datetime, timedelta
from ftfy import fix_encoding
from unidecode import unidecode

TEMPLATE_DIR = '/home/smcl/scrapefeed/templates/' ## Swap in your username.
TEMPLATE_FILE = 'form.html'
TEMPLATE_OUT = 'out.html'

application = Flask(__name__)
 
@application.route('/')
def main():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    html = env.get_template(TEMPLATE_FILE).render()
    return html


@application.route('/', methods=['POST'])
def my_form_post():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    text = request.form['text'].strip()
    print "---> URL entered: |" + text +'|'              # logging URLs in shell for debugging
    random.seed(text)
    url_dir='http://scrapefeed.net/feed/'
    if '.mp3' in text.lower():
        links=[text]
        title=text.split('/')[-1][:-4]
    else:
        try:
            page=fix_encoding(urllib2.urlopen(text).read().decode('utf-8'))
        except:
            try:
                page=fix_encoding(urllib2.urlopen(text).read().encode('utf-8'))
            except:
                try:
                    page=unidecode(unicode(urllib2.urlopen(text).read()))
                except:
                    page=urllib2.urlopen(text).read()
        soup=BeautifulSoup(page,'lxml')
        links=[]
        try: title=soup.title.string
        except: title=text.split('/')[-1].split('.')[0]    
        for link in soup.findAll('a'):
            temp_link=unicode(link.get('href')).strip()
            if temp_link.lower()[-4:]=='.mp3':
                links.append(temp_link)
    rsspart1='''<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>%s</title>
    <description></description>
    <link>%s</link>
    <language>en-us</language>
    <docs>%s</docs>
    <webMaster>Steve McLaughlin</webMaster>
    <itunes:author></itunes:author>
    <itunes:subtitle></itunes:subtitle>
    <itunes:summary></itunes:summary>
    <itunes:owner>
           <itunes:name>Steve McLaughlin</itunes:name>
           <itunes:email>steve.mclaugh@gmail.com</itunes:email>
    </itunes:owner>
<itunes:explicit>Yes</itunes:explicit>
<itunes:image href=""/>   
<itunes:category text="Technology">
     <itunes:category text="Podcasting"/>
</itunes:category>
'''%(title,url_dir,url_dir)

    rsspart2='''<item>
<title>%(title)s</title>
<link>%(url_dir)s</link>
<guid>%(mp3link)s</guid>
<description></description>
<enclosure url="%(mp3link)s" length="" type="audio/mpeg"/>
<category>podcasts</category>
<pubDate>%(pub_date)s</pubDate>
<itunes:author></itunes:author>
<itunes:explicit>No</itunes:explicit>
<itunes:subtitle></itunes:subtitle>
<itunes:summary></itunes:summary>
<itunes:duration></itunes:duration>
<itunes:keywords></itunes:keywords>
</item>
'''

    rsspart3='''
</channel>
</rss>
'''

    feed_items=[]
    counter=0
    for mp3_url in links:
	    temp_datetime = datetime.today() - timedelta(hours = counter)
            time_string=temp_datetime.strftime("%a, %d %b %Y %H:%M:%S")+' -0500'
            data = {'url_dir':url_dir,'title':mp3_url.split('/')[-1][:-4],'mp3link':mp3_url,'pub_date':time_string}
	    feed_items.append(rsspart2%data)
            counter+=1

    processed_text = rsspart1+'\n'.join(feed_items)+rsspart3

    filename=str(random.random()).replace('.','')+'.rss'
    with open('/var/www/html/feed/'+filename,'w') as fo:
	fo.write(processed_text)
    url_out=url_dir+filename
    
    html = env.get_template(TEMPLATE_OUT).render(url_out=url_out,title=title)
    return html
    
    


@application.route('/feed/<string:feed>')
def feed(feed):
    with open('/var/www/html/feed/'+feed) as fi: return fi.read()




if __name__ == '__main__':
    try:
        application.run(host='0.0.0.0')
    except Exception as detail:
            print "* Error: "+str(detail)
