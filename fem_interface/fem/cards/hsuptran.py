from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math

@dataclass
class HSUPTRAN:
    # key is itref
    nfield:int # 
    t:list[float]=field(default=list)
   

    def print(self,itref):
        TFEMmod=[]
        TFEMmod.append("HSUPTRAN ")
        TFEMmod.append(f'{self.nfield: 1.8E} {itref: 1.8E} {self.t[0]: 1.8E} {self.t[1]: 1.8E}\n')
        TFEMmod.append("        ")
        util_func.printDataItem_neg(TFEMmod,self.t[2::])
        TFEMmod.append("\n") 
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        nfield=int(float(data[0]))
        itref=int(float(data[1]))
        data=util_func.getdata(line,fin,math.ceil(nfield/4))

        return (itref,[nfield,data[2::]] )