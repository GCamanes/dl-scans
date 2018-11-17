################################################################################
# Python scipt : dowload all mangas with all chapters from http://lelscanv.com #
################################################################################

## INSTALL NEEDED
# sudo apt-get install curl

# -*- coding: utf-8 -*-

## IMPORT
import os, sys, getopt, argparse

## CONSTANT VARIABLES
PATH = "."

WEBSITEFIRST = "http://lelscanv.com/lecture-en-ligne-one-piece.php"
WEBSITEPART1 = "http://lelscanv.com/lecture-en-ligne-"
WEBSITEPART2 = ".php"

WEBSITEPART1_CHAP = "http://lelscanv.com/scan-"

LIST_MANGAS = []
DICO_MANGAS = {}

# Function to get the complete name of a chapter
# Format : [nameOfManga]_[chap num on 4 digit]
# Used in : chap repository and img file
def getChapName(manga, chap):
	chapName = ""
	if (len(chap.split(".")[0]) == 1):
		chapName = manga+"_chap000"+chap
	elif (len(chap.split(".")[0]) == 2):
		chapName = manga+"_chap00"+chap
	elif (len(chap.split(".")[0]) == 3):
		chapName = manga+"_chap0"+chap
	else:
		chapName = manga+"_chap"+chap
	return chapName

# Function to get all available chapter from a manga
# Return : list[string]
def getMangaChapList(manga):
	# Open html page
	os.system("curl -s " + WEBSITEPART1+manga+WEBSITEPART2 + " | grep '<option value="+ \
		'"'+WEBSITEPART1_CHAP+manga+"' > "+PATH+"/mangaChapList.txt")
	f = open(PATH+'/mangaChapList.txt', 'r')
	# get html content
	content = f.readlines()
	# close file and delete it
	f.close()
	line = content[0]
	line = line.split("</option>")[:-1]
	listChap = []
	for i in range(0, len(line)):
		listChap.append(line[i].split(">")[1])
	return listChap[::-1]

# Function to get all mangas available in the website
# Return : void
def getMangasList():
	# Open html page
	os.system("curl -s " + WEBSITEFIRST + " | grep '"+WEBSITEPART1+ \
		"' | grep 'select' > "+PATH+"/mangaslist.txt")
	f = open(PATH+'/mangaslist.txt', 'r')
	# get html content
	content = f.readlines()
	# close file and delete it
	f.close()
	line = content[0]
	line = line.split("</option>")[:-1]
	for i in range(0, len(line)):
		manga = line[i].split(".php")[0].split(WEBSITEPART1)[1]
		mangaMaj = line[i].split(">")[1]
		LIST_MANGAS.append(manga)
		DICO_MANGAS[manga] = getMangaChapList(manga)

# Function to get all available pages from a chapter
# Return : list[string]
def getMangaChapPageList(manga, chap):
	# Open html page
	os.system("curl -s " + WEBSITEPART1_CHAP+manga+"/"+chap + " | grep '<a href="+ \
		'"'+WEBSITEPART1_CHAP+manga+"/"+chap+"/' > "+PATH+"/mangaChapPageList.txt")
	f = open(PATH+'/mangaChapPageList.txt', 'r')
	# get html content
	content = f.readlines()
	# close file and delete it
	f.close()
	line = content[0]
	line = line.split("</a>")
	listPage = []
	for i in range(0, len(line)):
		line[i] = line[i].split(">")[1]
		if (line[i] != "Prec"):
			if (line[i] != "Suiv"):
				listPage.append(line[i])
			else:
				break
	return listPage

