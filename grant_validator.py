"""	File: ANDS_GrantValidator.py
	Author: Ben Weatherall
	Contact: Ben.Weatherall@adelaide.edu.au
	Python 3.4
	Description:
		Will take a csv file (Tab delimited) with at least one column named PURL who's content is a 
	research grant purl url (http://purl.org/au-research/grants/arc/20774028 for example). 
	Makes use of the ANDS API to determine if a grant id is valid.
	Returns a Tab delimited csv file with an additional column 'resolves' the content of this field 
	will be either true or false.
	As this is only a quick script, the columns on the output won't be ordered
"""
import urllib.request, json, difflib, csv, sys, pickle

API_KEY="" # Enter Your API Key

def importCSV():
	f = open(sys.argv[1], 'rt')
	try:
		reader = csv.DictReader(f, dialect='excel-tab')
		myDictionaryArray = []
		for row in reader:
			myDictionaryArray.append(row)
		
	finally:
		f.close()
		return myDictionaryArray
		
def request(key):
	
	request_url = "http://researchdata.ands.org.au/registry/services/{}/getGrants?id={}".format(API_KEY, key)

	request = urllib.request.Request(request_url)

	response = urllib.request.urlopen(request)

	string = str(response.readall().decode('utf-8'))

	result = json.loads(string)['message']

	if(result['numFound'] == 0):
		return False
	elif (result['numFound'] == 1):
		return True
	else:
		return "Too many Results"
		

	
def main():
	myArray = importCSV()
	validatedIDs = {}
	try:
		with open ('resolvedIDs.pickle', 'rb') as f:
			validatedIDs = pickle.load(f)
	except:
		pass
	
	
	avoidedDupes = 0

	for count, row in enumerate(myArray):
		row['grant_id'] = row['PURL'].split('/')[-1]
		print("{}/{}: {}".format(count, len(myArray), row['grant_id']))
		if(row['grant_id'] in validatedIDs):
			row['resolves'] = validatedIDs[row['grant_id']]
			avoidedDupes += 1
		else:
			row['resolves'] = request(row['grant_id'])
			validatedIDs[row['grant_id']] = row['resolves']

	with open('validated_grantIDs.txt', 'w') as f:  # Just use 'w' mode in 3.x
		w = csv.DictWriter(f, myArray[0].keys(), dialect='excel-tab')
		w.writeheader()
		for row in myArray:
			w.writerow(row)
	
	toPickle = {}
	for ID, resolution in validatedIDs.items():
		if(resolution == True):
			toPickle[ID] = resolution
			
	with open ('resolvedIDs.pickle', 'wb') as f:
		pickle.dump(toPickle, f, pickle.HIGHEST_PROTOCOL)
		
	print('Avoided {} duplicate ids'.format(avoidedDupes))
	input("Enter to End.")

if __name__ == "__main__":
    main()
