import re;
import sys;
import numpy.random as nr;
import numpy as np;
import urllib;
import copy;
import xml.etree.ElementTree as	ET;
import pickle

pth = "./Scrabble/"
acc = open(pth + "scrabble words distribution.txt");

## the crads pool that contains all cards with the scrabble words distribution
wordsPool = [];

for line in acc:
    wordsPool.append(line[0]);

nr.shuffle(wordsPool)
 
cardPool = list(''.join(wordsPool).lower())

## try 40 cards first

#cardPool = cardPool[1:40]



## with the current cards, get more new cards so that the total number of cards
## is 7
def getCard(cur):
    if len(cur)<7:
        index = min(7-len(cur),len(cardPool));
        for i in range(index):
            cur+=cardPool.pop();
    return cur;

#cur = ['A','C','D']
#getCard(cur)

## Define the letter score:
letterscores = {"a":1,"e":1,"i":1,"o":1,"n":1,"r":1,"t":1,"l":1,"s":1,"u":1,
          "d":2,"g":2,"b":3,"c":3,"m":3,"p":3,
          "f":4,"h":4,"v":4,"w":4,"y":4,
          "k":5,"j":8,"x":8,"q":10,"z":10}

## Define the chessboard
## Define the Double letter score X2LS, Triple letter score X3LS
## Double word score X2WS, Triple word score X3WS

X2LS = [[0,3],[0,11],
        [2,6],[2,8],
        [3,0],[3,7],[3,14],
        [6,2],[6,6],[6,8],[6,12],
        [7,3],[7,11],
        [8,2],[8,6],[8,8],[8,12],
        [11,0],[11,7],[11,14],
        [12,7],[12,8],
        [14,3],[14,11]]

X3LS = [[1,5],[1,9],
        [5,1],[5,5],[5,9],[5,13],
        [9,1],[9,5],[9,9],[9,13],
        [13,5],[13,9]]
        
X2WS = [[1,1],[1,13],
        [2,2],[2,12],
        [3,3],[3,11],
        [4,4],[4,10],
        [10,4],[10,10],
        [11,3],[11,11],
        [12,2],[12,12],
        [13,1],[13,13]]
        
X3WS = [[0,0],[0,7],[0,14],
        [7,0],[7,14],
        [14,0],[14,7],[14,14]]

## Define the counting rule
## index is the coordinate, letter is the chosen cards
def countScore(index,letter):
    score = 0;
    for i in range(len(letter)):
        if index[i] in X2LS:
            score += letterscores[letter[i]]*2;
        if index[i] in X3LS:
            score += letterscores[letter[i]]*3;
        else:
            score += letterscores[letter[i]];
   
    for i in range(len(letter)):
        if index[i] in X2WS:
            score *= 2;
        if index[i] in X3WS:
            score *= 3;
   
    return score; 
            
  
##
#letter=['A','I','R']
#index=[[1,1],[1,2],[1,3]] 
#countScore(index,letter)   

      
            
## Best policy
pth = "./Scrabble/"
f = open(pth + "scrabble.txt","rb");

wordPool = []; 
for line in f:
    line = line.strip();
    wordPool.append(line);
    f.close;
 
#chessBoard = np.chararray((15, 15))
#chessBoard[:] = '0'
  
def checkRow(curLine,curLoc,curLetter,candidate,curChessBoard):
    # 1. Check the length:
    ## rewrite!!! bug!!!
    front = curLoc;
    #back = 15-curLoc-len(curLetter);
    coordinate = dict();
    for word in candidate:
        coordinate[(word,curLine,curLoc,curLetter)] = [];
        ind = [i for i in range(len(word)) if word[i]==curLetter[0]];
        equal = [1]*len(ind);
        for i in ind:   
            if i>front or len(word)+curLoc-i-1>14:
                equal[ind.index(i)] = 0;  
            #if i<=front and len(word)-word.index(curLetter[len(curLetter)-1])-1<=back:
            if i<=front and len(word)+curLoc-i-1<=14:
                newLine = ['0']*15;
                newLine[(front-i):(len(word)+front-i)] = list(word); 
                for j in range(15):
                    if curChessBoard[curLine][j]!='0' and curChessBoard[curLine][j]!=newLine[j]:
                        equal[ind.index(i)] = 0;
                if word == curLetter:
                    equal[ind.index(i)] = 0;
            if equal[ind.index(i)] == 1:
                coordinate[(word,curLine,curLoc,curLetter)].append(range(front-i,(len(word)+front-i)));
    for i in coordinate.keys():
        if coordinate[i] == []:
            coordinate.pop(i);    
    return coordinate; ## only returns the col number but not the line number
    
    
