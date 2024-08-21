import math
from typing import IO
from dataclasses import dataclass,field
from fem_interface.fem.cards.util_func import printDataItem,getdata
from fem_interface.fem.cards import util_func
@dataclass
class SCONCEPT:
    # key is ircon
    nfield:int
    scontyp:int  # Structure concept type number (see Table 4.1)
    sconrole:int #Structure concept role number (see Table 4.2).
    irparent:int #Parent concept reference number ( or 0.0 if no parent).
    npart:int=0 # number of part concept
    njoint:int=0 # Number of joint (connection) concepts.
    irpart:list[int]=field(default_factory=list)# part concept reference numbers members
    irjoint:list[int]=field(default_factory=list)# joint concept reference numbers members

    def print(self,ircon:int)->list[str]:
        comb_ir=[]
        if len(self.irpart)>0:
            comb_ir.extend(self.irpart)
        if len(self.irjoint)>0:
            comb_ir.extend(self.irjoint)

        if (len(self.irpart)==0 and len(self.irjoint)==0):
            comb_ir.append(0)
        
        TFEMmod=[]
        TFEMmod.append("SCONCEPT  ")
        TFEMmod.append(f'{self.nfield:1.8E}  {ircon:1.8E}  {self.scontyp:1.8E}  {self.sconrole:1.8E}  \n')
        TFEMmod.append("          ")
        if self.nfield>4:
            if self.npart==None:
                self.npart=0
            if self.njoint==None:
                self.njoint=0
            
            TFEMmod.append(f'{self.irparent:1.8E}  {self.npart:1.8E}  {self.njoint:1.8E}  {comb_ir[0]:1.8E}  \n')
            
        if self.nfield>8:
            TFEMmod.append("        ")
            printDataItem(TFEMmod,comb_ir[1:])
            TFEMmod.append("\n")
        
        return TFEMmod
        

    def print_file(self,ircon,file:str):
        TFEMmod=self.print(ircon)
        util_func.append_lines_to_file(TFEMmod,file)


      





    
   
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:

        """ SCONCEPT  9.00000000E+00  3.00000000E+00  7.00000000E+00  0.00000000E+00
                      0.00000000E+00  2.00000000E+00  0.00000000E+00  8.49000000E+02
                      8.50000000E+02
            SCONCEPT  1.60000000E+01  4.00000000E+00  7.00000000E+00  0.00000000E+00
                      0.00000000E+00  9.00000000E+00  0.00000000E+00  8.51000000E+02
                      8.52000000E+02  8.53000000E+02  8.54000000E+02  8.55000000E+02
                      8.56000000E+02  8.57000000E+02  8.58000000E+02  8.59000000E+02
            SCONCEPT  1.20000000E+01  5.00000000E+00  7.00000000E+00  0.00000000E+00
                      0.00000000E+00  5.00000000E+00  0.00000000E+00  8.60000000E+02
                      8.61000000E+02  8.62000000E+02  8.63000000E+02  8.64000000E+02
          """
        ret:tuple[int,list[float]]=()
        if 'SCONCEPT' in line:
            data=getdata(line,fin,1)
            nfield=int(data[0]) # number of data fileds on this record
            ircone=int(data[1] )  # 
            
            scontyp=int(data[2] )  # 
            sconrole=int(data[3])
            
            data=getdata(line,fin,math.ceil(nfield/4))
            irparent=data[4]  # 
           
            if nfield<=5:
                ret=(ircone,[nfield,scontyp,sconrole,irparent])
                
            
            if nfield>5:
                npart=int(data[5])
                njoint=int(data[6])
                start_irpart=7
                end_irpart=7
                start_irjoint=7
                end_irjoint=7
                irpart=[]
                irjoint=[]
                if npart!=0:
                    end_irpart=start_irpart+npart
                    irpart=[int(i) for i in data[start_irpart:end_irpart]]
                    start_irjoint=end_irpart+1
                if njoint!=0:
                    end_irjoint=start_irjoint+njoint
                    irjoint=[int(i) for i in data[start_irjoint:end_irjoint]]
                
                ret=(ircone,[nfield,scontyp,sconrole,irparent,npart,njoint,irpart,irjoint])

            return ret