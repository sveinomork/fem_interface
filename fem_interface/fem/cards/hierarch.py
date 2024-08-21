from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math

@dataclass
class HIERARCH:
    # key is ihref
    nifeld:int
    iselty:int # super element type number
    indsel:int # super element index number
    islevl:int # super element level 
    itref:int # referecne data type hsuptran 
    ihpref:int # reference hierarch data type
    nsub:int # nubmer of sub element in super element
    ihsrefs:list[int]=field(default_factory=list)


    def print(self,ihref):
        TFEMmod=[]
        TFEMmod.append("HIERARCH ")
        TFEMmod.append(f'{self.nifeld: 1.8E} {ihref: 1.8E} {self.iselty: 1.8E} {self.indsel: 1.8E}\n')
        TFEMmod.append(f'          {self.islevl:1.8E}  {self.itref:1.8E}  {self.ihpref:1.8E}  {self.nsub:1.8E}\n')
        
        if self.nifeld>8:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,self.ihsrefs)
            TFEMmod.append("\n")

        
        
        
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        nfield=int(float(data[0]))
       
        ihref=int(float(data[1]))
        iselty=int(float(data[2]))
        indsel=int(float(data[3]))
        
        

        if nfield>8:
            data=util_func.getdata(line,fin,math.ceil(nfield/4))
            islevl=int(float(data[4]))
            itref=int(float(data[5]))
            ihpref=int(float(data[6]))
            nsub=int(float(data[7]))
            return (ihref,[nfield,iselty,indsel,islevl,itref,ihpref,nsub,data[8::]] )
        data=util_func.getdata(line,fin,2)
        islevl=int(float(data[4]))
        itref=int(float(data[5]))
        ihpref=int(float(data[6]))
        nsub=int(float(data[7]))
        return (ihref,[nfield,iselty,indsel,islevl,itref,ihpref,nsub] )
