



from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class GECCEN:
    # key is eccno external node nubmer
    ex:int #internal node number 
    ey:int #number of degress of freedom
    ez:int # order of degress of fredom

    def print(self,eccno):
        TFEMmod=[]
        TFEMmod.append("GECCEN    ")
        TFEMmod.append(f'{eccno:1.8E} {self.ex: 1.8E} {self.ey: 1.8E} {self.ez: 1.8E}\n')
        return TFEMmod
    
    def print_file(self,eccno,file:str):
        TFEMmod=self.print(eccno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (int(data[0]),[data[1],data[2],data[3]] )
