import math
import heapq
import time
import sys
import multiprocessing
from multiprocessing import Process

MAX = 1000
numSuccessor = 8


def minList(List):
    if len(List)==0:
        return math.inf;
    minValue=List[0].fValue0();
    for i in range(1,len(List)):
        if minValue>List[i].fValue0():
            minValue=List[i].fValue0();
    return minValue;
    
def wayList(Root):
    way=[]
    while(Root is not None):
        way.append(Root)
        Root=Root.parent
    return way

def isBelongTo(i,j,List):
    if i==List[0].x and j==List[0].y:
        return 0
    if i==List[len(List)-1].x and j==List[len(List)-1].y:
        return 1
    for k in range (1,len(List)-1):
        if i==List[k].x and j==List[k].y:
            return 2
    return 3

def writeResult(fileName, way,Map,eps):
    f= open(fileName,"a")
    f.write("Epsilon: %f\n"%eps)
    k=len(way)
    f.write("%d\n"%(k))
    for i in range(len(way)):
        f.write("(%d,%d) "%(way[k-1-i].x,way[k-1-i].y))
    f.write("\n")
    for i in range(len(Map)):
        for j in range(len(Map)):
            if isBelongTo(i,j,way)==0:
                f.write("G ")
            elif isBelongTo(i,j,way)==1:
                f.write("S ")
            elif isBelongTo(i,j,way)==2:
                f.write("x ")
            elif Map[i][j]=="1":
                f.write("o ")
            else:
                f.write("- ")
        f.write("\n")
    f.close()
    
def writeFail(fileName,eps):
    f=open(fileName,"a")
    f.write("Epsilon: %f\n"%eps)
    f.write("No way better\n")
    f.close()
    
def writeResultAStar(fileName, way,Map):
    f= open(fileName,"w")
    k=len(way)
    f.write("%d\n"%(k))
    for i in range(len(way)):
        f.write("(%d,%d) "%(way[k-1-i].x,way[k-1-i].y))
    f.write("\n")
    for i in range(len(Map)):
        for j in range(len(Map)):
            if isBelongTo(i,j,way)==0:
                f.write("G ")
            elif isBelongTo(i,j,way)==1:
                f.write("S ")
            elif isBelongTo(i,j,way)==2:
                f.write("x ")
            elif Map[i][j]=="1":
                f.write("o ")
            else:
                f.write("- ")
        f.write("\n")
    f.close()
    
    
def readFile(fname):
    f=open(fname,"r")
    N=int(f.readline(MAX))

    line=f.readline(MAX)
    ar=line.split(" ")
    Start=Node(int(ar[0]),int(ar[1]),None)
    line = f.readline(MAX)
    ar = line.split(" ")
    Goal = Node(int(ar[0]), int(ar[1]), None)

    Map=[]
    for i in range(N):
        line=f.readline(MAX)
        m=line.split(" ")
        if m[len(m)-1]=="1\n":
            m[len(m)-1]="1"
        else:
            m[len(m)-1]="0"
        Map.append(m)
    f.close()
    return Start,Goal,Map  


class Node:
    eps=1.0;
    Goalxy=[0,0];
    ID=0;
    def __init__(self,x,y,parent):
        self.x=x;
        self.y=y;
        self.parent=parent;
        self.gValue=math.inf;
    
    def fValue0(self):
        return self.gValue+self.heuristic();
        
    def __lt__(self,other):
        return self.fValue()<other.fValue();
    
    def __le__(self,other):
        return self.fValue()<=other.fValue();
    
    def __eq__(self,other):
        return self.fValue()==other.fValue();
    
    def __gt__(self,other):
        return not self.__le__(other);
    
    def __ge__(self,other):
        return not self.__lt__(other);
        
    def heuristic(self):
        if Node.ID==0:
            return max(abs(Node.Goalxy[0]-self.x),abs(Node.Goalxy[1]-self.y));
        elif Node.ID==1:
            return math.sqrt((Node.Goalxy[0]-self.x)*(Node.Goalxy[0]-self.x)+(Node.Goalxy[1]-self.y)*(Node.Goalxy[1]-self.y));
        else:
            return abs(Node.Goalxy[0]-self.x),abs(Node.Goalxy[1]-self.y);
        
    def fValue(self):
        return self.gValue+Node.eps*self.heuristic();
    
    def isSamePosition(self,other):
        return self.x==other.x and self.y==other.y;
    
    def isVisited(self,List):
        for i in range (len(List)):
            if self.isSamePosition(List[i]):
                self.gValue=List[i].gValue;
                return True;
        return False;
    
    def positionVisited(self,List):
        for i in range(len(List)):
            if self.isSamePosition(List[i]):
                return i
        return -1

