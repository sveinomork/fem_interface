from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func

@dataclass
class BGRAV:
    #llc is key
    modelnode:int
    opt:int
    gx:float
    gy:float
    gz:float
    
    def print(self,llc):
        TFEMmod=[]
        TFEMmod.append("BGRAV     ")
        TFEMmod.append(f'{llc:1.8E} {self.modelnode: 1.8E} {0: 1.8E} {self.opt: 1.8E}\n')   
        TFEMmod.append("          ") 
        TFEMmod.append(f'{self.gx:1.8E} {self.gy: 1.8E} {self.gz: 1.8E} {0: 1.8E}\n')              
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (int(data[0]),[data[1],data[3],data[4],data[5],data[6]] )