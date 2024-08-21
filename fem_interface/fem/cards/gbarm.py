from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func
from typing import IO
@dataclass
class GBARM:
    #key
    #geono unit vector number refered to on record GELREF1
    hz:float # height of beam current location
    bt:float  #width of bar at top
    bb:float  #wid of bar at bottom
    sfy:float
    sfz:float
    nloby:float=0 #number of integration points in each hoirzontal wall (flange) of beam 
    nlobz:float=0
    

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GBARM     {geono:1.8E}  {self.hz:1.8E}  {self.bt:1.8E}  {self.bb:1.8E}\n')
        TFEMmod.append(f'          {self.sfy:1.8E}  {self.sfz:1.8E}  {self.nloby:1.8E}  {self.nlobz:1.8E}\n')
        
       
        return TFEMmod
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (data[0],[*data[1::]] )
