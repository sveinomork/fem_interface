from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO

@dataclass
class DEP:
    s:float
    m:float
    b:float
    not_in_use:float


@dataclass
class BLDEP:
    # slave is key
    master:int
    nddof:int
    ndep:int
    deps:list[DEP]=field(default_factory=list)
    
    def print(self,slave):
        TFEMmod = []                      
        TFEMmod.append(f'BLDEP     {slave:1.8E}  {self.master:1.8E}  {self.nddof:1.8E}  {self.ndep:1.8E}\n')
        for dep in self.deps:
            TFEMmod.append(f'         {dep.s: 1.8E} {dep.m: 1.8E} {dep.b: 1.8E} {dep.not_in_use: 1.8E}\n')        
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        slave=int(data[0])
        master=int(data[1])
        nddof=int(data[2])
        ndep=int(data[3])
        
        data=util_func.getdata(line,fin,int(data[3])+1)
        data=data[4::]
        deps=[]
        while len(data)>0:
            dep=[]
            for n in range(4):
                dep.append(data[n])

            deps.append(DEP(*dep))
            
            data=data[4::]

        ret=(slave,[master,nddof,ndep,deps])

        return ret