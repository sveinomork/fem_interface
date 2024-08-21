from fem_interface.fem.fem_base import FEM_BASE

from typing import Self
from dataclasses import dataclass,field
import re
from itertools import islice
import os
from typing import IO
from fem_interface.fem.cards_import import *

import logging
logger = logging.getLogger(__name__)
import mmap

from fem_interface.fem.cards_import import CARDS





@dataclass
class READ(FEM_BASE):
    cards_in_fem:dict[str,int]=field(default_factory=dict)
    cards_read:dict[str,int]=field(default_factory=dict)


    PATTERN = re.compile(r'^(?=.{0,10}\b[A-Z]{1,10}[12]?\b)[A-Z]{1,10}[12]?\b')
   


   
                    
                    

    def read_fem(self,file:str)-> Self:
        """Read the Fem file and storted the data in the fem file"""
        logger.info(f'Start reading the following FEM file {file}')
        

        with open(file) as fin:
            for line in fin:          
                # get the FEM card data for each line 
                self._set_att(line,fin)
                #get the count of the cards on the fem file
                self._get_card_count_number(line=line)
        
        self._get_cards() 

        logger.info(f'Finish reading the FEM file')
        logger.info(f'The following card is not implemented and is not read')
        for card in self.no_cards:
            if card!="IEND":
                logger.info(f'{card}')
        logger.info(f'The following card count has been sucessfully read:')

        for k in self.cards:
            logger.info(f'{k} ')

    
    
    def _setup_beuslo_dict(self,name:str,line:str,fin:IO)->dict[int,dict[int,BEUSLO]]:
        attribute_dict=getattr(self,name.lower())
        g=globals()[name].create(line,fin)

        if int(g[0]) not in attribute_dict:
            attribute_dict[int(g[0])]=dict()
        if int(g[1]) not in attribute_dict[int(g[0])]:
            attribute_dict[int(g[0])][int(g[1])]=dict()

        attribute_dict[int(g[0])][int(g[1])][int(g[2])]= (globals()[name](*g[3]))

    def _setup_bello2_dict(self,name:str,line:str,fin:IO)->dict[int,dict[int,dict[int,BELLO2]]]:
        attribute_dict=getattr(self,name.lower())
        g=globals()[name].create(line,fin)
        if int(g[0]) not in getattr(self,name.lower()):
            attribute_dict=getattr(self,name.lower())
            attribute_dict[int(g[0])]=dict()
            if int(g[1]) not in attribute_dict[int(g[0])]:
                attribute_dict[int(g[0])][int(g[1])]=dict()
            if int(g[2]) not in attribute_dict[int(g[0])][int(g[1])]:
                attribute_dict[int(g[0])][int(g[1])][int(g[2])]=dict()
            attribute_dict[int(g[0])][int(g[1])][int(g[2])][int(g[3])]=globals()[name](*g[4])
            return


        
        if int(g[1]) not in attribute_dict[int(g[0])]:
            attribute_dict[int(g[0])][int(g[1])]=dict()
        if int(g[2]) not in attribute_dict[int(g[0])][int(g[1])]:
            attribute_dict[int(g[0])][int(g[1])][int(g[2])]=dict()

        attribute_dict[int(g[0])][int(g[1])][int(g[2])][int(g[3])]= (globals()[name](*g[4]))
        
    
    def _setup_gsetmemb_dict(self,name:str,line:str,fin:IO)->dict[int,list[dict[int,GSETMEMB]]]:
     

        g=globals()[name].create(line,fin)
        if int(g[0]) not in self.gsetmemb:
            
            self.gsetmemb[int(g[0])]=dict()
        if int(g[1]) not in self.gsetmemb[int(g[0])]:
            self.gsetmemb[int(g[0])][int(g[1])]=dict()

        self.gsetmemb[int(g[0])][int(g[1])][int(g[2])]=globals()[name](*g[3])
       
        

    
       
    


    
    def _setup_gen_dict(self,name:str,line:str,fin:IO)->dict[int,object]:
        """get the spesific data data for the FEM card """
        attribute_dict=getattr(self,name.lower())
        g=globals()[name].create(line,fin)
        attribute_dict[g[0]]=globals()[name](*g[1])
        return attribute_dict
    
    def _setup_gelref_dict(self,name:str,line:str,fin:IO,gelment1)->dict[int,object]:
        attribute_dict=getattr(self,name.lower())
        g=globals()[name].create(line,fin,gelment1)
        attribute_dict[g[0]]=globals()[name](*g[1])
        return attribute_dict
    
     


    
    def _set_att(self,line:str,fin:IO)->None:
               
        def name_in_line(line:str)->str:
            """check if the string in the line is a valid FEM card"""
            for name in CARDS:
                if rf'{name} 'in line:
                    return name
            return None
                
        name=name_in_line(line)

          
        if name is not None:
            
            if name=="BELLO2":
                self._setup_bello2_dict(name,line,fin)

            if name=="BEUSLO":
                self._setup_beuslo_dict(name,line,fin)
   
           
            if name=="GSETMEMB":
                self._setup_gsetmemb_dict(name,line,fin)
            
            if name=="GELREF1":
            
                self._setup_gelref_dict(name,line,fin,self.gelmnt1)
               
               
               
            # general setup     
            if name not in ['BEUSLO','GSETMEMB','BELLO2','GELREF1']:
                self._setup_gen_dict(name,line,fin)   
                

    def _get_card_count_number(self,line:str,pattern=PATTERN)->None:
        """get the count of the cards on the fem file"""
        #uppercase_word = re.findall(r'\b[A-Z]+[12]?\b', line)
        uppercase_word = pattern.findall( line)
        if len(uppercase_word) != 0:
            if uppercase_word[0] not in self.cards_in_fem:
                self.cards_in_fem[uppercase_word[0]]=1
                return None
            self.cards_in_fem[uppercase_word[0]]+=1   

    def _to_be_implemented(self,attr:list[str],card_dict:dict[str,int])->list[str]:
        """retrun a list of the cards that is on the fem file but not implemented"""
        
        return [item for item in card_dict.keys() if item not in attr  ]

    def _attribute_in_class(self)->list[str]:
        # Get all attributes of the class
        attributes = [attr.upper() for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr.startswith("_")]
        return attributes
    
    def _cards_read(self,attr:list[str],card_dict:dict[str,int])->list[str]:
        return [item for item in card_dict.keys() if item  in attr  ]

    
    def _get_cards(self)->None:
        
        
        no_cards=['PROGRAM','COMPUTER','USER','TFEMOD','IEND']
        atter=self._attribute_in_class()
        not_implemented=self._to_be_implemented(atter,self.cards_in_fem)
        no_cards.extend(not_implemented)
        self.no_cards=not_implemented
        for card in self.cards_in_fem:
            if card not in no_cards:
                self.cards.append(card) 