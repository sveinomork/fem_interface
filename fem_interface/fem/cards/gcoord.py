from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func

@dataclass
class GCOORD:

    xcoord:float
    ycoord:float
    zcoord:float
    
    def print(self,nodeno):
        TFEMmod=[]
        TFEMmod.append("GCOORD    ")
        TFEMmod.append(f'{nodeno:1.8E} {self.xcoord: 1.8E} {self.ycoord: 1.8E} {self.zcoord: 1.8E}\n')               
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)

    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (int(data[0]),[data[1],data[2],data[3]] )