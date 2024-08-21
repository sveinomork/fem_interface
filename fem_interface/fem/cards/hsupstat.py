from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math

@dataclass
class HSUPSTAT:
    # key is iselty
    nfield:int # 
    nidof:int # estimated number of internal degrees of freedoms
    nrdof:int # estimated number of retained degrees of freedoms
    nband: int # estimated bandwidth of the internal degrees freedoms.
    nelt: int # estimated number of elements
    lindep:int # if >0 this super element has linear dependent nodes
    reloadc:int # number of real load cases
    complc:int # number of complex load cases
    
   

    def print(self,iselty):
        TFEMmod=[]
        TFEMmod.append("HSUPSTAT ")
        TFEMmod.append(f'{self.nfield: 1.8E} {iselty: 1.8E} {self.nidof: 1.8E} {self.nrdof: 1.8E}\n')
        TFEMmod.append("         ")
        TFEMmod.append(f'{self.nband: 1.8E} {self.nelt: 1.8E} {self.lindep: 1.8E} {self.reloadc: 1.8E}\n')
        TFEMmod.append("         ")
        TFEMmod.append(f'{self.complc: 1.8E} \n')
         
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        nfield=int(float(data[0]))
        iselty=int(float(data[1]))
        data=util_func.getdata(line,fin,math.ceil(nfield/4))
        tab=[]
        tab.append(nfield)
        tab.extend(data[2:-3])

        return (iselty,[*tab])
