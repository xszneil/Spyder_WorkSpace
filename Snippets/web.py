
#work with web===================================================
import urllib2
webUrl = urllib2.urlopen("http://joemarini.com")    #get url, urllib2 is for python2, in python 3 we have urlib.request
print ("result code: " + str(webUrl.getcode()))
data = webUrl.read()
print data

#from HTMLParser import HTMLParser    #parse html
#parser = HTMLParser()
#f = open("samplehtml.html")
#if f.mode == "r":
#    contents = f.read() # read the entire file
#    parser.feed(contents)


#parse json, need to know the json structure============
import json
urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
webUrl = urllib2.urlopen(urlData)
data = webUrl.read()
theJSON = json.loads(data)

theJSON["metadata"]["title"]
theJSON["metadata"]["count"]

for i in theJSON["features"]:
    print i["properties"]["place"]

for i in theJSON["features"]:
    if i["properties"]["mag"] >= 4.0:
        print "%2.1f" % i["properties"]["mag"], i["properties"]["place"]


# parse xml====================
import xml.dom.minidom
doc = xml.dom.minidom.parse("samplexml.xml");
# print out the document node and the name of the first child tag
print doc.nodeName
print doc.firstChild.tagName
# get a list of XML tags from the document and print each one
skills = doc.getElementsByTagName("skill")
print "%d skills:" % skills.length
for skill in skills:
    print skill.getAttribute("name")
# create a new XML tag and add it into the document
newSkill = doc.createElement("skill")
newSkill.setAttribute("name", "jQuery")
doc.firstChild.appendChild(newSkill)

skills = doc.getElementsByTagName("skill")
print "%d skills:" % skills.length
for skill in skills:
    print skill.getAttribute("name")


# use twilio api=========================
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = "ACc19caa2b0daac4fd70aaf5f9f7278355"
auth_token = "510c29f9568ed25b1e21c91395152c76"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to="+13522227518",from_="+15169861050",body="Hello there!")


# use what do you like search engine api to check dirty words=======
import urllib

def read_text():
    quotes = open('movie_quotes.txt')
    contents_of_file = quotes.read()
    #print(contents_of_file)
    check_profanity(contents_of_file)
    quotes.close()

def check_profanity(text):
    conn = urllib.urlopen("http://www.wdyl.com/profanity?q="+text)
    output = conn.read()
    print(output)
    conn.close()

