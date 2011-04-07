#! /usr/bin/env python

import os
from optparse import OptionParser
from driver import run
from stringUtil import file2string, string2file
from parse import getItem, getItems

desc="""dict is a python program for building music dictation lessons.
"""

parser = OptionParser(description=desc)

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
  help="verbose output");
parser.add_option("-r", "--render", action="store_true", dest="render", 
  help="render dictation exercise, i.e., generate all .wav files");
parser.add_option("-p", "--play", action="store", type="string", dest="play",
  help="play dictation exerices N, where N = PLAY")
parser.add_option("-c", "--catalogue", action="store_true", dest="catalogue",
  help="display catalogue of entries in dictation excercise.  Use -v for verbose version.")
parser.add_option("-f", "--file", action="store", type="string", dest="filename",
  help="take input from file.  Default (no -f) is the file 'dictation'")
parser.add_option("-w", "--webpage", action="store_true", dest="webpage", 
  help="create web page for dictation exercises.  Look for 'index.html'.  You need to run 'dict -r' to render the audio files for the webpage to function as expected.")


(options, args) = parser.parse_args()

if options.filename:
  filename = file2string(options.filename)
else:
  filename = "dictation"

if options.catalogue:
  print
  dictation = file2string(filename)
  items = getItems(dictation, "ex")
  header = getItem(dictation, "dictation")
  title = getItem(header, "title")
  print "File:", filename
  print "Title:", title
  for item in items:
    index = getItem(item, "index")
    content = getItem(item, "content")
    if options.verbose:
      print
      print index
      print content
    else:
      line = content.split("\n")
      print index, line[0]

if options.play:
  dictation = file2string(filename)
  items = getItems(dictation, "ex")
  settings = getItems(dictation, "voice")

  for item in items:
    index = getItem(item, "index")
    if index == options.play:
      print
      theExercise =  getItem(item, "content")+"\n"
      n = 1
      for voice in settings:
        target = "voice:"+`n`
        theExercise = theExercise.replace(target, target+"\n"+voice+"\n")
        n = n + 1
      string2file(theExercise, "tmp1010")
      cmd = "sf2a -f tmp1010 -o dict1010"
      os.system(cmd)
      os.system("play dict1010.wav")
      print

if options.render:
  dictation = file2string(filename)
  items = getItems(dictation, "ex")
  settings = getItems(dictation, "voice")

  print "\n", len(items), "items to render ...\n"

  for item in items:
    index = getItem(item, "index")
    theExercise =  getItem(item, "content")+"\n"
    n = 1
    for voice in settings:
      target = "voice:"+`n`
      theExercise = theExercise.replace(target, target+"\n"+voice+"\n")
      n = n + 1
    outfile = index
    string2file(theExercise, "tmp1010")
    cmd = "sf2a -f tmp1010 -o "+outfile
    os.system(cmd)
  print "\n", len(items), "items rendered\n"

if options.webpage:
  dictation = file2string(filename)
  items = getItems(dictation, "ex")

  n = 0

  text = '<html>\n<head>\n<link rel="stylesheet" type="text/css"  media="screen" href="style.css">\n'

  text += file2string("script")

  text += '\n<head>\n\n<body>\n\n'

  element1 = '<p class="item">'
  element2 = ': '
  element3 = '<span class="embed"><embed src="'
  element4 = '" width=300 height=15px autostart=false repeat=false loop=false"> <embed></span>\n</p>\n\n'

  element5 = file2string("element5")

  element6 = file2string("element6")

  footer = '</body>\n</html>\n\n'

  for item in items:
    index = getItem(item, "index")
    theExercise =  getItem(item, "content")+"\n"
    n = n + 1
    print n, theExercise, "\n"
    file = `n`+".wav"
    text += element1 + `n` + element2 + element3 + file + element4
    element5x = element5.replace("example", "example"+`n`)
    element6x = element6.replace("example", "example"+`n`)
    text += element5x + theExercise + element6x+"\n\n"

  text += footer
  string2file(text, "index.html")



