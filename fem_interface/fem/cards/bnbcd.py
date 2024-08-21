from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class BNBCD:
    # key is nodeno
    ndof:int
    fix:list[int]=field(default_factory=list)
    
    def print(self,nodeno):
        TFEMmod = []                      
        TFEMmod.append(f'BNBCD     {nodeno:1.8E}  {self.ndof:1.8E}  {self.fix[0]:1.8E}  {self.fix[1]:1.8E}\n')
        TFEMmod.append(f'          {self.fix[2]:1.8E}  {self.fix[3]:1.8E}  {self.fix[4]:1.8E}  {self.fix[5]:1.8E}\n')        
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (int(data[0]),[data[1],data[2:]] )