from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import logging
logger = logging.getLogger(__name__)


@dataclass
class BELLO2:
    #key is LLC
    # key is elno
    loadtyp:int #Load typ 1) normal pressure 2) load given in component form
    complx:int # phase shift definition
    layer:int # layer number
    #elno:int # internal element nuber
    ndof: int # Number of translation degrees of freedom along the given load line for line fjorce
    intno:int # Integration station reference number for data type GELINT
    line:int # line specification
    side:int # element side definiation
    rload:list[int]=field(default_factory=list)
    
    def print(self,llc,elno,line,side):
        TFEMmod = []                      
        TFEMmod.append(f'BELLO2    {llc:1.8E}  {self.loadtyp:1.8E}  {self.complx:1.8E}  {self.layer:1.8E}\n')
        TFEMmod.append(f'          {elno:1.8E}  {self.ndof:1.8E}  {self.intno:1.8E}  {line:1.8E}\n')
        TFEMmod.append(f'          {side:1.8E} {self.rload[0]: 1.8E} {self.rload[1]: 1.8E} {self.rload[2]: 1.8E}\n')
    
        
        
        if (int(self.ndof)==9 and int(self.loadtyp)==1):
            TFEMmod.append(f'         {self.rload[3]: 1.8E} {self.rload[4]: 1.8E} {self.rload[5]: 1.8E} {self.rload[6]: 1.8E}\n')
            TFEMmod.append(f'         {self.rload[7]: 1.8E} {self.rload[8]: 1.8E} \n')
        
       
            
        return TFEMmod
    
    def print_file(self,llc,elno,line,side,file:str):
        TFEMmod=self.print(llc,elno,line,side)
        util_func.append_lines_to_file(TFEMmod,file)


    @staticmethod
    def create(line:str,fin:IO)->tuple[int,int,int,list[float]]:
        data=util_func.getdata(line,fin,3)
        llc=data[0]    
        loadtyp=data[1]
        ndof=1
        if loadtyp!=3:
            ndof=data[5]
        complx=data[2]
        layer=data[3]
        elno=data[4]           
        intno=data[6]
        line=data[7]
        side=data[8]



        if int(ndof) not in [9]:
            logger.warning(f'BEUSLO not implemented for this element')
            

       
                
        
        if int(ndof)==9 and int(loadtyp)==1:
            data=util_func.getdata(line,fin,3,data)


     
        return (llc,elno,line,side,[loadtyp,complx,layer,ndof,intno,line,side,data[9:]])




