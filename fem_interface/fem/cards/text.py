from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
from itertools import islice

@dataclass
class TEXT:
   
    #type:int
    subtype:int
    nrecs:int
    nbyte:int
    lines:list[str]=field(default_factory=list)
    key:int=1
    
    def print(self,type_):
        TFEMmod=[]
        TFEMmod.append("TEXT      ")
        TFEMmod.append(f'{type_:1.8E}  {self.subtype:1.8E}  {self.nrecs:1.8E}  {self.nbyte:1.8E}\n')
        TFEMmod.extend(self.lines)     
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        nrecs=data[2]
        lines=list(islice(fin, int(nrecs)))
        ret_tup=(data[0],[data[1],data[2],data[3],lines] )
    
        return ret_tup