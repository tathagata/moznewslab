import urllib, urllib2
import json
import sys
import csv

TWITTER_SRCH_URL = 'http://search.twitter.com/search.json'
TWITTER_USR_PROF = 'http://api.twitter.com/1/users/show.json?screen_name='
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


class AutoVivification(dict):
        """Implementation of perl's autovivification feature. code by nosklo in stackoverflow"""
        def __getitem__(self, item):
                try:
                        return dict.__getitem__(self, item)
                except KeyError:
                        value = self[item] = type(self)()
                return value

def get_user_location(user):
	url = TWITTER_USR_PROF + user
	#print url
	results=json.load(urllib2.urlopen(url))
	return results['location']


def geocode(address,sensor, **geo_args):
        geo_args.update({
        'address': address,
        'sensor': sensor
        })
	
	latlng=""
        try:
                url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
                result = json.load(urllib.urlopen(url))
        except:
                sys.stderr.write('Error lookng up geo-code %s' % address)
                return

        for s in result['results']:
                lat = s['geometry']['location']['lat'] 
                lng = s['geometry']['location']['lng'] 
                latlng = str(lat).split('.')[0] + ", " + str(lng).split('.')[0]
		print latlng, address
        return latlng


def get_tweets(query, **srch_args):
	page_number=1
        srch_args.update({
                'q' : query,
		'rpp':500,
                'since': '2011-07-01',
		'page_number':page_number, 
        })

	datadict=AutoVivification()
	more_tweets_left = True
	known_locos = {}
	for line in open('twitterhandles.csv').xreadlines():
		try:
			handle, lat, lng = line.split('\t')
			known_locos[handle]=lat.split('.')[0] + ", " + lng.strip('\n').split('.')[0]
		except:
			pass

        #users = []
        while more_tweets_left:
                url_srch = TWITTER_SRCH_URL + '?' + urllib.urlencode(srch_args)
                #print url_srch 
                results = json.load(urllib.urlopen(url_srch))
                for key in results.keys():
                        if key == 'error':
                                print 'Done'
                                more_tweets_left = False

                if not more_tweets_left or not results['results']:
                        more_tweets_left = False #sanity
                        break
                else:
                        for result in results['results']:
				date=result['created_at']
				created_at=date[5:-15]
				user=result['from_user']
				print user
				#since any user can tweet about #moznewslab, and mosty the do not have
				# geo data, so lookup base location of the user
				try:
					latlng=known_locos[user]
				except:
					loco=get_user_location(user)
					if len(loco)!=0: 
						latlng=geocode(loco,sensor="false")
					else:
					#dump it on dear Mr. LabModerator, @phillipadsmith
						latlng="43, -78"
				if len(latlng)!=0:
					try:
						datadict[latlng]+=1
					except:
						datadict[latlng]=1
				
                        page_number +=1
                        p = {'page':page_number}
                        srch_args.update(p)

        return datadict


if __name__ == "__main__":
	datadict=get_tweets('moznewslab')

	for k,v in datadict.items():
		print k,v
	