def AStar(Map,Start,Goal,fileName,ID):
    if Start.isSamePosition(Goal):
        way=wayList(Start)
        writeResult(fileName,way,Map)
        return
    Node.ID=ID
    Node.Goalxy[0]=Goal.x;
    Node.Goalxy[1]=Goal.y;
    N=len(Map);
    Open=[];
    Closed=[];
    Start.gValue=0;
    heapq.heappush(Open,Start);
    Successor=[[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]];
    while(Goal.positionVisited(Open) ==-1 and len(Open)>0):
        s=heapq.heappop(Open);
        if (s.positionVisited(Closed) ==-1):
            Closed.append(s);
        for i in range(numSuccessor):
            x=s.x+Successor[i][0];
            y=s.y+Successor[i][1];
            if x>=0 and x<N and y>=0 and y<N and Map[x][y]!="1":
                s1=Node(x,y,s);
                if s1.isVisited(Open) is False and s1.isVisited(Closed) is False:
                    s1.gValue=math.inf;
                if s1.gValue>s.gValue+1:
                    s1.gValue=s.gValue+1;
                    if s1.positionVisited(Closed) ==-1:
                        heapq.heappush(Open,s1);
                if Goal.isSamePosition(s1):
                    Goal=s1;
                    break;
    if Goal.gValue==math.inf:
        f=open(fileName,"w");
        f.write("-1");
        f.close();
    else:
        way=wayList(Goal);
        writeResultAStar(fileName,way,Map);  

def improvePath(Map,Start,Goal,eps,Open,Closed,Incons):
    if len(Open)==0:
        return False;
    N=len(Map);
    Successor=[[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]];
    while Goal>Open[0] :
        s=heapq.heappop(Open);
        if s.isVisited(Closed) is False:
            Closed.append(s);
        for i in range(numSuccessor):
            x=s.x+Successor[i][0];
            y=s.y+Successor[i][1];
            if x>=0 and x<N and y>=0 and y<N and Map[x][y]!="1":
                s1=Node(x,y,s);
                if s1.isVisited(Open) is False and s1.isVisited(Closed) is False and s1.isVisited(Incons) is False:
                    s1.gValue=math.inf;               
                if s1.gValue>s.gValue+1:
                    s1.gValue=s.gValue+1;
                    if s1.positionVisited(Closed) ==-1:
                        k1=s1.positionVisited(Open)
                        if k1==-1:
                            heapq.heappush(Open,s1);
                        else:
                            del Open[k1]
                            heapq.heapify(Open)
                            heapq.heappush(Open,s1)
                    else:
                        k2=s1.positionVisited(Incons)
                        if k2==-1:
                            Incons.append(s1);
                        else:
                            del Incons[k2]
                            Incons.append(s1)
                if Goal.isSamePosition(s1):
                        Goal.gValue=s1.gValue;
                        Closed.append(s1);
        if len(Open)==0:
            break;
    if (len(Closed)==0 or Goal.isSamePosition(Closed[len(Closed)-1])is False):
        return False;
    return True;
    
def ARAStar(Map,Start,Goal,fileName,ID,eps,deltaEps):
    if Start.isSamePosition(Goal):
        return Start;
    Node.eps=eps;
    Node.ID=ID;
    Node.Goalxy[0]=Goal.x;
    Node.Goalxy[1]=Goal.y;
    Goal.gValue=math.inf;
    Start.gValue=0;
    Open=[];
    Closed=[];
    Incons=[];
    heapq.heappush(Open,Start);
    if improvePath(Map,Start,Goal,eps,Open,Closed,Incons):
        way=wayList(Closed[len(Closed)-1])
        writeResult(fileName,way,Map,eps)
    else:
        writeFail(fileName,eps)
        return;
    if (len(Open)==0 and len(Incons)==0):
        eps1=eps;
    else: 
        eps1=min(eps,Goal.gValue/min(minList(Open),minList(Incons)));
    while(eps1>1):
        eps=eps-deltaEps;
        Node.eps=eps;
        tempList=Open;
        Open=[];
        for i in range(len(Incons)):
            heapq.heappush(Open,Incons[i]);
        for i in range(len(tempList)):
            heapq.heappush(Open,tempList[i]);
        del Incons[:];
        del Closed[:];
        if improvePath(Map,Start,Goal,eps,Open,Closed,Incons):
            way=wayList(Closed[len(Closed)-1])
            writeResult(fileName,way,Map,eps)
        else:
            writeFail(fileName,eps)
        if (len(Open)==0 and len(Incons)==0):
            eps1=eps;
        else: 
            eps1=min(eps,Goal.gValue/min(minList(Open),minList(Incons)));
        
 
def main(argv):
    Start, Goal, Map=readFile(argv[1])
    if len(argv)>4:
        startTime=time.time();
        actionProcess=Process(target=ARAStar,args=(Map,Start,Goal,argv[2],int(argv[3]),float(argv[4]),float(argv[5])));
        actionProcess.start();
        actionProcess.join(timeout=float(argv[6])/1000);
        actionProcess.terminate();
        endTime=time.time();
        print("Time: ",(endTime-startTime)*1000," ms" );
    else:
        AStar(Map,Start,Goal,argv[2],int(argv[3]))
                   
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main(sys.argv[:])
    
