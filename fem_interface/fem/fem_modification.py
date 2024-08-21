
from fem_interface.fem.fem_base import FEM_BASE   
from dataclasses import dataclass
from fem_interface.fem.cards.gnode import GNODE
from fem_interface.fem.cards.gelmnt1 import GELMNT1
from fem_interface.fem.cards.gsetmemb import GSETMEMB
from fem_interface.func.func_template import FUNC_TEMPLATE
from shapely.geometry import Point
import math


import logging
logger = logging.getLogger(__name__)




@dataclass
class UPDATE(FEM_BASE,FUNC_TEMPLATE):


    def remove_elements_from_volume_from_fem_modell(self,p1:Point,p2:Point):
        elements_to_be_removed=self.get_elements_inBox(p1,p2)
        logger.info(f'Number of elements to be removed: {len(elements_to_be_removed)}')
        elements_in_model=[el for el in self.gelmnt1]
       

        elements_not_to_be_removed=list(set(elements_in_model).difference(set(elements_to_be_removed)))
        logger.info(f'The modified modell contains {len(elements_not_to_be_removed)}')
            

        nodes_not_to_be_removed=self.select_nodes_not_to_be_removed(elements_not_to_be_removed)
        
    
        new_nodes_conv=self._update_gnode(nodes_not_to_be_removed)
      
        self._update_gcoord(new_nodes_conv)
        new_element_conv=self._update_gelment1(elements_not_to_be_removed,new_nodes_conv)


      
        self._update_gelref1(new_element_conv)
      
       
        self._update_gsetmemb(new_element_conv,elements_to_be_removed,new_nodes_conv)
       
        self._update_bnbc(new_nodes_conv)
       

    def create_set_from_elemenst_in_volume(self,p1:Point,p2:Point,name:str)->None:
        elements_to_be_added=self.get_elements_inBox(p1,p2)
        num=self.find_nex_unused_set_num()
        self.create_set(num,elements_to_be_added,2,name)

        
        



    def _update_gnode(self,nodes_not_to_be_removed:list[int])->dict[int,int]:
        conv_dict={}
       
        temp_gnode={}
        for n,node in enumerate(nodes_not_to_be_removed):
            temp_gnode[n+1]=self.gnode[node]
            conv_dict[node]=n+1
        self.gnode=temp_gnode
        return conv_dict
    
    def _update_gcoord(self,node_conv_dict:dict[int,int])->None:
        temp_coord={}
        for old_node,new_node in node_conv_dict.items():
            temp_coord[new_node]=self.gcoord[old_node]
        self.gcoord=temp_coord

    def _update_gelment1(self,elements_not_to_be_removed:list[int],node_conv_dict:dict[int,int])->dict[int,int]:
        conv_dict={}
        
        temp_gelmnt1={}

        for n,element in enumerate(elements_not_to_be_removed):
            nodes=[]
            for node in self.gelmnt1[element].nodin:
                nodes.append(node_conv_dict[node])
            _gelmnt1=GELMNT1(self.gelmnt1[element].elnox,self.gelmnt1[element].eltype,self.gelmnt1[element].eltyad,nodes)

            conv_dict[element]=n+1
            
            
            temp_gelmnt1[n+1]=_gelmnt1
        self.gelmnt1=temp_gelmnt1
        return conv_dict 
    
    def _update_gelref1(self,conv_dict:dict[int,int]):
        temp_gelref={}
        for old_element,new_element in conv_dict.items():
            temp_gelref[new_element]=self.gelref1[old_element]
        
        self.gelref1=temp_gelref
    
    
    
    def _update_gsetmemb(self, 
                         element_conv:dict[int,int], elements_to_be_removed:list[int],                       
                         node_conv:dict[int,int])->None:

        _gsetmemb={}
        for isref,value1 in self.gsetmemb.items():
            
            if isref not in _gsetmemb:
                _gsetmemb[isref]={}
            
                                  
            for istype,value2 in value1.items():
                
                fem_in_set=[]
                
                for _,value3 in value2.items():
                    fem_in_set.extend([fem for fem in value3.irmemb if fem!=0])
                
                if istype==2:

                    if 0 in fem_in_set:
                        print("ss")
                    

                    elements=[element_conv[element] for element in fem_in_set if element not in elements_to_be_removed]

                
                    
                    _gsetmemb[isref][istype]=self._create_set_input_from_fem_items(istype,elements)
                
                if istype==1:
                    
                    nodes=[node_conv[node] for node in fem_in_set if node  in node_conv]
                    
                    _gsetmemb[isref][istype]=self._create_set_input_from_fem_items(istype,nodes)
        
        self.gsetmemb= _gsetmemb


    def _update_bnbc(self,nodes_conv:dict[int,int])->None:
        _bnbcd={}
        for node,value in self.bnbcd.items():
            if node  in nodes_conv:
                _bnbcd[nodes_conv[node]]=value
        
        self.bnbcd= _bnbcd            
                

    
    def _get_fem_items(self,isref:int,istype:int)->list[int]:
        fem_items=[]
        for e,v in self.gsetmemb[isref][istype].items():
            fem_items.extend(v.irmemb)
        return fem_items
        

    def _create_set_input_from_fem_items(self,istype:int,fem_items:list[int],isorgi=0)->dict[int,GSETMEMB]:
        
        nfield=1024
       

        data_storage:dict[int,GSETMEMB]={}

        irmemb=[]
        count=1
        for n,element in enumerate(fem_items):
            if n != count*(nfield-5)-1:
                irmemb.append(element)
            else:
                irmemb.append(element)
               
                data_storage[count]=GSETMEMB(nfield,istype,isorgi,irmemb)
                count+=1
                irmemb=[]
        
        if len(irmemb)>0:
            nfield=len(irmemb)
            data_storage[count]=GSETMEMB(nfield,istype,isorgi,irmemb)
        
        return data_storage
    
    
    
   



            
                
        

     
    



        
        





   