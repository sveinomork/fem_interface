from dataclasses import dataclass,field
from typing import IO
from fem_interface.fem.cards import util_func
import math


@dataclass
class GSETMEMB:
    #index in dic isref_index
    #isref is key
    
    #isref:int  # internal set identification number
    #index:int # sequential record number
    
    nfield:int=0
    istype:int=2 #set type 1:nodes 2:elements
    isorgi:int=1
    irmemb:list[int]=field(default_factory=list)

    
   
    
    
    def print(self,isref,istype,index):
        
        

        TFEMmod = []                      
        TFEMmod.append(f'GSETMEMB  {self.nfield:1.8E}  {isref:1.8E}  {index:1.8E}  {istype:1.8E}\n')
        TFEMmod.append(f'          {self.isorgi:1.8E}  {self.irmemb[0]:1.8E}  {self.irmemb[1]:1.8E}  {self.irmemb[2]:1.8E}\n')
        TFEMmod.append("        ")
        util_func.printDataItem(TFEMmod,self.irmemb[3:])
        TFEMmod.append("\n")  
          
          
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,int,int,list[int]]:
        data=util_func.getdata(line,fin,1)
        nfield=data[0] # number of data fileds on this record       
        isref=data[1]   # internal set identification number as defined TDSETNAME
        index=data[2]   # sequential record number for current set
        istype=data[3]  # 1 set of nodes, 2 set of elments        
        data=util_func.getdata(line,fin,math.ceil(nfield/4))
        isorgi=data[4]
        irmemb=[int(el) for el in data[5:]]               
        return (isref,istype,index,[nfield,istype,isorgi,irmemb])


    

