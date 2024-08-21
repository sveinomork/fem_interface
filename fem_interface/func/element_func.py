from fem_interface.fem.fem_base import FEM_BASE
from typing import Self
from fem_interface.func.func_template import FUNC_TEMPLATE
from shapely.geometry import Point




class ELEMENT_FUNC(FEM_BASE,FUNC_TEMPLATE):
    def get_elements_cog(self,elements:list[int]=None)->dict[int,Point]:
        results={}

        def calculate_cog(nodes):
            total_nodes = len(nodes)
           
            cog_x = sum(self.gcoord[n].xcoord for n in nodes) / total_nodes
            cog_y = sum(self.gcoord[n].ycoord for n in nodes) / total_nodes
            cog_z = sum(self.gcoord[n].zcoord for n in nodes) / total_nodes
            return Point(cog_x, cog_y, cog_z)
        
        elements_to_process = elements if elements is not None else self.gelmnt1.keys()
        for elno in elements_to_process:
            element = self.gelmnt1[elno]
            results[elno] = calculate_cog(element.nodin)
                            
        return results
    
    def get_elements_inBox(self,p1:Point,p2:Point)->list[int]:
        selected_elements=[]
        print(f'x={p1.x},y={p1.y},z={p1.z}')
        print(f'x={p2.x},y={p2.y},z={p2.z}')
        for element,value in self.gelmnt1.items():
            return_element:bool=False
            for node in value.nodin:
                #print(f'x={self.gcoord[node].xcoord},y={self.gcoord[node].ycoord},z={self.gcoord[node].zcoord}')
                if p1.x<=float(self.gcoord[node].xcoord)<=p2.x:
                    return_element=True    
                else:
                    return_element=False
                    break
                
                if p1.y<=float(self.gcoord[node].ycoord)<=p2.y: 
                    return_element=True
                else:
                    return_element=False
                    break                    
                        
                if p1.z<=float(self.gcoord[node].zcoord)<=p2.z:
                    return_element=True
                else:
                    return_element=False
                    break        

            if return_element==True:
                selected_elements.append(element)
                return_element=False
        
        return selected_elements
    
    def get_elements_containg_nodes(self,nodes:list[int])->list[int]:
        elment=[]
        for elno,value in self.gelmnt1.items():
            for node in value.nodin:
                if int(node) in nodes:
                    elment.append(elno)
            
        return list(set(elment))
    
    
    def _get_elements_not_to_remove(self,remove_el:list[int])->list[int]:
        return [el for el in self.gelmnt1 if el not in remove_el]
    
    
    
    
    def get_element_sides(self,nodes:list[int],element)->list[int]:
      
       # Retrieve element type and node indices for the given element
        element_data = self.gelmnt1[element]
        eltype = element_data.eltype
        node_indices = element_data.nodin

        # Find surface indices that match the input nodes
        surf_indices = [index + 1 for index, node in enumerate(node_indices) if node in nodes]

       
       
        sides=[]

        from fem_interface.fem.element_parameters import side_dic_20,side_dic_30,side_dic_31

                
         # Map element types to their corresponding side dictionaries
        side_dict_map = {
        20: side_dic_20,
        30: side_dic_30,
        31: side_dic_31,
        }

        # Check if eltype exists in the map and find matching side
        if eltype in side_dict_map:
            for side, indices in side_dict_map[eltype].items():
               
                      
                if all(item in surf_indices  for item in indices)==True: 
                
                    sides.append(side)

        return sides
        # Return -1 or raise an exception if no side is found
        #raise ValueError(f"No matching side found for element {element} with nodes {nodes}")
         
        
            
         
         

            

   