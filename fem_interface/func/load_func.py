from fem_interface.fem.fem_base import FEM_BASE
from typing import Self
from fem_interface.func.func_template import FUNC_TEMPLATE
from fem_interface.func import func_geo as geo
from fem_interface.fem.cards.gcoord import GCOORD
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from vectormath import Vector3
import math
from typing import Callable, Tuple, Union
import inspect
import logging
logger = logging.getLogger(__name__)



   
from fem_interface.fem.cards.beuslo import BEUSLO


def _analysis_function(func:callable):
    signature=inspect.signature(func)
         # Extract parameters from the signature
    params = signature.parameters
    args_dict = {}
    for name, param in params.items():
        if param.default != inspect.Parameter.empty:
            args_dict[name] = param.default
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            args_dict[name] = "Keyword Arguments"
        else:
            args_dict[name] = None
    
    return args_dict



class LOAD_FUNC(FEM_BASE,FUNC_TEMPLATE):

   
    

    LoadFuncType = Callable[..., Union[float, Tuple[float, float, float]]]   


    def _process_func(self,elno:int,beusol_obj:dict[int,BEUSLO],load_func:LoadFuncType,lc_new:int,lf:float,**args_dict:dict[str,int])->None:
        for side,beu in beusol_obj.items():
            rload=[]
            nodes=self.get_nodes_in_element_side(elno,side)
            args=_analysis_function(load_func)



            #args.update({'x':x,'y':y,'z':z})
            for node in nodes:
                x,y,z=self.get_node_coordinates(node)

                local_var=locals()
                for key in args:
                    if key  in local_var:
                        args[key]=local_var[key]
                    if key in args_dict:
                        args[key]=args_dict[key]
          

                match beu.loadtyp:
                    case 1:
                        
                        rload.append(load_func(**args))

                    case 2:
                        

                        rload.extend([r*lf for r in list(load_func(**args))])
                self._init_beuslo(elno,lc_new)
                
                self.beuslo[lc_new][int(elno)][side]=BEUSLO(beu.loadtyp,beu.complx,beu.layer,beu.ndof,beu.intno,side,rload)
                

    def _init_beuslo(self,elno:int,lc_new:int)->None:

        
        if lc_new not in self.beuslo:
            self.beuslo[lc_new]={}
            
        if int(elno) not in self.beuslo[lc_new]:
            self.beuslo[lc_new][int(elno)]={}

    def _create_beuslo_base(self,loadtyp:int,complx:int,layer:int,ndof:int,intno:int):
        return BEUSLO(loadtyp=loadtyp,
                      complx=complx,
                      layer=layer,
                      ndof=ndof,
                      intno=intno,
                      side=0,
                      rload=[]

                      )

     
    def create_beuslo(self,lc:int,side:int,beusol_obj:BEUSLO,element:int,load_func:LoadFuncType|None=None,lf:float=1.0,**load_args:dict[str,float])->None:

        
        
        
        self._init_beuslo(element,lc)
       
        beu_dict={}
        beu_dict[side]=beusol_obj

   

        self._process_func(elno=element,beusol_obj=beu_dict,load_func=load_func,lc_new=lc,lf=lf,**load_args)

            
            
          
    
    def edit_beuslo(self,lc_new:int,lc_base:int,elist:list[int],load_func:LoadFuncType|None=None,lf:float=1.0,constant_load:float|None=None)->None:
        
        case= load_func is not None
        args = {"val": constant_load} if constant_load is not None else {}


        for elno,value in self.beuslo[lc_base].items():
            

            match case:
                                   
                case (True,False):
                    if int(elno) not in elist:
                        continue
                    self._init_beuslo(elno,lc_new)
                    for side,beu in self.beuslo[lc_base][int(elno)].items():
                        rload=[lf*r for r in beu.rload]

                    self.beuslo[lc_new][int(elno)][side]=BEUSLO(beu.loadtyp,beu.complx,beu.layer,beu.ndof,beu.intno,side,rload)

                case (False,True):
                   self._process_func(elno,value,load_func,side,args,lc_new,lf)

                case (False,False):
                    for side,obj in self.beuslo[lc_base][int(elno)].items():
                        rload=[lf*r for r in obj.rload]
                        self._init_beuslo(elno,lc_new)
                        self.beuslo[lc_new][int(elno)][side]=BEUSLO(obj.loadtyp,obj.complx,obj.layer,obj.ndof,obj.intno,side,rload)
                #
                case (True,True):
                    if int(elno) not in elist:
                        continue
                    self._process_func(elno,value,load_func,side,args,lc_new,lf)
                   




                


            




            
            pass


    def add_beuslo_to_plane(self,pp1:Point,pp2:Point,pp3:Point,lc:int,beusol_obj:BEUSLO,load_func:LoadFuncType|None=None,lf:float=1.0,**load_args:dict[str,float])->None:

        eq=geo.get_planeq3P(pp1,pp2,pp3)
        nodes=self.get_nodes_in_plane(eq)

        

        # get elements
        elements=self.get_elements_containg_nodes(nodes)


        for element in elements:
            nodes_in_element=list(set(self.gelmnt1[element].nodin).intersection(set(nodes)))

           

            sides=self.get_element_sides(nodes_in_element,element)
            if len(sides)==0:
                continue
            for side in sides:
                self.create_beuslo(lc=lc,side=side,beusol_obj=beusol_obj,element=element,load_func=load_func,lf=lf,**load_args)
                



   
        
    
