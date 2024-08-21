from dataclasses import dataclass
from typing import IO
from fem_interface.fem.cards import util_func

@dataclass
class BELFIX:
    # fixno is key
    opt:int # 
    trano:int #element type number
    a1:int #additonal information related to element typ
    a2:int
    a3:int
    a4:int
    a5:int
    a6:int
    
    
    def print(self,fixno):
        TFEMmod = []
        TFEMmod.append(f'BELFIX    {fixno:1.8E}  {self.opt:1.8E}  {self.trano:1.8E}  \n') 
        TFEMmod.append(f'          {self.a1:1.8E}  {self.a2:1.8E}  {self.a3:1.8E}  {self.a4:1.8E}\n')
        TFEMmod.append(f'          {self.a5:1.8E}  {self.a6:1.8E}  \n')
        return TFEMmod
    
    def print_file(self,fixno,file:str):
        TFEMmod=self.print(fixno)
        util_func.append_lines_to_file(TFEMmod,file)

    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,3)
        return (data[0],[data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]])