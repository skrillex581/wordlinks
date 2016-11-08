#!/usr/bin/env python
import cPickle as pickle
import re
import os
from app.utils.spgraph import Graph as dGraph, PathNotFound
from app.models import Word


#dictionary supports TEARS->SEARS->STARS->STARE->STALE->STILE->SMILE
class Graph(object):
    def __init__(self,location):
        self._nodes = {} #dict of words
        self._g = dGraph()
        self._location = location
        print self._location
    def GetFileName(self,length):
        return "{0}_{1}.pik".format(self._location,length)
    def CreateEdge(self, s,e):
        if (not self._nodes[s].__contains__(e)) and e!=s:
            self._nodes[s].append(e)
            self._g.AddEdge(s,e,1)
    def BuildMatchingsFromDatabase(self,length):
        if os.path.isfile(self.GetFileName(length)):
            self._g = pickle.load(open(self.GetFileName(length),"rb"))    
            return 	
        print "BuildMatchingsFromDatabase for length: {0}".format(length)	
        words = Word.query.filter_by(wordlength=length)
        self._contents = ""
        for w in words:
            self._contents += (" " + w.word.lower()) #build in-memory map of all words	
            self.CreateNode(w.word.lower())    
        
        keys = self._nodes.keys()        
        for w in keys:			
            keylen = len(w)
            for i in range(len(w)):
                pattern = list(w) #turn into set
                pattern[i]= "[a-z]{1}"
                pattern = "".join(pattern) #turn into string
                words = re.findall(pattern, self._contents) # Word.query.filter_by(wordlength=keylen).filter_by(Word.word.like(pattern)).all()
                for j in words:                    
                    self.CreateEdge(w,j)        
        for j in self._nodes:
            self._g.AddVertex(j)
            for i in self._nodes[j]:
                self._g.AddEdge(j,i)        
        pickle.dump(self._g,open(self.GetFileName(length),"wb"))
        self._contents = ""  
    def CreateNode(self, w):
        if not self._nodes.has_key(w):
            self._nodes[w] = []
            self._g.AddVertex(w)
    def FindLadder(self, s, d):        
        return self._g.FindShortestPath(s,d)
        

