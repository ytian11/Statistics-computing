import numpy as np;
import numpy.random as nr;
import copy;
from shoe import shoe;
from matplotlib import pyplot as plt;

class War(object):
    def __init__(self,shoe):
        self._shoe = shoe;
        self._pool1 = [];
        self._pool2 = [];
        self._h1 = [];
        self._h2 = [];
        #self._n1 = self._shoe.getNum1();
        #self._n2 = self._shoe.getNum1();
        self._round = 1;
    
    def run(self):
        winner = [1,2];
        while True:
            self._h1 = self._shoe.getNext1();
            self._h2 = self._shoe.getNext2();
            
            if self._h1[0] > self._h2[0]:
                self._shoe.getCard1(np.append(np.append(self._h1,self._pool1),np.append(self._h2,self._pool2)));
                self._pool1 = [];
                self._pool2 = [];
                if self._shoe.isEmpty1() or self._shoe.isEmpty2():
                    break;
            if self._h1[0] < self._h2[0]:
                self._shoe.getCard2(np.append(np.append(self._h1,self._pool1),np.append(self._h2,self._pool2)));
                self._pool1 = [];
                self._pool2 = [];
                if self._shoe.isEmpty1() or self._shoe.isEmpty2():
                    break;
            if self._h1[0] == self._h2[0]:
                act = map(lambda x:(x>0.5),nr.rand(1));
                if act[0]==0:
                    self._pool1 = np.append(self._pool1,self._shoe.combineCard1(self._h1,self._shoe.getNext1(2)));
                    self._shoe.returnCard1(self._pool1[len(self._pool1)-1]);
                    self._pool1 = self._pool1[:(len(self._pool1)-1)];
                    
                    self._pool2 = np.append(self._pool2,self._shoe.combineCard2(self._h2,self._shoe.getNext2(2)));
                    self._shoe.returnCard2(self._pool2[len(self._pool2)-1]);
                    self._pool2 = self._pool2[:(len(self._pool2)-1)];
                                                      
                if act[0]==1:
                    self._pool1 = np.append(self._pool1,self._shoe.combineCard1(self._h1,self._shoe.getNext1(4)));
                    self._shoe.returnCard1(self._pool1[len(self._pool1)-1]);
                    self._pool1 = self._pool1[:(len(self._pool1)-1)];
                    
                    self._pool2 = np.append(self._pool2,self._shoe.combineCard2(self._h2,self._shoe.getNext2(4)));
                    self._shoe.returnCard2(self._pool2[len(self._pool2)-1]);
                    self._pool2 = self._pool2[:(len(self._pool2)-1)];  
            
            self._round += 1;
            if self._round > 10000*self._shoe._nDeck:
                break;                                                  
        print "The winner is Player %s, at Round %s" % (winner[self._shoe.isEmpty1()],self._round);                 
        return self._round;


## Example: simulation replicates 100 times
def simulation(nDeck=1,R=100):
    myshoe = shoe(nDeck);
    rounds = [0]*R;
    for i in range(R):
        myshoe.shuffle();
        war = War(myshoe);
        rounds[i] = war.run();
    roundnew = [c for c in rounds if c<10000*nDeck];
    plt.hist(roundnew,range=[0,max(roundnew)],facecolor="red",normed=True);
    plt.xlabel("Rounds");
    plt.ylabel("Density");
    plt.show();

if __name__ == "__main__":
    simulation(1);
    plt.close();
    simulation(2);