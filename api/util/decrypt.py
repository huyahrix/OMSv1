import datetime	
from .aes256 import aes256

def decryptData(encText):
	try:
		dailyHashes = [
	  	    "0LC4K6oXKU",
	  	    "LoKlo1HcQj",
	  	    "mgrQdeZA15",
	  	    "zAy6DYwet7",
	  	    "8XJ6X2F0R8",
	  	    "tWieS9EoXL",
	  	    "kJZ2067Euo"
		    ]
		weekDay = datetime.datetime.today().weekday()
		compatibleWeekDay = weekDay + 1
		if weekDay == 6:
			compatibleWeekDay = 0
        
		passPhrase = dailyHashes[compatibleWeekDay]
		data = aes256().decrypt(encText, passPhrase).decode('utf-8')
		#print('pass phrase', passPhrase)
	except :
		return None
	
	return data
