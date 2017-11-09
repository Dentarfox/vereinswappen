# MIT License

# Copyright (c) 2017 Sebastian Frei

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from clint.textui import colored, puts
import os
import csv
from lxml import html
import requests
import urllib.request
import emoji

puts(colored.white('Vereinswappen Scrapper v 1.0 by Sebastian Frei'))
puts(colored.yellow('Geben Sie den exakten Dateipfad ihrer CSV Datei an.'))
file = input("Dateipfad (TestCSV): ")
if file == "":
	file="TestCSV.csv"

try:
   with open(file, newline='') as csvfile:
      puts(colored.yellow("lese Datei: " + file))

      logoreader = csv.DictReader(csvfile)
      for row in logoreader:
      	r = requests.post("http://www.vereinswappen.de/vereine.php?option=vereinssuchen", data={'verein': row['verein'], 'suchen': 'Suchen'})
      	tree = html.fromstring(r.content)
      	#print(r.content)
      	vereinswappen = tree.xpath('//img[@style="max-width: 100px; width: 100px;"]/@src')
      	i =1
      	for x in vereinswappen:
      		if not os.path.exists('Wappen'):
      			os.makedirs('Wappen')
      		filename = "Wappen/"+row['verein']+str(i)+".png"
      		urllib.request.urlretrieve(x, filename)
      		i+=1
      	#print(vereinswappen)
      	puts(colored.yellow('Lade Wappen '+row['verein']+'...'))
      	print(emoji.emojize('Success! :white_check_mark:', use_aliases=True))

   if not logoreader:
      print ("keine Daten vorhanden siehe README " + file)
      file_content = "name\n"

except IOError as e:
   print ("I/O error({0}): {1}".format(e.errno, e.strerror))
except: #handle other exceptions such as attribute errors
   print ("Unexpected error:", sys.exc_info()[0])
print (emoji.emojize(":soccer:  Fertig! Die Wappen befinden sich im Ordner Wappen ", use_aliases=True))
