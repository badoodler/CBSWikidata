import pywikibot
from pywikibot.data import api
from pprint import pprint
from datetime import datetime
import urllib.request, json 
import time
#test = wikidata in real wikidata
site = pywikibot.Site("test", "wikidata")
repo = site.data_repository()
#item = reference to "Germany" item because Netherlands does not exist in test.wikidata = Q55 in real wikidata
item = pywikibot.ItemPage(repo,"Q343")
#property = statement within the item that you want to change. (population) = P1082 in real wikidata
property = "P63"
#1000 is populationnumber atm, should be CBS data number
srclink = "https://opendata.cbs.nl/statline/#/CBS/nl/dataset/37296ned"
# with urllib.request.urlopen("https://opendata.cbs.nl/ODataApi/odata/37296ned/UntypedDataSet?$filter=((Perioden+eq+%272017JJ00%27))&$select=TotaleBevolking_1") as url:
    # data = json.loads(url.read())

# population = data["value"][0]["TotaleBevolking_1"]


with open('C:/Users/Levi/Desktop/data.json') as file:
    data = json.load(file)

# pprint(data)
for x,y in enumerate(data):

	if( x % 2 == 0 and x > 0):
		print("sleeping for 30 seconds")
		#this timeout is to prevent getting a timeout which is to protect from vandalism in wikidata. If you edit too much, too fast without having bot permissions you will get blocked.
		time.sleep(30) # seconds
		
		
	print(data[x]["result"])
	print(data[x]["srcDate"])
	print(data[x]["srcTableUrl"])
	print(data[x]["srcurl"])

	def set_claim(numToInput):
		claim = pywikibot.Claim(repo, property)
		claim.setTarget(pywikibot.WbQuantity(numToInput, site=repo))
		item.addClaim(claim, bot=True)
		#this link should be CBS source table link
		add_source_url(claim, data[x]["srcurl"])
		#date should be the date that is specified for last updated CBS data date
		add_point_in_time(claim, pywikibot.WbTime(year = data[x]["srcDate"]))
		return claim

	def create_claim(pid, isReference=False):
		return pywikibot.Claim(repo, pid, isReference=isReference)
		
	def add_point_in_time(claim, date):
		#p66 = P585 in real wikidata
		pitclaim = pywikibot.Claim(repo, 'P66', isQualifier=True)
		pitclaim.setTarget(date)
		claim.addQualifier(pitclaim)
		
	def add_source_url(claim, source):
		#P93 = P854 in real wikidata
		source_claim = create_claim('P93', isReference=True)
		source_claim.setTarget(source)
		now = datetime.now()
		source_date = pywikibot.WbTime(year=now.year, month=now.month, day=now.day)
		#P388 = P813 in real wikidata
		date_claim = create_claim('P388', isReference=True)
		date_claim.setTarget(source_date)
		claim.addSources([source_claim,date_claim], bot=True)

	set_claim(data[x]["result"])

#sources used for code:
#https://github.com/JKatzwinkel/wikidata-sempub-util/blob/a933a0a8eb514f33f409a8a03b2fc8f80096b395/wiki.py
#https://www.wikidata.org/wiki/Wikidata:Pywikibot_-_Python_3_Tutorial/Quantities_and_Units