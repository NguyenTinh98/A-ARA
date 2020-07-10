from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

import math
import heapq
import time
import random

MAX = 1000
numSuccessor = 8
deltaEps = 0.5
sleepTime=0.001

Color={"Map":"#e0e0e0","Block":"#2b2b2b","Start":"#ff80ff","Goal":"#ffff00","Open":"#ffffff","Incons":"#8484ff","Way":"#ff0000","Last way":"#00ff40"}
Heuristic={"Max(dx,dy)":0,"Euclid":1,"Manhattan":2}

def minList(List):
    if len(List)==0:
        return math.inf;
    minValue=List[0].fValue0();
    for i in range(1,len(List)):
        if minValue>List[i].fValue0():
            minValue=List[i].fValue0();
    return minValue;
   
class Node:
    eps=1;
    Goalxy=[0,0];
    id=0;
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
        if Node.id==0:
            return max(abs(Node.Goalxy[0]-self.x),abs(Node.Goalxy[1]-self.y));
        elif Node.id==1:
            return math.sqrt((Node.Goalxy[0]-self.x)*(Node.Goalxy[0]-self.x)+(Node.Goalxy[1]-self.y)*(Node.Goalxy[1]-self.y))
        else:
            return abs(Node.Goalxy[0]-self.x)+abs(Node.Goalxy[1]-self.y)
    
    def fValue(self):
        return self.gValue+Node.eps*self.heuristic();
    
    def isVisited(self,List):
        for i in range (len(List)):
            if self.x==List[i].x and self.y==List[i].y:
                self.gValue=List[i].gValue;
                return True;
        return False;
    def isSamePosition(self,other):
        return self.x==other.x and self.y==other.y;
    
    def positionVisited(self,List):
        for i in range(len(List)):
            if self.isSamePosition(List[i]):
                return i
        return -1
