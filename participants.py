from __future__ import division
import participants
import urllib, urllib2, urlparse
import json
import random
import sys

PARTICIPANTS=['http://p2pu.org/en/groups/knight-mozilla-learning-lab/people/','http://p2pu.org/en/groups/knight-mozilla-learning-lab/people/2/1','http://p2pu.org/en/groups/knight-mozilla-learning-lab/people/3/1']

GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

def scrape_p2pu():
	#html = '''<div id ="content"><a href='%s'><img width="54" height="54" alt="%s" src="%s"><h3>%s</h3></a></div></div>'''	
	profile_urls = []
	zIndex = 0
	for PARTICIPANT in PARTICIPANTS:
		f = urllib2.urlopen(PARTICIPANT)
		from BeautifulSoup import BeautifulSoup
		soup = BeautifulSoup(f)
		figures = soup('figure')
		for figure in figures:
			profile_url = 'http://p2pu.org' + figure.findNext('a').attrs[0][1].encode('utf-8')
			try:
				if profile_url in profile_urls:
					continue
				else:
					profile_urls.append(profile_url) 
					purl = urllib2.urlopen(profile_url)
					psoup = BeautifulSoup(purl)

					location = psoup('dd')
					
					geo_loc = geocode(location[0].text, sensor="false")
					#print "Geo Location",location[0].text,geo_loc
					if geo_loc is None:
						#print 'No data', profile_url
						continue

					uls = psoup('ul')
					skills = []
					for ul in uls:
						if ul.findNext('a').attrs[-1][-1].startswith('View'):
							skills.append(ul.findNext('a').text)
					skillset = '/'.join(skills)
							
					avatar = figure.findNext('img').attrs[1][-1].encode('utf-8')
					if urlparse.urlparse(avatar).scheme != 'http':
						avatar = 'http://p2pu.org' + avatar
					name = figure.findNext('img').attrs[-1][-1].encode('utf-8')

					zIndex += 1
					print "['",name, "','", avatar, "','", profile_url,"',", geo_loc,",", zIndex,",'", skillset,"'],"
			except:
				pass
	

def geocode(address,sensor, **geo_args):
    	geo_args.update({
        'address': address,
        'sensor': sensor  
    	})

	try:
    		url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    		result = json.load(urllib.urlopen(url))
	except:
		sys.stderr.write('Error lookng up geo-code %s' % address)	
		return

    	for s in result['results']:
		#Since same city gives the same lat lngs, adding some random bits
		# so that the avatars dont overlap
		lat = s['geometry']['location']['lat'] + random.random()/2
		lng = s['geometry']['location']['lng'] + random.random()/2
		latlng = str(lat) + ", " + str(lng)
	return latlng	
    	#print json.dumps([s['geometry']['location']['lat'][0] for s in result['results']], indent=2)

if __name__ == '__main__':
	scrape_p2pu()

