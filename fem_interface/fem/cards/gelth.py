from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func
@dataclass
class GELTH:
    #key
    #geono unit vector number refered to on record GELREF1
    th:float # height of beam current location
    nint:float=0  #thickness of beam web
    ishear:float=0  # width of top flang
    

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GELTH     {geono:1.8E}  {self.th:1.8E}  {self.nint:1.8E}  {self.ishear:1.8E}\n')
      
        return TFEMmod
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (data[0],[*data[1::]] )