# Function to download a page as an image file 
# Return : list[string]	
def dlMangaChapPageImgFile(manga, chap, page, path):
	imgFileAdress = ""
	imgFileName = ""
	# Loop to manage some bug that appear when the targeted line is absent from the curl return
	while("?v=" not in imgFileAdress):
		# Open html page
		os.system("curl -s " + WEBSITEPART1_CHAP+manga+"/"+chap+"/"+page+ \
			" | grep '<img src="+'"'+ \
			"/mangas/"+manga+"/' > "+PATH+"/mangaImgFile.txt")
		f = open(PATH+'/mangaImgFile.txt', 'r')
		# get html content
		content = f.readlines()
		# close file and delete it
		f.close()
		line = content[0]

		imgFileName = line.split("?v=")[0].split("/")[-1]
		imgFileName = getChapName(manga, chap)+"_"+imgFileName
		imgFileAdress = line.split('"')[1]
		if ("http://lelscanv.com/" not in imgFileAdress):
			imgFileAdress = "http://lelscanv.com"+imgFileAdress
		print imgFileAdress

	print imgFileName
	os.system('curl -o '+path+'/'+imgFileName+' '+ imgFileAdress +" > /dev/null")

# Function to download chapter in listChap from a manga
# Return : void
def dlMangaScan(manga, listChap):
	# Loop on all available chapters
	for chap in listChap:
		print "# DL : chapter", str(chap), "..."
		pathChap = PATH+"/"+manga+"/"+getChapName(manga, chap)
		# Managing chapter folder creation
		try :
			os.mkdir(pathChap)
		except :
			pass
		# Downloading all pages of the chapter
		listPage = getMangaChapPageList(manga, chap)
		print listPage
		for page in listPage:
			dlMangaChapPageImgFile(manga, chap, page, pathChap)

# Function to download a manga
# Return : void
def dlManga(manga):
	print "## DL", manga, "..."

	# Managing manga folder creation
	try :
		os.mkdir(PATH+"/"+manga)
		print "# create a directory"
	except :
		print "# don't need to create a directory"
		pass

	listChap = getMangaChapList(manga)
	dlMangaScan(manga, listChap)

def dlMangaChap(manga, chap):
	print "## DL", manga, "..."

	# Managing manga folder creation
	try :
		os.mkdir(PATH+"/"+manga)
		print "# create a directory"
	except :
		print "# don't need to create a directory"
		pass

	listChap = getMangaChapList(manga)
	if (chap in listChap):
		dlMangaScan(manga, [chap])
	else:
		print "/!\ "+manga+" : chapter "+chap+" not available"

def dlMangaLastChap(manga, last):
	print "## DL", manga, "..."

	# Managing manga folder creation
	try :
		os.mkdir(PATH+"/"+manga)
		print "# create a directory"
	except :
		print "# don't need to create a directory"
		pass

	listChap = getMangaChapList(manga)
	print last
	if (last > len(listChap) or last < 0) :
		print "/!\ "+manga+" : only "+str(len(listChap))+" available chapters"
	else:
		dlMangaScan(manga, listChap[-last:])

# Function to show all available manga and their chapters
# Return : void
def showMangaList():
	for manga in LIST_MANGAS:
		print "-", manga, ": chapter from", DICO_MANGAS[manga][0], "to", DICO_MANGAS[manga][-1]

# Function to run the python script
def main():
	# Definition of argument option
	parser = argparse.ArgumentParser(prog="dlScans.py")
	parser.add_argument('-a', '--all', help='liste of all available mangas', action='store_true')
	parser.add_argument('-m', '--manga', nargs=1, help='select a manga to download', action='store', type=str)
	parser.add_argument('-c', '--chap', nargs=1, help='select a specific chapter to download', action='store', type=str)
	parser.add_argument('-l', '--last', nargs=1, help='select a last X chapter to download', action='store', type=int)
	# Parsing of command line argument
	args = parser.parse_args(sys.argv[1:])

	if (args.all == True):
		print "** List of all available mangas **"
		print "... loading ..."
		getMangasList()
		showMangaList()
		sys.exit()

	elif (args.manga != None):
		if (args.chap == None and args.last == None):
			print "downloading all chapters from", args.manga[0]
			dlManga(args.manga[0])
		elif (args.chap != None):
			print "downloading chapter", args.chap[0], "from", args.manga[0]
			dlMangaChap(args.manga[0], args.chap[0])
		else:
			print "downloading the last", args.last[0], "chapter(s) from", args.manga[0]
			dlMangaLastChap(args.manga[0], args.last[0])
	else:
		print "/!\ No arguments"
		parser.print_help()

	#dlManga("fairy-tail", 600)

if __name__ == "__main__":
	main()

