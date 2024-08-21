from fem_interface.fem.fem_base import FEM_BASE
from typing import Self
from fem_interface.func.func_template import FUNC_TEMPLATE
from fem_interface.fem.cards.gcoord import GCOORD
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from vectormath import Vector3
import numpy as np
import math

import logging
logger = logging.getLogger(__name__)



   

class NODE_FUNC(FEM_BASE,FUNC_TEMPLATE):

   def get_node_coordinates(self,node:int)->tuple[float,float,float]:
      return (self.gcoord[node].xcoord,self.gcoord[node].ycoord,self.gcoord[node].zcoord)
      
      


   def translate_nodes(self,trans_vector:Vector3)->None:
      for key,val in self.gcoord.items():
         self.gcoord[key]=GCOORD(val.xcoord+trans_vector.x,val.ycoord+trans_vector.y,val.zcoord+trans_vector.z)

   def get_nodes_inBox(self,p1:Point,p2:Point)->list[int]:
      selected_node=[]
      for node,value in self.gcoord.items():
         if p1.x<=float(value.xcoord)<=p2.x:
            if p1.y<=float(value.ycoord)<=p2.y:
               if p1.z<=float(value.zcoord)<=p2.z:                
                  selected_node.append(node)    
      return selected_node
   
   
   def get_nodes_in_plane(self,plane:np.ndarray,tolerance=1e-4)->list[int]:
    # Plane that P1, P2, P3 lie within
    #plane = np.array([planeEq[0], planeEq[1], planeEq[2], planeEq[3]]) # i.e. A = 2, B = -8, C = 5, D = -18
    
      nodes=[]
      for key,value in self.gcoord.items():
         pt=np.array([value.xcoord,value.ycoord,value.zcoord])
        # Compute A*pt[0] + B*pt[1] + C*pt[3] + D for each point pt in pts
        # Checks that abs(...) is below threshold (1e-6) to allow for floating point error        
         if np.abs(pt.dot(plane[:3]) - plane[3]) <= tolerance:
            nodes.append(int(key))
            
      return nodes

   
   def get_nodes_between_z_coor(self,z1:float,z2:float)->list[int]:
      selected_nodes=[]
      for node,value in self.gcoord.items():
         if z1<=float(value.zcoord)<=z2:
            selected_nodes.append(node)
      return selected_nodes
   

   
   def get_exe_nodes_inBox_vector(self,p1:Point,vec:Vector3)->list[int]:
      selected_node=[]
      p2=Point(p1.x+vec.x,p1.y+vec.y,p1.z+vec.z)
      for node,value in self.gcoord.items():
         if p1.x<=float(value.xcoord)<=p2.x:
            if p1.y<=float(value.ycoord)<=p2.y:
               if p1.z<=float(value.zcoord)<=p2.z:                
                  selected_node.append(node)
      return selected_node    
      #return [int(self.gnode[int_node].nodex) for int_node in selected_node]
   
   def get_max_min_coor(self)->dict[str,float]:
      x_tab=set()
      y_tab=set()
      z_tab=set()
      for node,value in self.gcoord.items():
         x_tab.add(value.xcoord)
         y_tab.add(value.ycoord)
         z_tab.add(value.zcoord)

      return {'min_x':min(x_tab),'max_x':max(x_tab),'min_y':min(y_tab),'max_y':max(y_tab),'min_z':min(z_tab),'max_z':max(z_tab)}
   

   def get_nodes_in_elements(self,elements:list[int])->list[int]:
      nodes=[]
      for element in elements:
         nodes.extend([node for node in self.gelmnt1[element].nodin])
      return list(set(nodes))
         
   def select_nodes_to_be_removed(self,remove_el)->list[int]:
      el_not_removed=[el for el in self.gelmnt1 if el not in remove_el]
      nodes_not_removed=self.get_nodes_in_elements(el_not_removed)
      nodes_in_removed_element=self.get_nodes_in_elements(remove_el)

      return [node for node in nodes_in_removed_element if node not in nodes_not_removed]

   def select_nodes_not_to_be_removed(self,elements_not_to_be_removed:list[int])->list[int]:

         return self.get_nodes_in_elements(elements_not_to_be_removed)
   

   def get_nodes_in_element_side(self,elnum:int,side:int)->list[int]:
      """get the nodes in element side"""


      def get_elment_side_nodes(elnum:int,side:int,elment_side_dict:dict[int,int])->list[int]:
         nodes=[]
         for el_side,indxs in elment_side_dict.items():
            if int(side) != el_side:
               continue
            for indx in indxs:
               nodes.append(self.gelmnt1[int(elnum)].nodin[indx-1])
         return nodes


         
      from fem_interface.fem.element_parameters import side_dic_20,side_dic_30,side_dic_31

      eltype=self.gelmnt1[int(elnum)].eltype

      match eltype:
         case 20:
            return get_elment_side_nodes(elnum,side,side_dic_20)
         case 30:
            return get_elment_side_nodes(elnum,side,side_dic_30)
         case 31:
            return get_elment_side_nodes(elnum,side,side_dic_31)
      




      
     
   