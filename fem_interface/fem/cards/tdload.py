from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO
@dataclass
class TDLOAD: 
    #llc:int  # internal load identification number
    
    nfield:int
    codname:int
    codtxt:int
    txt:str
    
    
        
    def print(self,llc):
        TFEMmod = []                      
        TFEMmod.append(f'TDLOAD    {self.nfield:1.8E}  {llc:1.8E}  {self.codname:1.8E}  {self.codtxt:1.8E}\n')
        TFEMmod.append("        {:}\n".format(self.txt)) 
        return TFEMmod 
    
    def print_file(self,llc,file:str):
        TFEMmod=self.print(llc)
        util_func.append_lines_to_file(TFEMmod,file)

    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (int(data[1]),[data[0],data[2],data[3],data[4]] )   