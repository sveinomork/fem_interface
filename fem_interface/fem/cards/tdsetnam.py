from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
from itertools import islice

@dataclass
class TDSETNAM:
    nfield:int # number of datafiled
    #isref is key
    codname:int
    codtxt:int
    name:str
 
    
    def print(self,isref):
        TFEMmod = []                      
        TFEMmod.append(f'TDSETNAM  {self.nfield:1.8E}  {isref:1.8E}  {self.codname:1.8E}  {0.0:1.8E}\n')
        TFEMmod.append("        {:}\n".format(self.name))
      
        return TFEMmod
    
    def print_file(self,isref,file:str):
        TFEMmod=self.print(isref)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
       
        
        return (int(data[1]),[data[0],data[2],data[3],data[4]] )  