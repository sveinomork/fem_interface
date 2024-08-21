from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math




@dataclass
class TYPE:
    typepro:int #finite element representation type
    irrpattr:int #Number of finite element representations.
    


@dataclass
class  SPROSELE:

    # key is irpsel
    nfield:int # Number of data fields on this data type
    numtype:int # Number of finite element representation types.   
    numtypes:list[TYPE]=field(default_factory=list) # finite element representation reference numbers (internal id).

    def print(self,irpsel):

        flat_list=[]
        for k in self.numtypes:
            
            flat_list.append(k.typepro)
            flat_list.append(k.irrpattr)
            

        TFEMmod=[]
      
        TFEMmod.append("SPROSELE  ")
        TFEMmod.append(f'{self.nfield:1.8E}  {irpsel:1.8E}  {self.numtype:1.8E}  {flat_list[0]:1.8E}  \n')
        if self.nfield>4:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,flat_list[1:])
            TFEMmod.append("\n")

        return TFEMmod
    
    def print_file(self,irpsel,file:str):
        TFEMmod=self.print(irpsel)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:

       
        ret:tuple[int,list[float]]=()
        
        if 'PROSELE' in line:
            data=util_func.getdata(line,fin,1)
            nfield=int(data[0]) # number of data fileds on this record

           
            irpsel=int(data[1] )  # 
            
            numtype=int(data[2] )  # 
          
            numpsels=[]
            data=util_func.getdata(line,fin,math.ceil(nfield/4))
            data=data[3::]
            
            while len(data)>0:
                
                typeprop=data[0]
                irpattr=int(data[1])

               

                pselP=TYPE(typeprop,irpattr)
                numpsels.append(pselP)
                data=data[2::]
            
           
            
                
            ret=(irpsel,[nfield,numtype,numpsels])

            return ret