def checkCol(curLine,curLoc,curLetter,coordinate,curChessBoard):
    candidateIndex = dict();
    for col in coordinate.keys():
        candidateIndex[col] = [];
        
        if len(coordinate[col])==1:
            for l in range(len(col[0])):
                tempBoard = copy.deepcopy(curChessBoard);
                tempBoard[curLine,coordinate[col][0][l]] = col[0][l];
            #tempBoard[curLine,coordinate[col]] = list(col[0]);
            for j in coordinate[col][0]:
                coorespond = 1;
                temp = ''.join(tempBoard[:,j]);
                colletter = re.split('0+',temp);
                colletter = [x for x in colletter if x != ''] ;
                for k in colletter:
                    if k not in wordPool:
                        coorespond = 0;
                if coorespond == 1:
                    candidateIndex[col].append([[curLine,i] for i in coordinate[col][0]]);            
            
        elif len(coordinate[col])>1:
            tempBoard = copy.deepcopy(curChessBoard);
            for policy in coordinate[col]:
                for l in range(len(col[0])):
                    tempBoard[curLine,policy[l]] = col[0][l];
                    #temp = list(''.join(tempBoard[curLine]));
                    #temp[policy[0]:policy[len(policy)-1]+1] = list(col[0]);
                    #tempBoard.replace(tempBoard[curLine],temp);
                for j in policy:
                    coorespond = 1;
                    temp = ''.join(tempBoard[:,j]);
                    colletter = re.split('0+',temp);
                    colletter = [x for x in colletter if x != ''] ;
                    for k in colletter:
                        if k not in wordPool:
                            coorespond = 0;
                    if coorespond == 1:
                        candidateIndex[col].append([[curLine,i] for i in policy]);
                        
    for i in candidateIndex.keys():
        if candidateIndex[i] == []:
            candidateIndex.pop(i);    
    return candidateIndex;
                    

def bestPolicy(curChessBoard,handcard):
    allScore = dict();
    finScore = [];
    allInd = dict();
    for i in range(15):
        if sum(curChessBoard[i].count('0'))<15:
            temp = ''.join(curChessBoard[i]);
            rowletter = re.split('0+',temp);
            rowletter = [x for x in rowletter if x != ''];
            temp = '0'+temp+'0';
            rowletter = list(set(rowletter));
            
            for j in rowletter:
                allScore_row = dict();
                finScore_row = [];
                #ind = [x for x in range(len(temp)-len(j)) if j==temp[x:(x+len(j))]];## startpoint of the given words
                ind = [x for x in range(len(temp)) if re.match('0'+j+'0',temp[x:])];
                for k in ind:
                    potential = [];
                    candidate = [];
                    for line in wordPool:
                        if re.search(j,line,re.IGNORECASE):
                            potential.append(line);
                    #f.close;
                    for line in potential:
                        temp = line.replace(j,'');
                        con1 = all([True if temp.count(item)<=handcard.count(item) else False for item in temp]);
                        con2 = set(temp)<=set(handcard);
                        if con1 and con2 and line!=j:
                            candidate.append(line);
                
                    cor_temp = checkRow(i,k,j,candidate,curChessBoard);      
                    ind_temp = checkCol(i,k,j,cor_temp,curChessBoard);
                    
                    #cor_temp = [cor_temp[ii] for ii in cor_temp.keys() if ii[0]!=ii[3]]; 
                    #ind_temp = [ind_temp[ii] for ii in ind_temp.keys() if ii[0]==ii[3]];
                    
                    allInd.update(ind_temp);
                
                    allScore_pol = dict();
                    finScore_pol = [];
                    
                    for l in ind_temp.keys():
                        allScore_pol[l] = [];
                        #if len(ind_temp[i])>1:
                        for m in ind_temp[l]:
                            sc = countScore(m,l[0]);
                            allScore_pol[l].append([sc]);
                            finScore_pol.append(sc);
                       # if len(ind_temp[i])<=1:
                            #    sc = countScore(j,ind_temp[i]);
                            #    allScore_pol[i].append = [sc];
                            #    finScore_pol.append(sc);                                    
                    allScore_row.update(allScore_pol);
                    finScore_row += finScore_pol;
                allScore.update(allScore_row);
                finScore += finScore_row;
    
    ## find the best policy
    if finScore !=[]:
        mx = max(finScore);
        TF = [True if [mx] in allScore[temp] else False for temp in allScore.keys()];
        temp1 = allScore.keys()[TF.index(True)];
        temp2 = allScore[temp1].index([mx]);
    
    ## update chessboard
        ind = allInd[temp1][temp2];
        for k in range(len(ind)):
            curChessBoard[ind[k][0],ind[k][1]] = temp1[0][k];       
    elif finScore == []:
        mx = 0;
        temp1 = ('','','','');
            
    return {"board":curChessBoard,"score":mx,"words":temp1[0],"curLetter":temp1[3]};
            
    
        
