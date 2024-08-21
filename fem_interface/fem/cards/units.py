from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func

@dataclass
class UNITS:
    nfield:int
    #id:int kye
    lenfac:float #Length unit coverted to SI base unit [m]
    forfac:float #Force unit coverted SI base unit [N]
    tempfac:float # Temperature difference unit convert to SI base unit [delC]
    
    def print(self,id):
        TFEMmod=[]
        TFEMmod.append("UNITS     ")
        TFEMmod.append(f'{self.nfield:1.8E} {id: 1.8E} {self.lenfac: 1.8E} {self.forfac: 1.8E}\n')    
        TFEMmod.append(f'          {self.tempfac:1.8E}  \n')           
        return TFEMmod
    
    def print_file(self,id,file:str):
        TFEMmod=self.print(id)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (data[1],[data[0],data[2],data[3],data[4]] )