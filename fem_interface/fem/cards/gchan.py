from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func

@dataclass
class GCHAN:
    #key
    #geono unit vector number refered to on record GELREF1
    hz:float # height of beam current location
    ty:float  #thickness of beam web
    by:float  # thickness of  bottom flang
    tz:float # thickness of top and bottom flang
    sfy:float #factors modifying the shear areas calculated by the preprocessor program
    sfz:float
    k:int # Web orientation 
    nloby:float=0 #number of integration points in each hoirzontal wall (flange) of beam 
    nlobz:float=0
    

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GCHAN     {geono:1.8E}  {self.hz:1.8E}  {self.ty:1.8E}  {self.by:1.8E}\n')
        TFEMmod.append(f'          {self.tz:1.8E}  {self.sfy:1.8E}  {self.sfz:1.8E}  \n')
        TFEMmod.append(f'          {self.k:1.8E}  {self.nloby:1.8E}  {self.nlobz:1.8E}  \n')
        return TFEMmod
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,3)
        return (data[0],[*data[1::]] )
