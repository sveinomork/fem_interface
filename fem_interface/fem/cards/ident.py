from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class IDENT:
    slevel:int #superelement level
    #seltype:int #superelement type number is key
    selmod:int #superelement model dimension
    def print(self,seltype):
        TFEMmod=[]
        TFEMmod.append("IDENT     ")
        TFEMmod.append(f'{self.slevel:1.8E}  {seltype:1.8E}  {self.selmod:1.8E}  {0.0:1.8E}  \n')
        return TFEMmod
    
    def print_file(self,seltype,file:str):
        TFEMmod=self.print(seltype)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (int(data[1]),[data[0],data[2]] )