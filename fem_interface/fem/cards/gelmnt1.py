from dataclasses import dataclass,field
from typing import IO,List
from fem_interface.fem.cards import util_func

@dataclass
class GELMNT1:
    
    # key elno internal element number
    elnox:int #external element number
    eltype:int #element type number
    eltyad:int #additonal information related to element typ
    nodin:List[int]=field(default=list)

    
    
    def print(self,elno):
        TFEMmod = []
        TFEMmod.append(f'GELMNT1   {self.elnox:1.8E}  {elno:1.8E}  {self.eltype:1.8E}  {self.eltyad:1.8E}\n')           
        if self.eltype==25:
            TFEMmod.append(f'          {self.nodin[0]:1.8E}  {self.nodin[1]:1.8E}  {self.nodin[2]:1.8E}  {0:1.8E}\n')
        elif self.eltype==23:
            TFEMmod.append(f'          {self.nodin[0]:1.8E}  {self.nodin[1]:1.8E}  {self.nodin[2]:1.8E}  {0:1.8E}\n')


        else:
            
            TFEMmod.append("        ")
            _NoSteps = util_func.printDataItem(TFEMmod,  self.nodin)
            TFEMmod.append("\n")
        return TFEMmod
    
    def print_file(self,elno,file:str):
        TFEMmod=self.print(elno)
        util_func.append_lines_to_file(TFEMmod,file)
    

    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        elnox=data[0]
        elno=int(data[1])
        eltype=int(data[2])
        eltyad=data[3]
         # 3-nodes curved beam element
        if eltype==int(23):
            data= util_func.getdata(line,fin,2,data)
            if len(data)==8:
                del(data[-1:])
            
        # 4 nodes shell element
        if eltype==int(24):
            data= util_func.getdata(line,fin,2,data)
        # 3 nodes shell element
        if eltype==int(25):
            data= util_func.getdata(line,fin,2,data)                        
                        
        # MASS ELEMENT    
        if eltype==int(11):
            data= util_func.getdata(line,fin,2,data)
            del(data[-3:])        
                
        # BEAM ELEMENT
        if eltype==int(15):
            data= util_func.getdata(line,fin,2,data)
            if len(data)==8:
                del(data[-2:]) 
                
        if eltype==int(28):
            data= util_func.getdata(line,fin,3,data)

        if eltype==int(26):
            data= util_func.getdata(line,fin,3,data)
            if len(data)==12:
                del(data[-2:]) 
                                               
        # 20 NODE ISOPARMETRIC HEXAHEDRON
        if eltype==int(20):
            data= util_func.getdata(line,fin,6,data)
                               
        #15 NODES ISOPARAMETRIC TRIRANGULAR PRISM
        if eltype==int(30):
            data= util_func.getdata(line,fin,5,data)
            if len(data)==20:
                data.pop(-1) 

        if eltype==int(31):
            data= util_func.getdata(line,fin,4,data)
            if len(data)==16:
                del(data[-2:])
                #data.extend([0,0])
            
        return (elno,[elnox,eltype,eltyad,[int(i) for i in data[4:]]])

                    
           


