

import math
from typing import IO
from dataclasses import dataclass,field
from fem_interface.fem.cards.util_func import getdata
from fem_interface.fem.cards import util_func
@dataclass
class TDSCONC:

    # key is IRCON
    name:str
    nfield:int # Number of numeric data fields at this data type before text data (MAX=1024)
    codnam:int  #
    codtxt:int   #

    def print(self,ircon:int)->list[str]:
        TFEMmod=[]
        TFEMmod.append("TDSCONC   ")
        TFEMmod.append(f'{self.nfield:1.8E}  {ircon:1.8E}  {self.codnam:1.8E}  {self.codtxt:1.8E}  \n')
        TFEMmod.append("        {:}\n".format(self.name)) 
        return TFEMmod
    
    def print_file(self,ircon,file:str):
        TFEMmod=self.print(ircon)
        util_func.append_lines_to_file(TFEMmod,file)

    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=getdata(line,fin,2)
        return (int(data[1]),[data[4],data[0],data[2],data[3]] )