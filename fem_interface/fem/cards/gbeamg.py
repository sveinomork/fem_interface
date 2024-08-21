from dataclasses import dataclass,field
from typing import List
from fem_interface.fem.cards import util_func
from typing import IO
@dataclass  
class GBEAMG:
    #key
    #geono unit vector number refered to on record GELREF1
    comp:int 
    area:float
    ix:float
    iy:float
    iz:float
    iyz:float
    wxmin:float
    wymin:float
    wzmin:float
    shary:float
    sharz:float
    shceny:float
    shcenz:float
    sy:float
    sz:float
    wpy:float=0
    wpz:float=0
    fabr:int=0
    not_used:int=0
    
   
        
    
    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GBEAMG    {geono:1.8E}  {self.comp:1.8E}  {self.area:1.8E} {self.ix: 1.8E}\n')
        TFEMmod.append(f'         {self.iy: 1.8E} {self.iz: 1.8E} {self.iyz: 1.8E} {self.wxmin: 1.8E}\n')
        TFEMmod.append(f'         {self.wymin: 1.8E} {self.wzmin: 1.8E} {self.shary: 1.8E} {self.sharz: 1.8E}\n')
        TFEMmod.append(f'         {self.shceny: 1.8E} {self.shcenz: 1.8E} {self.sy: 1.8E} {self.sz: 1.8E}\n')
        if self.comp==2:
            TFEMmod.append(f'         {self.wpy: 1.8E} {self.wpz: 1.8E} {self.fabr: 1.8E} \n')
        return TFEMmod
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)


    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        if int(data[1])==2:
            data=util_func.getdata(line,fin,5)
        if int(data[1])==0:
            data=util_func.getdata(line,fin,4)

     
        return (int(data[0]),[*data[1::]] )
