from fem_interface.fem.fem_base import FEM_BASE
from collections import deque
import time

import logging
logger = logging.getLogger(__name__)


class WRITE(FEM_BASE):
  


  

    def _write_gsetmemb(self,card:str):
        TFEMmod=[]
        attribute=getattr(self,card.lower())

        for k1,v1 in attribute.items():
            for k2,v2 in v1.items():
                for k3,v3 in v2.items():
                    if v3 is not None:
                        TFEMmod.extend(v3.print(k1,k2,k3))
        return TFEMmod


    def _write_beuslo(self,card:str):
        TFEMmod=[]
        attribute=getattr(self,card.lower())

        for k1,v1 in attribute.items():
            for k2,v2 in v1.items():
                for k3,v3 in v2.items():
                    if v3 is not None:
                        TFEMmod.extend(v3.print(k1,k2,k3))
        return TFEMmod

    def _write_bello2(self,card:str):
        TFEMmod=[]
        attribute=getattr(self,card.lower())

        for k1,v1 in attribute.items():
            for k2,v2 in v1.items():
                for k3,v3 in v2.items():
                    for k4,v4 in v3.items():
                        if v4 is not None:
                            TFEMmod.extend(v4.print(k1,k2,k3,k4))
        return TFEMmod
     
    def _update_cards(self) -> None:
        """Check if each attribute is not empty and add its name to the cards list."""
        # Iterate over all attributes of the instance
        self.cards=[]
        for attr_name, attr_value in self.__dict__.items():
            # Skip the 'cards' attribute itself
            if attr_name in [ 'cards','no_cards','cards_in_fem']:
                continue
            # Check if the attribute is not empty
            if (attr_value and attr_name.islower()):
                # Add the attribute name to the 'cards' list if not already present
                if attr_name not in self.cards:
                    self.cards.append(attr_name.upper())

    

    
   
    
    def _write(self):
        self._update_cards()

        TFEMmod=[]
        for card in self.cards:
            start_time = time.time()  # Start measuring time
        
            if card=='GSETMEMB':
                TFEMmod.extend(self._write_gsetmemb(card))
                #v.print_file(k,f'{card.lower()}.fem')
            
            if card=='BEUSLO':
                TFEMmod.extend(self._write_beuslo(card))
             
            if card=='BELLO2':
                TFEMmod.extend(self._write_bello2(card))

            if card  not in ['GSETMEMB','BEUSLO','BELLO2']:    
                try:
                    attribute=getattr(self,card.lower())

                  

                    for k,v in attribute.items():
                        if v is not None:
                            TFEMmod.extend(v.print(k))
                            
                            #v.print_file(k,f'{card.lower()}.fem')
                except:
                    logger.critical(f'{card} not implemented')
            end_time = time.time()  # End measuring time
            execution_time = end_time - start_time
            logger.info(f'Execution time Write for {card}: {execution_time} seconds')
        TFEMmod.append("IEND      0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00")
        return TFEMmod
    
    def write(self,file:str)->None:
        TFEMmod=self._write()
        #_repository
        start_time = time.time()  # Start measuring time
        with open(f'{file}', "w") as text_file:
            
            for out in TFEMmod:                
                text_file.writelines(out)
        end_time = time.time()  # End measuring time
        execution_time = end_time - start_time
        logger.info(f'Execution time fro writing FEM file: {execution_time} seconds')
        logger.info(f'Fem file writen to file {file}')

    def write2(self,file:str)->None:
        TFEMmod=self._write()
        #_repository
        start_time = time.time()  # Start measuring time
        with open(f'{file}', "w",buffering=6192) as text_file:
            text_file.writelines(TFEMmod)
            
            
        end_time = time.time()  # End measuring time
        execution_time = end_time - start_time
        logger.info(f'Execution time fro writing FEM file: {execution_time} seconds')
        logger.info(f'Fem file writen to file {file}')

            

       