class GUI(Frame):
     def __init__(self,size=30):
        self.Map=[]
        self.Feature=[]
        self.id=0
        self.gui_map=0
        self.size=size
        self.filepath=0
        self.button_Run=0
        self.button_Renew=0
        self.button_Setup=0
        self.button_Setup2=0
        self.button_Start=0
        self.button_Goal=0
        self.button_Read=0
        self.button_Save=0
        self.button_Random=0
        self.text_N=0
        self.combo_heu=0
        self.combo_algo=0
        self.text_eps=0
        self.button_Maze=0
        self.result=0
        self.Start=Node(0,0,None)
        self.Goal=Node(self.size-1,self.size-1,None)
        self.way=[]
        super().__init__()
        
     def program(self,option=0):
         self.initUI(option)
         self.master.mainloop()
     def draw(self,x,y,c):
         self.gui_map.create_rectangle(10*(x+1)+10, 10*(y+1)+10, 20+10*(x+1), 20+10*(y+1),outline="#000", fill=c)

     def onLeftDrag(self,event):
        #self.change(event)
        x=int((event.x-20)/10)
        y=int((event.y-20)/10)
        if x>-1 and y>-1 and x<len(self.Map) and y<len(self.Map) and  self.Feature[y][x]==0:
            if self.Map[y][x]==0:
                self.draw(x,y,Color["Block"])
                self.Map[y][x]=1
            if x<len(self.Map) and y+1<len(self.Map) and self.Map[y+1][x]==0 and self.Feature[y+1][x]==0:
                self.draw(x,y+1,Color["Block"])
                self.Map[y+1][x]=1
     def onleftPress(self,event):
         
         x=int((event.x-20)/10)
         y=int((event.y-20)/10)
         
         if x>-1 and y>-1 and x<len(self.Map) and y<len(self.Map) and  self.Feature[y][x]==0:
             if self.Map[y][x]==0:
                 self.draw(x,y,Color["Block"])
                 self.Map[y][x]=1
             else:
                 self.draw(x,y,Color["Map"])
                 self.Map[y][x]=0
     def initUI(self,option=0):
         s="{0}x{1}+0+0".format(self.size*10+270,self.size*10+80)
         self.master.geometry(s)
         self.master.title("AStar")
         self.pack(fill=BOTH, expand=1)
        
         if option==0:
             for i in range(self.size):
                 m=[]
                 for j in range(self.size):
                     m.append(0)
                 self.Map.append(m)

         canvas = Canvas(self)
         for i in range(self.size):
                 m=[]
                 for j in range(self.size):
                     m.append(0)
                 self.Feature.append(m)
         self.gui_map=canvas
         for i in range(self.size):
             for j in range(self.size):
                 t=Color["Map"]
                 if self.Map[i][j]==1:
                     t=Color["Block"]
                 self.draw(j,i,t)
         self.draw(self.Start.y,self.Start.x,Color["Start"])
         self.draw(self.Goal.y,self.Goal.x,Color["Goal"])

         self.Feature[self.Start.x][self.Start.y]=1
         self.Feature[self.Goal.x][self.Goal.y]=1
         
         self.gui_map.pack(fill=BOTH, expand=1)
         self.gui_map.bind('<B1-Motion>',self.onLeftDrag)
         self.gui_map.bind('<Button-1>',self.onleftPress)
        
         Label(self.master,text="Size NxN").place(x=self.size*10+30,y=20)
         #Label(self.master,text="N").place(x=self.size*10+30,y=40)
         Label(self.master,text="Point").place(x=self.size*10+30,y=140)
         Label(self.master,text="Option").place(x=self.size*10+30,y=190)
         Label(self.master,text="Result").place(x=self.size*10+30,y=280)
         Label(self.master,text="Heuristic").place(x=self.size*10+30,y=100)
         Label(self.master,text="Algorithm").place(x=self.size*10+150,y=100)
         Label(self.master,text="Epsilon").place(x=self.size*10+30,y=60)

         self.result=Label(self.master,text="")
         self.result.pack()
         self.result.place(x=self.size*10+105,y=307)
         self.text_N=Entry(self.master,width=15)
         self.text_N.pack()
         self.text_N.place(x=self.size*10+30,y=40)
         self.text_eps=Entry(self.master,width=15)
         self.text_eps.pack()
         self.text_eps.place(x=self.size*10+30,y=80)

         self.combo_heu=ttk.Combobox(self.master,values=["Max(dx,dy)","Euclid","Manhattan"],width=10)
         self.combo_heu.place(x=self.size*10+30,y=120)
         self.combo_heu.current(0)
         self.combo_algo=ttk.Combobox(self.master,values=["A*","ARA*"],width=10)
         self.combo_algo.place(x=self.size*10+150,y=120)
         self.combo_algo.current(0)
         #self.combo_heu.pack()

         self.gui_map.create_rectangle(self.size*10+30,305,self.size*10+230,330,outline="#000")

         self.button_Run=Button(self.master,text="Run",width=10,height=1,command=self.Run_Click,relief="groove")
         self.button_Run.pack()
         self.button_Run.place(x=self.size*10+30,y=340)
         self.button_Renew=Button(self.master,text="Reset",width=10,height=1,command=self.Renew_Click,relief="groove")
         self.button_Renew.pack()
         self.button_Renew.place(x=self.size*10+150,y=340)
         self.button_Setup=Button(self.master,text="Set up",width=10,height=1,command=self.Setup_Click,relief="groove")
         self.button_Setup.pack()
         self.button_Setup.place(x=self.size*10+150,y=36)
         self.button_Setup2=Button(self.master,text="Set up",width=10,height=1,command=self.Setup2_Click,relief="groove")
         self.button_Setup2.pack()
         self.button_Setup2.place(x=self.size*10+150,y=76)
         self.button_Start=Button(self.master,text="Start",width=10,height=1,command=self.Start_Click,relief="groove")
         self.button_Start.pack()
         self.button_Start.place(x=self.size*10+30,y=160)
         self.button_Goal=Button(self.master,text="Goal",width=10,height=1,command=self.Goal_Click,relief="groove")
         self.button_Goal.pack()
         self.button_Goal.place(x=self.size*10+150,y=160)
         self.button_Random=Button(self.master,text="Random",width=10,height=1,command=self.Random_Click,relief="groove")
         self.button_Random.pack()
         self.button_Random.place(x=self.size*10+30,y=210)
         self.button_Maze=Button(self.master,text="Maze",width=10,height=1,command=self.Maze_Click,relief="groove")
         self.button_Maze.pack()
         self.button_Maze.place(x=self.size*10+150,y=210)
         self.button_Read=Button(self.master,text="Read file",width=10,height=1,command=self.Read_Click,relief="groove")
         self.button_Read.pack()
         self.button_Read.place(x=self.size*10+30,y=250)
         self.button_Save=Button(self.master,text="Save file",width=10,height=1,command=self.Save_Click,relief="groove")
         self.button_Save.pack()
         self.button_Save.place(x=self.size*10+150,y=250)


     def Random_Click(self):
         M=[]
         for i in range(self.size):
             m=[]
             for j in range(self.size):
                 m.append(0)
             M.append(m)
         n=self.size*self.size/2
         i=0
         self.destroy()
         self=GUI(len(M))
         self.Map=M
         while i<n:
             a=random.randint(0,len(M)-1)
             b=random.randint(0,len(M)-1)
             if self.Map[a][b]==0:
                 self.Map[a][b]=1
                 i=i+1
         while True:
             a=random.randint(0,self.size-1)
             b=random.randint(0,self.size-1)
             if self.Map[a][b]!=1:
                 self.Start.x=a
                 self.Start.y=b
                 break
         while True:
             a=random.randint(0,self.size-1)
             b=random.randint(0,self.size-1)
             if self.Map[a][b]!=1 and  not (self.Start.x==a and self.Start.y==b):
                 self.Goal.x=a
                 self.Goal.y=b
                 break
         self.initUI(1)
     def Maze_Click(self):
         M=maze(self.size)
         self.destroy()
         self=GUI(len(M))
         self.Map=M
         while True:
             a=random.randint(0,self.size-1)
             b=random.randint(0,self.size-1)
             if self.Map[a][b]!=1:
                 self.Start.x=a
                 self.Start.y=b
                 break
         while True:
             a=random.randint(0,self.size-1)
             b=random.randint(0,self.size-1)
             if self.Map[a][b]!=1 and not (self.Start.x==a and self.Start.y==b):
                 self.Goal.x=a
                 self.Goal.y=b
                 break
         self.initUI(1)
         return
     def Run_Click(self):
         self.Renew_Click(1)

         Node.id=Heuristic[self.combo_heu.get()]
         t=self.text_eps.get()
         if(self.combo_algo.get()=="A*"):
             self.id=0
             if t!="":
                 Node.eps=float(t)
             else:
                 Node.eps=1.0
             self.AStar()
         else:
             self.id=1
             if t!="":
                 Node.eps=float(t)
             else:
                 Node.eps=5.0
             self.ARAStar()
         
     def Start_Press(self,event):
         
         x=int((event.x-20)/10)
         y=int((event.y-20)/10)
         if x>-1 and y>-1 and x<len(self.Map) and y<len(self.Map) and self.Feature[y][x]==0:
                 self.draw(self.Start.y,self.Start.x,Color["Map"])
                 self.draw(x,y,Color["Start"])
                 self.Map[y][x]=0
                 self.Feature[self.Start.x][self.Start.y]=0
                 self.Start.x=y
                 self.Start.y=x
                 self.Feature[y][x]=1
         self.gui_map.bind('<Button-1>',self.onleftPress)
     def Start_Click(self):
         self.gui_map.bind('<Button-1>',self.Start_Press)
         
     def Goal_Press(self,event):
         x=int((event.x-20)/10)
         y=int((event.y-20)/10)
         if x>-1 and y>-1 and x<len(self.Map) and y<len(self.Map) and self.Feature[y][x]==0:
                 self.draw(self.Goal.y,self.Goal.x,Color["Map"])
                 self.draw(x,y,Color["Goal"])
                 self.Map[y][x]=0
                 self.Feature[self.Goal.x][self.Goal.y]=0
                 self.Goal.x=y
                 self.Goal.y=x
                 self.Feature[y][x]=1
         self.gui_map.bind('<Button-1>',self.onleftPress)
     def Goal_Click(self):
         self.gui_map.bind('<Button-1>',self.Goal_Press)
     def Renew_Click(self,option=0):
         
         self.way=[]
         self.result.config(text="")
         self.Goal.parent=None

         if option==0:
             self.Map=[]
             for i in range(self.size):
                 m=[]
                 for j in range(self.size):
                     m.append(0)
                 self.Map.append(m)
         for i in range(self.size):
             for j in range(self.size):
                 self.Feature[i][j]=0
         self.Feature[self.Start.x][self.Start.y]=1
         self.Feature[self.Goal.x][self.Goal.y]=1
        
         for i in range(self.size):
             for j in range(self.size):
                 t=Color["Map"]
                 if self.Map[i][j]==1:
                     t=Color["Block"]
                 self.draw(j,i,t)
        
         self.draw(self.Start.y,self.Start.x,Color["Start"])
         self.draw(self.Goal.y,self.Goal.x,Color["Goal"])
         #self.gui_map.update()
     def Setup_Click(self):
             s=0
             t=0
             if self.text_N.get()!="":
                 s=int(self.text_N.get())
                 t=1     
             if t==1:
                 self.destroy()
                 self=GUI(s)
                 self.initUI()
     def Setup2_Click(self):
             if self.text_eps.get()!="":
                 Node.eps=float(self.text_eps.get())

     def Read_Click(self):
         self.filepath=fd.askopenfilename(initialdir=r"/",filetypes=(('Text file','*.txt'),("All files", "*.*")))
         Start,Goal,Map=readFile(self.filepath)
         self.destroy()
         self=GUI(len(Map))
         self.Start=Start
         self.Goal=Goal
         self.Map=Map
         self.initUI(1)
     def Save_Click(self):
         self.filepath=fd.asksaveasfilename(initialdir = r"/",title = "Select file",filetypes = (("Text file","*.txt"),("All files","*.*")))
         writeFile(self.filepath,self.way,self.Map,self.id)
     def AStar(self):
         Node.Goalxy[0]=self.Goal.x;
         Node.Goalxy[1]=self.Goal.y;
         Open=[];
         Closed=[];
         self.Start.gValue=0;
         self.Goal.gValue=math.inf
         Successor=[[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]];
         heapq.heappush(Open,self.Start);
         while(self.Goal.positionVisited(Open) ==-1 and len(Open)>0):
             s=heapq.heappop(Open);
             if (s.positionVisited(Closed) ==-1):
                 Closed.append(s);
             for i in range(numSuccessor):
                 x=s.x+Successor[i][0];
                 y=s.y+Successor[i][1];
                 if x>=0 and x<self.size and y>=0 and y<self.size and self.Map[x][y]!=1:
                     s1=Node(x,y,s);
                     if s1.isVisited(Open) is False and s1.isVisited(Closed) is False:
                         s1.gValue=math.inf;
                     if s1.gValue>s.gValue+1:
                         s1.gValue=s.gValue+1;
                         if s1.positionVisited(Closed) ==-1:
                             self.draw(s1.y,s1.x,Color["Open"])
                             time.sleep(sleepTime)
                             self.gui_map.update()
                             heapq.heappush(Open,s1);
                     if self.Goal.isSamePosition(s1):
                         self.Goal=s1;
                         break;
         if self.Goal.gValue==math.inf:
             self.way= -1;
             self.result.config(text="FAIL!!!")
         else:
             self.draw(self.Goal.y,self.Goal.x,Color["Goal"])
             way=[]
             root=self.Goal
             while(root is not None):
                  way.append([root.x,root.y])
                  root=root.parent;
             self.way=way
             k=len(way)
             for i in range(1,k-1):
                 self.draw(way[k-1-i][1],way[k-1-i][0],Color["Last way"])
                 time.sleep(sleepTime)
                 self.gui_map.update()
             self.result.config(text="{0} steps".format(len(way)))
     def improvePath(self,Open,Closed,Incons):
          if len(Open)==0:
              return False;
          N=self.size
          Successor=[[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]];
          while self.Goal>Open[0] :
              s=heapq.heappop(Open);
              if s.isVisited(Closed) is False:
                  Closed.append(s);
              for i in range(numSuccessor):
                  x=s.x+Successor[i][0];
                  y=s.y+Successor[i][1];
                  if x>=0 and x<N and y>=0 and y<N and self.Map[x][y]!=1:
                      s1=Node(x,y,s);
                      if s1.isVisited(Open) is False and s1.isVisited(Closed) is False and s1.isVisited(Incons) is False:
                          s1.gValue=math.inf;
                      if s1.gValue>s.gValue+1:
                            s1.gValue=s.gValue+1;
                            if s1.positionVisited(Closed) ==-1:
                                k1=s1.positionVisited(Open)
                                if k1==-1:
                                    heapq.heappush(Open,s1);
                                    if self.checkWay(s1) is False:
                                            self.draw(s1.y,s1.x,Color["Open"])
                                            time.sleep(sleepTime)
                                            self.gui_map.update()
                                else:
                                    del Open[k1]
                                    heapq.heapify(Open)
                                    heapq.heappush(Open,s1)
                            else:
                                k2=s1.positionVisited(Incons)
                                if k2==-1:
                                    Incons.append(s1);
                                    if self.checkWay(s1) is False:
                                            self.draw(s1.y,s1.x,Color["Incons"])
                                            time.sleep(sleepTime)
                                            self.gui_map.update()
                                else:
                                    del Incons[k2]
                                    Incons.append(s1)
                          
                      if self.Goal.isSamePosition(s1):
                          self.Goal.gValue=s1.gValue;
                          Closed.append(s1);
              if len(Open)==0:
                  break;
          if (len(Closed)==0 or self.Goal.isSamePosition(Closed[len(Closed)-1])is False):
              return False;
          return True;
      
     def checkWay(self,Root):
         if self.Feature[Root.x][Root.y]==0:
             return False
         return True
      
     def ARAStar(self):
         if self.Start.isSamePosition(self.Goal):
             return;
         Node.Goalxy[0]=self.Goal.x;
         Node.Goalxy[1]=self.Goal.y;
         self.Goal.gValue=math.inf;
         self.Start.gValue=0;
         Open=[];
         Closed=[];
         Incons=[];
         heapq.heappush(Open,self.Start);
         if (self.improvePath(Open,Closed,Incons)):
             Root=Closed[len(Closed)-1];
             w=[]
             while(Root is not None):
                 w.append([Root.x,Root.y])
                 self.Feature[Root.x][Root.y]=1
                 Root=Root.parent;
             self.way.append(w)
             k=len(self.way)-1
             j=len(self.way[k])-1
             for i in range(1,j):
                 self.draw(self.way[k][j-i][1],self.way[k][j-i][0],Color["Way"])
                 time.sleep(sleepTime)
                 self.gui_map.update()
             self.result.config(text="{0} steps".format(len(self.way[k])))
             
         else:
             self.result.config(text="FAIL!!!")
             return;
         if (len(Open)==0 and len(Incons)==0):
             eps1=Node.eps;
         else: 
             eps1=min(Node.eps,self.Goal.gValue/min(minList(Open),minList(Incons)));
         while(eps1>1):
             Node.eps=Node.eps-deltaEps;
             tempList=Open;
             Open=[];
             for i in range(len(Incons)):
                 heapq.heappush(Open,Incons[i]);
             for i in range(len(tempList)):
                 heapq.heappush(Open,tempList[i]);
             Incons=[]
             Closed=[]
             if (self.improvePath(Open,Closed,Incons)):
                 Root=Closed[len(Closed)-1];
                 w=[]
                 while(Root is not None):
                     w.append([Root.x,Root.y])
                     self.Feature[Root.x][Root.y]=1
                     Root=Root.parent;
                 self.way.append(w)
                 k=len(self.way)-1
                 j=len(self.way[k])-1
                 for i in range(1,j):
                     self.draw(self.way[k][j-i][1],self.way[k][j-i][0],Color["Way"])
                     time.sleep(sleepTime)
                     self.gui_map.update()
                 self.result.config(text="{0} steps".format(len(self.way[k])))
             if (len(Open)==0 and len(Incons)==0):
                 eps1=Node.eps;
             else: 
                 eps1=min(Node.eps,self.Goal.gValue/min(minList(Open),minList(Incons)));                
         k=len(self.way)-1
         j=len(self.way[k])-1
         for i in range(1,j):
             self.draw(self.way[k][j-i][1],self.way[k][j-i][0],Color["Last way"])
             time.sleep(sleepTime)
             self.gui_map.update()
         self.result.config(text="{0} steps".format(len(self.way[k])))
         
