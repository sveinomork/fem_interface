from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO
@dataclass
class TDMATER: 
    #matno:int  # internal load identification number
    
    nfield:int
    codname:int
    codtxt:int
    name:str
    
   
        
    def print(self,matno):
        TFEMmod = []                      
        TFEMmod.append(f'TDMATER   {self.nfield:1.8E}  {matno:1.8E}  {self.codname:1.8E}  {self.codtxt:1.8E}\n')
        TFEMmod.append("        {:}\n".format(self.name)) 
        return TFEMmod 
    
    def print_file(self,matno,file:str):
        TFEMmod=self.print(matno)
        util_func.append_lines_to_file(TFEMmod,file)

    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (int(data[1]),[data[0],data[2],data[3],data[4]] )   