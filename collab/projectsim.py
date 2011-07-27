import sys
import json
import nltk
import csv
import urllib, urllib2, urlparse

def img(profile):
	r = urllib.urlopen(profile)
	from BeautifulSoup import BeautifulSoup
	soup = BeautifulSoup(r)
	avatar = soup.findAll('img')[0].attrs[1][-1].encode('utf-8')
        if urlparse.urlparse(avatar).scheme != 'http':
        	avatar = 'http://p2pu.org' + avatar
	#print avatar
	return avatar



proj_desc = list(csv.reader(open('proj_desc.csv'),delimiter=',',quotechar=';'))

all_desc = [row[4].lower().split() for row in proj_desc]

tc = nltk.TextCollection(all_desc)

td_matrix = {}

# Compute a term-document matrix such that td_matrix[(name,profile,cred)][term]
# returns a tf-idf score for the term in the project description document

for idx in range(len(all_desc)):
	desc = all_desc[idx] 
	fdist = nltk.FreqDist(desc)

	name = proj_desc[idx][1]
	profile = proj_desc[idx][3]
	cred = proj_desc[idx][2]
	
	
	td_matrix[(name, profile,cred)] = {}
	
	for term in fdist.iterkeys():
		td_matrix[(name,profile,cred)][term] = tc.tf_idf(term, desc)


distances = {}

for (name,profile,cred) in td_matrix.keys():
	distances[(name,profile,cred)] = {}
	(max_score_hack, most_similar_hack,hack_proj_desc) = (0.0,(None,None,None),None)
	(max_score_hacker, most_similar_hacker,hacker_proj_desc) = (0.0,(None,None,None),None)

	for (name_, profile_,cred_) in td_matrix.keys():
		terms = td_matrix[(name, profile,cred)].copy()
		terms_ = td_matrix[(name_, profile_,cred_)].copy()

		for term in terms:
			if term not in terms_:
				terms_[term] = 0

		for term_ in terms_:
			if term_ not in terms:
				terms[term_] = 0
		
		v = [score for (term,score) in sorted(terms.items())]
		v_ = [score_ for (term_, score_) in sorted(terms_.items())]
		distances[(name,profile,cred)][(name_,profile_,cred_)] = nltk.cluster.util.cosine_distance(v, v_)

		#print distances[(name,profile,cred)][(name_,profile_,cred_)]

		if profile == profile_:
			continue
		# Hack too similar:
		
		if cred_ == 'Hack' :			
			if distances[(name, profile, cred)][(name_, profile_,cred_)] > max_score_hack:
				for i in proj_desc:
					if i[3]==profile_:
						hack_proj_desc = i[4]
				(max_score_hack, most_similar_hack,hack_proj_desc) = (distances[(name,profile,cred)][(name_,profile_,cred_)], (name_,profile_,cred_),hack_proj_desc)

		# Hacker too similar:
		if cred_ == 'Hacker':
			if distances[(name, profile, cred)][(name_, profile_,cred_)] > max_score_hacker:
				for i in proj_desc:
					if i[3]==profile_:
						hacker_proj_desc = i[4]

				(max_score_hacker, most_similar_hacker,hacker_proj_desc) = (distances[(name,profile,cred)][(name_,profile_,cred_)], (name_,profile_,cred_),hacker_proj_desc)

		


	

	template = '''<div class="col"><h3>%s</h3><div class="ft"><img src="%s" width=150 height=150/><p>%s</p><p><a href="%s">P2PU Profile</a></p></div></div>'''
	template_mid = '''<div class="col"><h3>%s(H)</h3><div class="ft"><img src="%s" width=150 height=150/><p>%s</p><p><a href="%s">P2PU Profile</a></p></div></div>'''
	template_last = '''<div class="col last"><h3>%s(X)</h3><div class="ft"><img src="%s" width=150 height=150/><p>%s</p><p><a href="%s">P2PU Profile</a></p></div></div>'''


	for i in proj_desc:
		if i[3]==profile:
			project=i[4] 
	print '''<hr/>'''
	print template % (name, img(profile), project, profile)
	print template_mid % (most_similar_hack[0], img(most_similar_hack[1]), hack_proj_desc, most_similar_hack[1])
	print template_last % (most_similar_hacker[0], img(most_similar_hacker[1]), hacker_proj_desc,most_similar_hacker[1])
									

