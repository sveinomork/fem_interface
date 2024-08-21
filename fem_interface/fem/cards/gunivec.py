from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class GUNIVEC:
    # key is transno external node nubmer
    unix:int #internal node number 
    uniy:int #number of degress of freedom
    uniz:int # order of degress of fredom

    def print(self,transno):
        TFEMmod=[]
        TFEMmod.append("GUNIVEC  ")
        TFEMmod.append(f'{transno: 1.8E} {self.unix: 1.8E} {self.uniy: 1.8E} {self.uniz: 1.8E}\n')
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (int(data[0]),[data[1],data[2],data[3]] )
