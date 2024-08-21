from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func
@dataclass
class GIORH:
    #key
    #geono unit vector number refered to on record GELREF1
    hz:float # height of beam current location
    ty:float  #thickness of beam web
    bt:float  # width of top flang
    tt:float # thickness of top flang
    bb:float # width of bottom flang
    tb:float # thickness of bottom flang 
    sfy:float #factors modifying the shear areas calculated by the preprocessor program
    sfz: float
    nlobyt:int=0 # number of integration points in top flang
    nlobyb: int=0 # number of integration points in bottom flang
    nlobz:int=0 # number of integration points in web

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GIORH     {geono:1.8E}  {self.hz:1.8E}  {self.ty:1.8E}  {self.bt:1.8E}\n')
        TFEMmod.append(f'          {self.tt:1.8E}  {self.bb:1.8E}  {self.tb:1.8E}  {self.sfy:1.8E}\n')
        TFEMmod.append(f'          {self.sfz:1.8E}  {self.nlobyt:1.8E}  {self.nlobyb:1.8E}  {self.nlobz:1.8E}\n')
        return TFEMmod
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,3)
        return (data[0],[*data[1::]] )
