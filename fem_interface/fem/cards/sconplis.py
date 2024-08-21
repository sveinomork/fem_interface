from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math




@dataclass
class PSEL:
    typepro:int #finite element representation type
    irpsele:int #Number of finite element representations.
    


@dataclass
class  SCONPLIS:

    # key is ircon
    nfield:int # Number of data fields on this data type (including this field).
    numsel:int # Number of finite element representation types.   
    numsels:list[PSEL]=field(default_factory=list) # finite element representation reference numbers (internal id).

    def print(self,ircon):

        flat_list=[]
        for k in self.numsels:
            
            flat_list.append(k.typepro)
            flat_list.append(k.irpsele)
            

        TFEMmod=[]
      
        TFEMmod.append("SCONPLIS  ")
        TFEMmod.append(f'{self.nfield:1.8E}  {ircon:1.8E}  {self.numsel:1.8E}  {flat_list[0]:1.8E}  \n')
        if self.nfield>4:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,flat_list[1:])
            TFEMmod.append("\n")

        return TFEMmod
    
    def print_file(self,ircon,file:str):
        TFEMmod=self.print(ircon)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:

       
        ret:tuple[int,list[float]]=()
        
        if 'SCONPLIS' in line:
            data=util_func.getdata(line,fin,1)
            nfield=int(data[0]) # number of data fileds on this record

           
            ircone=int(data[1] )  # 
            
            numpsel=int(data[2] )  # 
          
            numpsels=[]
            data=util_func.getdata(line,fin,math.ceil(nfield/4))
            data=data[3::]
            
            while len(data)>0:
                
                typeprop=data[0]
                irpsele=int(data[1])

               

                pselP=PSEL(typeprop,irpsele)
                numpsels.append(pselP)
                data=data[2::]
            
           
            
                
            ret=(ircone,[nfield,numpsel,numpsels])

            return ret