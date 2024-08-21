from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func
@dataclass
class GPIPE:
    #key
    #geono unit vector number refered to on record GELREF1
    di:float # inner diameter
    dy:float  # outer diameter
    t:float  # thickness of  tube
    sfy:float # factor shear
    sfz:float
    ncir:int=0 # number of integration point
    nrad:int=0
    
    

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GPIPE     {geono:1.8E}  {self.di:1.8E}  {self.dy:1.8E}  {self.t:1.8E}\n')
        TFEMmod.append("          ") 
        TFEMmod.append(f'{self.sfy:1.8E}  {self.sfz:1.8E}  {self.ncir:1.8E}  {self.nrad:1.8E}  \n')
    
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (data[0],[*data[1::]] )
