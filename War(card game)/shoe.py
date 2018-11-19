## @file shoe.py
## @stores a class representing a card shoe

import numpy as np;
import numpy.random as nr;


class shoe(object):
    SUITS = ["C","H","S","D"] ;
    CNUM = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"];
    CPERSUIT = 13;
    CARDVAL = np.array(range(CPERSUIT));
    DECKSIZE = 52;
    
    def __init__(self, nDeck=1):
        self._nDeck = nDeck;
        self._stack = np.repeat(map(lambda x:x+1, range(self.CPERSUIT)), nDeck*4);
        self._stack1 = [];
        self._stack2 = [];
        
    def shuffle(self):
        if len(self._stack) > 0:
            nr.shuffle(self._stack);
            self._stack1 = self._stack[range(self.DECKSIZE/2)];
            self._stack2 = self._stack[self.DECKSIZE/2:];
    
    def isEmpty1(self):
        return len(self._stack1)==0;
        
    def isEmpty2(self):
        return len(self._stack2)==0;        
    
    def getNext1(self,num=1):
        card = self._stack1[:num];
        self._stack1 = self._stack1[num:];
        return card;
    
    def getNext2(self,num=1):
        card = self._stack2[:num];
        self._stack2 = self._stack2[num:];
        return card;
            
    def getCard1(self, win):
        self._stack1 = np.append(self._stack1, win);
    
    def getCard2(self, win):
        self._stack2 = np.append(self._stack2, win);      
        
    def returnCard1(self, back):
        self._stack1 = np.append(back, self._stack1);
    
    def returnCard2(self, back):
        self._stack2 = np.append(back, self._stack2);
        
    def combineCard1(self, set1, set2):
        pool = np.append(set1,set2);
        return pool;
    
    def combineCard2(self, set1, set2):
        pool = np.append(set1,set2);
        return pool;
            
    def getNum1(self):
        return(len(self._stack1));
        
    def getNum2(self):
        return(len(self._stack2));              
        
                
myshoe = shoe(1)
myshoe._stack
myshoe._stack1
myshoe._stack2
myshoe.shuffle()