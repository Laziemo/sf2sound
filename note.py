import math

from parse import splitToken, trisectToken, isSubset, alphaPrefix, numPrefix, count
from ring import Ring

class Note(object):

  # CONSTANTS
  semitoneFactor = math.exp(math.log(2)/12.0)
  middleCFreq = 261.62556530059868
  CFreq_1 = middleCFreq/2  # 130.81278265029934 Hertz
  CFreq_2 = CFreq_1/2      #  65.40639132514967 Hertz
  CFreq_3 = CFreq_2/2      #  32.70319566257484 Hertz
  CFreq_4 = CFreq_3/2      #  16.351597831287421 Hertz

  alternateNoteDict = { }

  def __init__(self, NOTE_TABLE):
    self.ring = Ring()
    self.setNotes(NOTE_TABLE)
    self.setAlternateNoteDict()
    self.accents = ['+', '-', ',', '.', '_', '^']
    self.setFrequencyDictionary(self.CFreq_4, NOTE_TABLE)
     
  def setNotes(self, NOTE_TABLE):
  # List of note names
    if NOTE_TABLE == { }:
      self.notes = ["do", "di", "re", "ri", "mi", "fa", "fi", "sol", "si", "la", "li", "ti"]
    else:
      self.notes = NOTE_TABLE.keys()
    self.ring.pushList(self.notes)
    
  """
  def setNotes(self, noteList):
  # List of note names
    self.notes = noteList
    self.ring.pushList(self.notes)
  """
  
  # return unique numerical index for each note token
  def index(self, token):
  
    # scale length:
    SL = len(self.notes)
  
    # parse
    root, infix, suffix = trisectToken(token)
    root = self.normalizedNote(root)
    # print "trisection["+token+"]:", root, infix, suffix
   
    # get index of bare note 
    k = self.ring.index(root)
    if k < 0:
      return -1000
   
    # add octave shifts
    if len(infix) > 0:
      octave = int(infix) - 1
    else:
      octave = 0
    octave += count('^', suffix)
    octave -= count('_', suffix)
    k = k + SL*octave
   
    # add semitione shifts
    s = count('+', suffix)
    s -= count('-', suffix)
    k += s
   
    return k
   
  def note(self, j):
  # return normalized note of index j
  # scale length:
    SL = len(self.notes)
    k = j % SL
    octave = j // SL
    if octave == 0:
      return self.notes[k]
    else:
      octave = octave + 1
      return self.notes[k]+`octave`
   
  def isNote(self, token):
    root, suffix = splitToken(token)
    a = alphaPrefix(root)	
    a = self.normalizedNote(a)
    if a in self.notes:
      return True
    else:
      return False
      
  def setAlternateNoteDict(self):
    self.alternateNoteDict = {
     "de":"ti",
     "ra":"di",
     "me":"ri",
     "fe":"mi",
     "se":"fi",
     "le":"si",
     "te":"li"
    } 
    self.alternateNotes = self.alternateNoteDict.keys()
    
  def normalizedNoteData(self, x):
    y = alphaPrefix(x)
    root, suffix = splitToken(x)
    if y in self.alternateNoteDict.keys():
      return self.alternateNoteDict[y]+suffix
    else:
      return y, suffix
    
  def normalizedNote(self, x):
    y = alphaPrefix(x)
    root, suffix = splitToken(x)
    if y in self.alternateNoteDict.keys():
      return self.alternateNoteDict[y]+suffix
    else:
      return y+suffix

  def setFrequencyDictionary(self, baseFrequency, NOTE_TABLE):
    if NOTE_TABLE == {}:
      self.noteFreq = {}
      freq = baseFrequency
      for j in range(0, len(self.notes)):
        self.noteFreq[self.notes[j]] = freq
        freq = self.semitoneFactor*freq
    else:
      self.noteFreq = NOTE_TABLE
      self.noteFreq["x"] = 0.0
      

  def freq(self, token, nSemitoneShifts, octaveNumber):
    # Return frequency of note defined by token
    
    # base calculation
    root, suffix = splitToken(token)
    a = alphaPrefix(root)
    a = self.normalizedNote(a)
    f = self.noteFreq[a]
    
    # apply octave number
    for i in range(0, octaveNumber):
      f = 2*f
    
    # apply transpose register
    factor = pow(self.semitoneFactor, nSemitoneShifts);
    # print "factor:", factor
    f = f*factor
    
    # process upward octave shifts 
    n = 0
    np = numPrefix(token[len(a):])
    if len(np) > 0:
      n = int(np[0:1])-1
    else:
      n = 0
    n += count('^', suffix)   
    for i in range(0, n):
      f = 2.0*f 
      
    # process downward octave shifts 
    n = count('_', suffix)
    if n > 0:
      for i in range(0,n):
        f = f/2.0
        
    # process semitone shifts
    n = count('+', suffix) - count('-', suffix)
    if n > 0:
      for i in range(0,n):
        f = f*self.semitoneFactor
    if n < 0:
      for i in range(0,-n):
        f = f/self.semitoneFactor
        
    return f, root, suffix

  # print dictionary
  def printNoteFreq():
    j = 0
    for N in note:
      print j, N, noteFreq[N]
      j = j + 1
