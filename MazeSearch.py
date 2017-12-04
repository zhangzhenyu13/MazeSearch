from GameState import GameState
import copy
#
#
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
#node
class Node:
    pos=()
    prevNode=None
    bonus=0
    fee=0
    stepNum=0
    def eqPos(self, other):
        if other==None:return False
        if self.pos[0]==other.pos[0] and self.pos[1]==other.pos[1]:
            return True
        else:return False
    def __str__(self):
        s='Pos('+str(self.pos[0])+','+str(self.pos[1])+')|Bonus('+str(self.bonus)+')'
        return s
    def __eq__(self, other):
        if other is None:
            return False
        if self.pos[0] == other.pos[0] and self.pos[1]==other.pos[1]:
            return True
        return False
#so the steps
def getDirect(node1,node2):
    print(node1,"to",node2)
    x=node1.pos[0]-node2.pos[0]
    y=node1.pos[1]-node2.pos[1]
    if x>0:return LEFT
    elif x<0:return  RIGHT
    elif y>0:return  DOWN
    elif y<0:return UP
    else:pass
def StepTo(Pnode,Gnode,gs):
    print("from",Pnode,"to",Gnode)
    node = Gnode
    actionList=[]
    while Pnode.eqPos(node.prevNode)==False:
        actionList.insert(0,getDirect(node.prevNode,node))
        node=node.prevNode
        node.stepNum+=1
    actionList.insert(0,getDirect(Pnode,node))
    gs.step(actionList)
#push func
def OpenPush(node,open):#插入排序
    pass
    j = 0
    for a in open:
        if node.fee < a.fee:
            open.insert(j, copy.deepcopy(node))
            return
        else:
            j+=1
    #print(len(open),j,"push")
    open.insert(j,copy.deepcopy(node))

#fee Cal
def NodeFee(Pnode,node,f1=1,f2=5):
    prevNum=0
    factor1=f1;factor2=f2
    bonus=node.bonus
    while Pnode.eqPos(node.prevNode)==False:
        node=node.prevNode
        prevNum+=1
        bonus+=node.bonus
        #print(node,prevNum)
    prevNum+=1
    fee=factor1*prevNum-factor2*bonus
    #print("fee=",fee)
    return fee
def RestFee(node):
    factor1=1;factor2=0
    fee=-node.stepNum*factor1-node.bonus*factor2
    return fee
    pass
#5Method for Searching
#BFS
def BFS(gs,cs):
    open=[]
    close=[]
    #
    flag=False
    #init
    node=Node()
    node.bonus=0
    node.pos=cs
    Pnode=copy.deepcopy(node)
#init
    csn=copy.deepcopy(node)
    open.append(csn)
#begin iteration
    count=1
    while len(open) > 0:
        #print(csn,"with prevN as ",csn.prevNode, "for", count)
        open.pop(0)
        close.append(csn)
        suc=gs.query_successor(csn.pos)
        for i in range(4):
            #print("in",i)
            node.pos,node.bonus, flag=suc[i]
            if csn.prevNode is not None and node.eqPos(csn.prevNode):
                #print("Father:",node)
                continue
            if node in close:
                continue
            if node.eqPos(csn):
                continue
            node.bonus+=csn.bonus
            node.prevNode = csn
            if flag:
                print("found Goal")
                Gnode=node
                StepTo(Pnode,Gnode,gs)
                return 0

            open.append(copy.deepcopy(node))
            #print("add",node,"after",node.prevNode)
        csn=open[0]

        count=count+1

#failed
    return -1
#DFS
def DFS(gs,cs):
    open = []
    close = []
    #
    flag = False
    # init
    node = Node()
    node.isWall = False
    node.bonus = 0
    node.pos = cs
    Pnode = copy.deepcopy(node)
    # init
    csn = copy.deepcopy(node)
    open.append(csn)
    # begin iteration
    count = 1
    while len(open) > 0:
        #print(csn, "with prevN as ", csn.prevNode, "for", count)
        open.pop(len(open)-1)
        close.append(csn)
        suc = gs.query_successor(csn.pos)
        for i in range(4):
            # print("in",i)
            node.pos, node.bonus, flag = suc[i]
            if csn.prevNode is not None and node.eqPos(csn.prevNode):
                #print("Father:", node)
                continue
            if node in close:
                #print(node,"visited")
                continue
            if csn.eqPos(node):
                continue
            node.bonus+=csn.bonus
            node.prevNode = csn
            if flag:
                print("found Goal")
                Gnode = node
                StepTo(Pnode, Gnode, gs)
                return 0

            open.append(copy.deepcopy(node))
            #print("add", node, "after", node.prevNode)

        csn = open[len(open)-1]

        count = count + 1

        # failed
    return -1
