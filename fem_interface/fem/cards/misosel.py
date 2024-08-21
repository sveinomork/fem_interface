from dataclasses import dataclass
from fem_interface.fem.cards import util_func
from typing import IO


@dataclass
class MISOSEL:
    young:float
    poiss:float
    rho:float
    damp:float
    alpha:float
    
    def print(self,matno):
        TFEMmod = []                      
        TFEMmod.append(f'MISOSEL   {matno:1.8E}  {self.young:1.8E}  {self.poiss:1.8E}  {self.rho:1.8E}\n')
        TFEMmod.append(f'          {self.damp:1.8E}  {self.alpha:1.8E}    \n')
        return TFEMmod
    
    def print_file(self,matno,file:str):
        TFEMmod=self.print(matno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        
        return (int(data[0]),[data[1],data[2],data[3],data[4],data[5] ])  