def r2c(a):
    b = copy.deepcopy(a);
    for z1 in range(shape(a)[0]):
        for z2 in range(shape(a)[1]):
            b[z1,z2] = a[z2,shape(a)[0]-z1-1];  
    return b;    
    
def c2r(a):
    b = copy.deepcopy(a);
    for z1 in range(shape(a)[0]):
        for z2 in range(shape(a)[1]):
            b[z1,z2] = a[shape(a)[0]-z2-1,z1];  
    return b;                                     
                                                                                        
   
## Computer to computer simulation                                                             
def c2c():
    chessBoard = np.chararray((15, 15));
    chessBoard[:] = '0';
    cur = '';
    p1_score = 0;
    p2_score = 0;
    rounds = 1;
        
    ## Step 1, use the center point
    firstCards = [];
    res = dict();
    ind = dict();
    handcard = getCard(cur);
    for line in wordPool:
        con1 = all([True if line.count(item)<=handcard.count(item) else False for item in line]);
        con2 = set(line)<=set(handcard);
        if con1 and con2:
            firstCards.append(line);
    maxScore=0;

    for i in firstCards:
        if len(i)%2==0:
            coord = range(7-len(i)/2,7+len(i)/2);
        elif len(i)%2!=0:
            coord = range(7-len(i)/2,8+len(i)/2);
        ind[i] = [[7,x] for x in coord];
        res[i] = countScore(ind[i],i);
        if res[i]>maxScore:
            maxScore = res[i];
    choose = [x for x in res.keys() if res[x]==maxScore][0];
    
    ## Update chessBoard, score and current cards
    p1_score += maxScore;
    for k in range(len(choose)):
        chessBoard[ind[choose][k][0],ind[choose][k][1]] = choose[k];
    temp = choose;
    handcard = list(handcard);
    for i in range(len(temp)):
        handcard[handcard.index(temp[i])] = '';
    cur = ''.join(handcard);
    
    rounds += 1;
    
    while True:
        if cardPool == []:
            break;
        handcard = getCard(cur);
        curCB = copy.deepcopy(chessBoard);
        res_queue = bestPolicy(r2c(curCB),handcard);
        curCB = copy.deepcopy(chessBoard);
        res_line = bestPolicy(curCB,handcard);
         
        if res_queue["score"]==0 and res_line["score"]==0:
            break;   
        elif res_queue["score"]>res_line["score"]:
            chessBoard = c2r(res_queue["board"]);
            temp = res_queue["words"].replace(res_queue["curLetter"],'');
            handcard = list(handcard);
            for i in range(len(temp)):
                handcard[handcard.index(temp[i])] = '';
            cur = ''.join(handcard);
            if rounds%2==0:
                p2_score += res_line["score"];
            else:
                p1_score += res_line["score"];
        else:
            chessBoard = res_line["board"];
            temp = res_line["words"].replace(res_line["curLetter"],'');
            handcard = list(handcard);
            for i in range(len(temp)):
                handcard[handcard.index(temp[i])] = '';
            cur = ''.join(handcard);
            if rounds%2==0:
                p2_score += res_queue["score"];
            else:
                p1_score += res_queue["score"];    
        rounds += 1;
    
    print 'Rounds:'+str(rounds)+';Computer 1:'+str(p1_score)+';Computer 2:'+str(p2_score);
    print 'Current ChessBoard:\n';
    print chessBoard;
        
## Person to computer interaction                                                             

## Check if the current coordinate include center
def centerCheck(x):
    if [7,7] not in x:
        print 'In first round, the coordinates must include [7,7]! Type again:';
        return 0;
    else:
        return 1;

## Check if the word coorespond to each column
def colCheck(x_word,x_coordinate,curChessBoard):
    ## Check if the words is suitable in column
    tempBoard = copy.deepcopy(curChessBoard);
    for l in range(len(x_word)):
        tempBoard[x_coordinate[l][0],x_coordinate[l][1]] = x_word[l];
    x_column = [num[1] for num in x_coordinate];    
    for j in x_column:
        coorespond = 1;
        temp = ''.join(tempBoard[:,j]);
        colletter = re.split('0+',temp);
        colletter = [x for x in colletter if x != ''] ;
        for k in colletter:
            if k not in wordPool:
                coorespond = 0;
	
    return coorespond;
 
	
	                                                             
