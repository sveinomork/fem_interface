from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math




@dataclass
class PSEL:
    typeattr:int #finite element representation type
    value:int #atribute value
    


@dataclass
class  SPROCODE:

    # key is irpattr
    nfield:int # Number of data fields on this data type (including this field).
    numattr:int # Number of finite element representation types.   
    attrs:list[PSEL]=field(default_factory=list) # finite element representation reference numbers (internal id).

    def print(self,irpattr):

        flat_list=[]
        for k in self.attrs:
            
            flat_list.append(k.typeattr)
            flat_list.append(k.value)
            

        TFEMmod=[]
      
        TFEMmod.append("SPROCODE  ")
        TFEMmod.append(f'{self.nfield:1.8E}  {irpattr:1.8E}  {self.numattr:1.8E}  {flat_list[0]:1.8E}  \n')
        if self.nfield>4:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,flat_list[1:])
            TFEMmod.append("\n")

        return TFEMmod
    
    def print_file(self,irpattr,file:str):
        TFEMmod=self.print(irpattr)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:

       
        ret:tuple[int,list[float]]=()
        
        
        data=util_func.getdata(line,fin,1)
        nfield=int(data[0]) # number of data fileds on this record

           
        irpattr=int(data[1] )  # 
            
        numattr=int(data[2] )  # 
          
        attrs=[]
        data=util_func.getdata(line,fin,math.ceil(nfield/4))
        data=data[3::]
            
        while len(data)>0:
                
            typeattr=data[0]
            value=int(data[1])

            pselP=PSEL(typeattr,value)
            attrs.append(pselP)
            data=data[2::]
                           
        ret=(irpattr,[nfield,numattr,attrs])

        return ret