from dataclasses import dataclass,field
from fem_interface.fem.cards import util_func
from typing import IO
import math




@dataclass
class FEAREP:
    typrep:int #finite element representation type
    nferep:int #Number of finite element representations.
    irferep:list[int]=field(default_factory=list) #finite element representation reference numbers (internal id)


@dataclass
class SCONMESH:

    # key is ircon
    nfield:int # Number of data fields on this data type (including this field).
    numrep:int # Number of finite element representation types.   
    itemrep:list[FEAREP]=field(default_factory=list) # finite element representation reference numbers (internal id).

    def print(self,ircon):

        flat_list=[]
        for k in self.itemrep:
            
            flat_list.append(k.typrep)
            flat_list.append(k.nferep)
            flat_list.extend(k.irferep)

        TFEMmod=[]
      
        TFEMmod.append("SCONMESH  ")
        TFEMmod.append(f'{self.nfield:1.8E}  {ircon:1.8E}  {self.numrep:1.8E}  {flat_list[0]:1.8E}  \n')
        if self.nfield>4:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,flat_list[1:])
            TFEMmod.append("\n")

        """
           SCONMESH  7.00000000E+00  8.63000000E+02  1.00000000E+00  2.00000000E+00
                     2.00000000E+00  2.10000000E+01  2.20000000E+01
           SCONMESH  6.00000000E+00  8.64000000E+02  1.00000000E+00  2.00000000E+00
                     1.00000000E+00  2.00000000E+01
           SCONMESH  6.00000000E+00  8.65000000E+02  1.00000000E+00  2.00000000E+00
                     1.00000000E+00  2.70000000E+01
           SCONMESH  6.00000000E+00  8.66000000E+02  1.00000000E+00  2.00000000E+00
                     1.00000000E+00  2.80000000E+01
        """
        return TFEMmod
    
    def print_file(self,ircon,file:str):
        TFEMmod=self.print(ircon)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:

        """
          SCONMESH  9.00000000E+00  8.17900000E+03  1.00000000E+00  2.00000000E+00
                    4.00000000E+00  5.30000000E+02  5.31000000E+02  5.32000000E+02
                    5.33000000E+02

        """
        ret:tuple[int,list[float]]=()
        
        if 'SCONMESH' in line:
            data=util_func.getdata(line,fin,1)
            nfield=int(data[0]) # number of data fileds on this record

           
            ircone=int(data[1] )  # 
            
            numrep=int(data[2] )  # 
          
            numreps=[]
            data=util_func.getdata(line,fin,math.ceil(nfield/4))
            data=data[3::]
            
            while len(data)>0:
                
                typrep=data[0]
                nrep=int(data[1])

                irferep=[]
                for n in range(nrep):
                    irferep.append(data[n+2])

                feareP=FEAREP(typrep,nrep,irferep)
                numreps.append(feareP)
                data=data[nrep+2::]
            
           
            
                
            ret=(ircone,[nfield,numrep,numreps])

            return ret