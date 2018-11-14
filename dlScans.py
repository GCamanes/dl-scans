#############################################################################
# Pyhtn scipt : dowload all mangas with all chapters from http://lelscan.me #
#############################################################################

## INSTALL NEEDED
# sudo apt-get install curl
# sudo apt-get install python-pip
# sudo pip install pandas

# -*- coding: utf-8 -*-

## IMPORT
import os
import pandas as pd

## CONSTANT VARIABLES
PATH = "."

WEBSITEFIRST = "http://lelscanv.com/lecture-en-ligne-one-piece.php"
WEBSITEPART1 = "http://lelscanv.com/lecture-en-ligne-"
WEBSITEPART2 = ".php"

TARGETFORMANGALIST = "http://lelscanv.com/lecture-en-ligne-"

LIST_MANGAS = []
DICO_MANGAS = {}


# 1
# Function to get all mangas available in the website
# get also the last chapter for each of them in a dictionary
# Return : void
def getMangasList():
	# Open html page
	os.system("curl -s " + WEBSITEFIRST + " | grep '"+TARGETFORMANGALIST+"' | grep 'select' > "+PATH+"/mangaslist.txt")
	
	f = open(PATH+'/mangaslist.txt', 'r')
	# get html content
	content = f.readlines()
	# close file and delete it
	f.close()
	print len(content)
	line = content[0]
	line = line.split("</option>")[:-1]
	print len(line)
	for i in range(0, len(line)):
		manga = line[i].split(".php")[0].split(TARGETFORMANGALIST)[1]
		mangaMaj = line[i].split(">")[1]
		print i, manga, mangaMaj
		LIST_MANGAS.append(manga)
		DICO_MANGAS[manga]=mangaMaj

if __name__ == "__main__":

	print "Vive les mangas !"

	getMangasList()
	print LIST_MANGAS
	print DICO_MANGAS
