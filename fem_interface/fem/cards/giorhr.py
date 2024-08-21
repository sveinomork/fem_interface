from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func

@dataclass
class GIORHR:
    #key
    #geono unit vector number refered to on record GELREF1
    hz:float # height of beam current location
    ty:float
    bt:float  #width of bar at top
    tt:float
    bb:float  #wid of bar at bottom
    tb:float
    sfy:float
    sfz:float
    nloby:float=0 #number of integration points in each hoirzontal wall (flange) of beam 
    nlobz:float=0
    

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GIORHR    {geono:1.8E}  {self.hz:1.8E}  {self.ty:1.8E}  {self.bt:1.8E}\n')
        TFEMmod.append(f'          {self.tt:1.8E}  {self.bb:1.8E}  {self.tb:1.8E}  {self.sfy:1.8E}\n')
        TFEMmod.append(f'          {self.nloby:1.8E}  {self.nlobz:1.8E}  \n')
        
       
        return TFEMmod
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,3)
        return (data[0],[*data[1::]] )
