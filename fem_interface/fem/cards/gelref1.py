from dataclasses import dataclass,field
from typing import IO
from fem_interface.fem.cards import util_func
from fem_interface.fem.cards.gelmnt1 import GELMNT1
@dataclass

class GELREF1:
    
    matno:int # mat number
    addno:int #element type number
    intno:int #additonal information related to element typ
    mintno:int
    strano:int
    streno:int
    strepono:int
    geono:int
    fixno:int
    eccno:int
    transno:int
    geonos:list[float]=field(default_factory=list)
    
    def print(self,elno):
        TFEMmod = []
        TFEMmod.append(f'GELREF1   {elno:1.8E}  {self.matno:1.8E}  {self.addno:1.8E}  {self.intno:1.8E}\n') 
        TFEMmod.append(f'          {self.mintno:1.8E}  {self.strano:1.8E}  {self.streno:1.8E}  {self.strepono:1.8E}\n')
        TFEMmod.append(f'          {self.geono:1.8E}  {self.fixno:1.8E} {self.eccno: 1.8E} {self.transno: 1.8E}\n')
        if len(self.geonos)>0:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,self.geonos)
            TFEMmod.append("\n")  

        return TFEMmod
    
    def print_file(self,elno,file:str):
        TFEMmod=self.print(elno)
        util_func.append_lines_to_file(TFEMmod,file)

    @staticmethod
    def create(line:str,fin:IO,gelmnt1:dict[int,GELMNT1])->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,3)
        
        le=len([var for var in data[8:12] if var < 0])
        if le > 0:
            ndof=len(gelmnt1[data[0]].nodin)
            n=(le*ndof)//4+1
            data1=util_func.getdata(line,fin,n+1)
            genos=[data1[i+4] for i in range(ndof*le)]
            
            return (data[0],[data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],genos])
        else:
        
         return (data[0],[data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11]])