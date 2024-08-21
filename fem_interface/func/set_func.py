from fem_interface.fem.fem_base import FEM_BASE
from typing import Self
from fem_interface.func.func_template import FUNC_TEMPLATE
from fem_interface.fem.cards.gsetmemb import GSETMEMB
from fem_interface.fem.cards.tdsetnam import TDSETNAM



class SET_FUNC(FEM_BASE,FUNC_TEMPLATE):

    def create_set(self,num,fem_List,type,tx1=None,tx2=None)->None:
        
        if tx1==None:
            n_tx1=0
        else:
            n_tx1=len(tx1)

        if tx2==None:
            n_tx2=0
        else:
            n_tx2=len(tx2)
        
        if num not in self.gsetmemb:
            self.gsetmemb[num]={}
        if type not in self.gsetmemb[num]:
            self.gsetmemb[num][type]={}
        if num not in self.tdsetnam:
            self.tdsetnam[num]=TDSETNAM(4,100+n_tx1,100+n_tx2,tx1)        
        count=0
        index=1
        tempList=[]
        for element in fem_List:
            _slots = 1024
            count+=1
            if count<_slots-5:
                index=index
                tempList.append(element)
            else:
                self.gsetmemb[num][type][index]=GSETMEMB(1024,type,1,tempList)
                tempList=[]
                tempList.append(element)
                index+=1
                count=0
        else:
            self.gsetmemb[num][type][index]=GSETMEMB(len(tempList)+5,2,1,tempList)


    def find_nex_unused_set_num(self)->int:
        set_nums=[]
        for num in self.gsetmemb:
            set_nums.append(num)
        
        return max(list(set(set_nums)))+1