#EqualFeeSearch
def EqFS(gs,cs):
    node=Node()
    node.pos=cs
    node.bonus=0
    node.fee=0
    open=[]
    close=[]
    csn=copy.deepcopy(node)
    Pnode=copy.deepcopy(node)
    open.append(csn)
    while len(open)>0:
        open.pop(0)
        close.append(csn)
        suc=gs.query_successor(csn.pos)
        #print(csn,csn.fee,"after",csn.prevNode)

        for i in range(4):
            node.pos, node.bonus, flag=suc[i]
            if node.prevNode is not None and node.eqPos(csn.prevNode):
                continue
            if csn.eqPos(node):
                continue
            if node in close:
                continue
            node.bonus+=csn.bonus
            node.prevNode = csn
            node.fee = NodeFee(Pnode,node)
            if node.bonus>0:
                Gnode = node
                StepTo(Pnode, Gnode, gs)
                node.bonus = 0
                node.fee = 0
                Pnode = copy.deepcopy(node)
                open.clear()
                close.clear()
                csn = Pnode
                open.append(csn)
                break

            if flag==True:
                print("found Goal")
                Gnode=node
                StepTo(Pnode,Gnode,gs)
                return 0

            OpenPush(copy.deepcopy(node),open)
            #print("add",node,node.fee)

        csn=open[0]
    return -1
#Climb Mountain
def CloserToSearch(gs,cs):
    node = Node()
    node.pos = cs
    node.bonus = 0
    node.fee = 0
    open = []
    close = []
    csn = copy.deepcopy(node)
    Pnode = csn
    open.append(csn)
    while len(open) > 0:
        open.pop(0)
        close.append(csn)
        suc = gs.query_successor(csn.pos)
        #print(csn, "after", csn.prevNode)

        for i in range(4):
            node.pos, node.bonus, flag = suc[i]
            if node.prevNode is not None and node.eqPos(csn.prevNode):
                continue
            if node in close:
                continue
            if csn.eqPos(node):
                continue
            node.bonus = csn.bonus + node.bonus
            if node.bonus>0:
                Gnode=node
                StepTo(Pnode,Gnode,gs)
                node.bonus=0
                node.fee=0
                Pnode=copy.deepcopy(node)
                open.clear()
                close.clear()
                csn=Pnode
                open.append(csn)
                break

            node.fee = RestFee(node)
            node.prevNode = csn
            if flag == True:
                print("found Goal")
                Gnode = node
                StepTo(Pnode, Gnode, gs)
                return 0
            OpenPush(node, open)
            #print("add", node)

        csn = open[0]
    return -1
#A*
def BestNodeSearch(gs,cs):
    node = Node()
    node.pos = cs
    node.bonus = 0
    node.fee = 0
    open = []
    close = []
    csn = copy.deepcopy(node)
    Pnode = csn
    open.append(csn)
    while len(open) > 0:
        open.pop(0)
        close.append(csn)
        suc = gs.query_successor(csn.pos)
        print(csn, "after", csn.prevNode)

        for i in range(4):
            node.pos, node.bonus, flag = suc[i]
            if node.prevNode is not None and node.eqPos(csn.prevNode):
                continue
            if csn.eqPos(node):
                continue

            if node in open:
                oldNode=open[open.index(node)]
                if NodeFee(Pnode,node)<NodeFee(Pnode,oldNode):
                    #oldNode=node
                    open.remove(oldNode)
                else:
                    continue
            elif node in close:
                oldNode=close[close.index(node)]
                if NodeFee(Pnode,node)<NodeFee(Pnode,oldNode):
                    #oldNode=node
                    close.remove(oldNode)
                else:
                    continue
            else:
                pass

            node.prevNode = csn
            node.bonus = csn.bonus + node.bonus
            node.fee = RestFee(node) + NodeFee(Pnode, node)
            if node.bonus > 0:
                Gnode = node
                StepTo(Pnode, Gnode, gs)
                node.bonus=0
                node.fee=0
                Pnode = copy.deepcopy(node)
                open.clear()
                close.clear()
                csn = Pnode
                open.append(csn)
                break



            if flag == True:
                print("found Goal")
                Gnode = node
                StepTo(Pnode, Gnode, gs)
                return 0
            OpenPush(node, open)
            print("add", node)

        csn = open[0]
    return -1
    pass
#main
def main():
    mapfile="layouts\\small.lay"
    gs=GameState(mapfile)
    cs=gs.get_current_state()
    method={1:BFS,2:DFS,3:EqFS,4:CloserToSearch,5:BestNodeSearch}
    m=eval(input("BFS:1,DFS:2,等费用:3,爬山法:4,A*:5\n"))
    try:
        method[m](gs,cs)
    except Exception as InE:
        print(InE.args)
        print("Alg Stopped with Error!")
        exit -1

    print("finished with")
    f=open(".\\result_success.txt")
    print(f.read())
    f.close()
    return 0
main()
