import datetime	
from .aes256 import aes256
import json

def encrypt():

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
	print('pass phrase: ', passPhrase)
	return aes256().encrypt(json.dumps({ "username": "DINHTHIEN", "password": "@abc123@"}), passPhrase).decode()


if __name__ == '__main__':
	print(encrypt())