def readFile(fname):
    f=open(fname,"r")
    N=int(f.readline(MAX))
    ar=[]

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
        for j in range(N):
            m[j]=int(m[j])
        Map.append(m)
    f.close()
    return Start,Goal,Map  

def writeFile(fname,way,Map,id):
    f= open(fname,"w")
    if(way==-1):
        f.write("-1")
    else:
        k=0
        w=[]
        if id==0:
            k=len(way)
            w=way
        else:
            k=len(way[len(way)-1])
            w=way[len(way)-1]
        f.write("%d\n"%(k))
        for i in range(k):
            f.write("(%d,%d) "%(w[k-1-i][0],w[k-1-i][1]))
        f.write("\n")
        M=[]
        for i in range(len(Map)):
            m=[]
            for j in range(len(Map)):
                if Map[i][j]==0:
                    m.append("-")
                else:
                    m.append("o")
            M.append(m)
        for i in range(1,len(w)-1):
            M[w[i][0]][w[i][1]]="x"
        M[w[0][0]][w[0][1]]="G"
        M[w[-1][0]][w[-1][1]]="S"
        
        for i in range(len(Map)):
            for j in range(len(Map)):
                f.write("%s "%(M[i][j]))
            f.write("\n")
    f.close()

def neighbor(x,y,size,g):
    plus=[[-2,0],[2,0],[0,-2],[0,2]]
    t=[]
    i=0
    t.append(random.randint(0,3))
    while len(t)<4:
        a=random.randint(0,3)
        r=1
        for j in t:
            if j==a:
                r=0
                break
        if r==1:
            t.append(a)
    for i in t:
        x1=x+plus[i][0]
        y1=y+plus[i][1]
        if x1>0 and x1<size and y1>0 and y1< size and g[x1][y1]==1:
            return [x1,y1]
    return -1

def delW(a,b,Map):
    if a[0]==b[0]:
        Map[a[0]][int((a[1]+b[1])/2)]=0
    else:
        Map[int((a[0]+b[0])/2)][a[1]]=0
        
def maze(size):
    Map=[]
    t=0
    for i in range(size):
        m=[]
        for j in range(size):
            m.append(1)
        Map.append(m)
    x=0
    y=0
    stack=[]
    while x%2==0:
        x=random.randint(0,size)
    while y%2==0:
        y=random.randint(0,size)
    Map[x][y]=0
    current=[x,y]
    k=int(size/2)
    k=k*k
    i=1
    stack=[]
    stack.append(current)
    while i<k:
        t=neighbor(current[0],current[1],size,Map)
        if t ==-1:
            if len(stack)>0:
                current=stack.pop()
        else:
            stack.append(current)
            delW(t,current,Map)
            Map[t[0]][t[1]]=0
            current=t
            i+=1
    return Map

def main():

    e=GUI()
    e.program()

if __name__ == '__main__':
    main()
