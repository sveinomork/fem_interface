from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class IEND:
    slevel:int #superelement level
    seltype:int #superelement type number is key
    selmod:int #superelement model dimension
    def print(self,seltype):
        TFEMmod=[]
        TFEMmod.append("IEND      ")
        TFEMmod.append(f'{0.0:1.8E}  {0.0:1.8E}  {0.0:1.8E}  {0.0:1.8E}  \n')
        return TFEMmod
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        
        return (1,[data[1],data[2],data[3]] )