def p2c(chessBoard,cur,p1_score,p2_score,rounds):
    while True:
        if cardPool == []:
            break;
        ## Step 1, use the center point
        handcard = getCard(cur);
        print 'Current handcards:\n'+handcard;
        print 'Current ChessBoard:\n';
        print chessBoard;
        
        if rounds%2 == 1:
        ## Player's round
	   while True:
	       print 'Plese type in the word:';
	       p_word = raw_input();
	       print 'Plese type in the coordinate:(In the form [[x1,y1],[x2,y2]])';
	       p_coordinate = raw_input();
	       p_coordinate = eval(p_coordinate);
        
	       if rounds == 1 and centerCheck(p_coordinate):
	           break;
	       if colCheck(p_word,p_coordinate,chessBoard):
	           break;
	           	       
	   for l in range(len(p_word)):
	       chessBoard[p_coordinate[l][0],p_coordinate[l][1]] = p_word[l];
	   p1_score += countScore(p_coordinate,p_word);  		
	   handcard = list(handcard);
	   for i in range(len(p_word)):
	       handcard[handcard.index(p_word[i])] = '';
	       cur = ''.join(handcard);
        if rounds%2 == 0:
	    #handcard = getCard(cur);
	    curCB = copy.deepcopy(chessBoard);
	    res_queue = bestPolicy(r2c(curCB),handcard);
	    curCB = copy.deepcopy(chessBoard);
	    res_line = bestPolicy(curCB,handcard);
	    if res_queue["score"]>res_line["score"]:
	        chessBoard = c2r(res_queue["board"]);
	        temp = res_queue["words"].replace(res_queue["curLetter"],'');
	        handcard = list(handcard);
	        for i in range(len(temp)):
	            handcard[handcard.index(temp[i])] = '';
	            cur = ''.join(handcard);
	        p2_score += res_queue["score"];
	    else:
	        chessBoard = res_line["board"];
	        temp = res_line["words"].replace(res_line["curLetter"],'');
	        handcard = list(handcard);
	        for i in range(len(temp)):
	            handcard[handcard.index(temp[i])] = '';
	            cur = ''.join(handcard);
	            p2_score += res_line["score"];
   
        rounds += 1;
        print 'Rounds:'+str(rounds)+';You:'+str(p1_score)+';Computer:'+str(p2_score);
        print 'Current ChessBoard:\n';
        print chessBoard;
        print 'Do you want to end the game?(Y:Yes,N:No)';
        end = raw_input();
        if end == 'Y':
            root = ET.Element("savepoint")
            ET.SubElement(root, "score1", name="Player").text = str(p1_score);
            ET.SubElement(root, "score2", name="Computer").text = str(p2_score);
            ET.SubElement(root, "round", name="Round").text = str(rounds);
            ET.SubElement(root, "board", name="Board").text = chessBoard.tostring();
            ET.SubElement(root, "cur", name="CurrentCards").text = cur;
            tree = ET.ElementTree(root);
            #sp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            #filename = "".join(sp)+".xml"
            tree.write("savepoint.xml");
            break;


   	
   	
   	
## Example
## Computer to computer simulation:
chessBoard = np.chararray((15, 15));
chessBoard[:] = '0';
cur = '';
p1_score = 0;
p2_score = 0;
rounds = 1;
c2c() ## Around 2 mins




## Person to computer:
chessBoard = np.chararray((15, 15));
chessBoard[:] = '0';
cur = '';
p1_score = 0;
p2_score = 0;
rounds = 1;
p2c(chessBoard,cur,p1_score,p2_score,rounds);

## Read from save file
savepoint = ET.parse('savepoint.xml');
node = savepoint.getiterator();
p1_score = int(node[1].text.rstrip());
p2_score = int(node[2].text.rstrip());
rounds = int(node[3].text.rstrip());
cur = node[5].text.rstrip().replace("'","");
temp = node[4].text.rstrip().replace("'","");
chessBoard = np.chararray((15, 15));
chessBoard[:] = '0';
for m in range(15):
    for n in range(15):
        chessBoard[m,n] = temp[m*15+n];

p2c(chessBoard,cur,p1_score,p2_score,rounds)
          
                    