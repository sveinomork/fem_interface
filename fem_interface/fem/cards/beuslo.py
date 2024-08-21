from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import logging
logger = logging.getLogger(__name__)


@dataclass
class BEUSLO:
    #key is LLC
    # key is elno
    loadtyp:int #Load typ 1) normal pressure 2) load given in component form
    complx:int # phase shift definition
    layer:int # layer number
    #elno:int # internal element nuber
    ndof: int # if lodtyp 1 number of node on the specified lement side,if 2 numb tranlation dof
    intno:int
    side:int
    rload:list[int]=field(default_factory=list)
    
    def print(self,llc,elno,side):
        TFEMmod = []                      
        TFEMmod.append(f'BEUSLO    {llc:1.8E}  {self.loadtyp:1.8E}  {self.complx:1.8E}  {self.layer:1.8E}\n')
        TFEMmod.append(f'          {elno:1.8E}  {self.ndof:1.8E}  {self.intno:1.8E}  {side:1.8E}\n')
    
        if int(self.loadtyp)==3:
            TFEMmod.append(f'         {1: 1.8E} {0: 1.8E} {0: 1.8E} {0: 1.8E}\n')
            
        if (int(self.ndof)==8 and int(self.loadtyp)==1):
            TFEMmod.append(f'         {self.rload[0]: 1.8E} {self.rload[1]: 1.8E} {self.rload[2]: 1.8E} {self.rload[3]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[4]: 1.8E} {self.rload[5]: 1.8E} {self.rload[6]: 1.8E} {self.rload[7]: 1.8E}\n')
        
        
        
        
        if (int(self.ndof)==6 and int(self.loadtyp)==1):
            TFEMmod.append(f'         {self.rload[0]: 1.8E} {self.rload[1]: 1.8E} {self.rload[2]: 1.8E} {self.rload[3]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[4]: 1.8E} {self.rload[5]: 1.8E} {0: 1.8E} {0: 1.8E}\n')
        if (int(self.ndof)==24 and int(self.loadtyp)==2):
            TFEMmod.append(f'         {self.rload[0]: 1.8E} {self.rload[1]: 1.8E} {self.rload[2]: 1.8E} {self.rload[3]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[4]: 1.8E} {self.rload[5]: 1.8E} {self.rload[6]: 1.8E} {self.rload[7]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[8]: 1.8E} {self.rload[9]: 1.8E} {self.rload[10]: 1.8E} {self.rload[11]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[12]: 1.8E} {self.rload[13]: 1.8E} {self.rload[14]: 1.8E} {self.rload[15]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[16]: 1.8E} {self.rload[17]: 1.8E} {self.rload[18]: 1.8E} {self.rload[19]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[20]: 1.8E} {self.rload[21]: 1.8E} {self.rload[22]: 1.8E} {self.rload[23]: 1.8E}\n')
        if (int(self.ndof)==18 and int(self.loadtyp)==2):
            TFEMmod.append(f'         {self.rload[0]: 1.8E} {self.rload[1]: 1.8E} {self.rload[2]: 1.8E} {self.rload[3]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[4]: 1.8E} {self.rload[5]: 1.8E} {self.rload[6]: 1.8E} {self.rload[7]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[8]: 1.8E} {self.rload[9]: 1.8E} {self.rload[10]: 1.8E} {self.rload[11]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[12]: 1.8E} {self.rload[13]: 1.8E} {self.rload[14]: 1.8E} {self.rload[15]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[16]: 1.8E} {self.rload[17]: 1.8E} {0: 1.8E} {0: 1.8E}\n')
        return TFEMmod
    

    def print_file(self,llc,elno,side,file:str):
        TFEMmod=self.print(llc,elno,side)
        util_func.append_lines_to_file(TFEMmod,file)
    
        


    @staticmethod
    def create(line:str,fin:IO)->tuple[int,int,int,list[float]]:
        data=util_func.getdata(line,fin,2)
        llc=data[0]    
        loadtyp=data[1]
        ndof=1
        if loadtyp!=3:
            ndof=data[5]
        complx=data[2]
        layer=data[3]
        elno=data[4]           
        intno=data[6]
        side=data[7]

        if int(ndof) not in [1,6,8,18,24]:
            logger.warning(f'BEUSLO not implemented for this element')
            

        if int(ndof)==1:
            data=util_func.getdata(line,fin,1,data)
                
        if int(ndof)==6 and int(loadtyp)==1:
            data=util_func.getdata(line,fin,3,data)
            del(data[-2:]) 
        if int(ndof)==8 and int(loadtyp)==1:
            data=util_func.getdata(line,fin,3,data)
        if int(ndof)==18 and int(loadtyp)==2:
            data=util_func.getdata(line,fin,6,data)          
                
        if int(ndof)==24 and int(loadtyp)==2:
            data=util_func.getdata(line,fin,7,data)
        return (llc,elno,side,[loadtyp,complx,layer,ndof,intno,side,data[8:]])




