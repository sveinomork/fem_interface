from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class GNODE:
    
    # key is ndoeno external node nubmer
    nodex:int #internal node number 
    ndof:int #number of degress of freedom
    odof:int # order of degress of fredom

    def print(self,nodeno):
        TFEMmod=[]
        TFEMmod.append("GNODE     ")
        TFEMmod.append(f'{self.nodex:1.8E}  {nodeno:1.8E}  {self.ndof:1.8E}  {self.odof:1.8E}\n')
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (int(data[1]),[data[0],data[2],data[3]] )
