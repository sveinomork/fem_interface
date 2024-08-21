import logging
logger = logging.getLogger(__name__)
from fem_interface.fem.fem_base import FEM_BASE
from typing import Self
from fem_interface.func.func_template import FUNC_TEMPLATE
from fem_interface.fem.cards.gcoord import GCOORD
from fem_interface.fem.cards.bnbcd import BNBCD
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from vectormath import Vector3



   

class NODE_FUNC(FEM_BASE,FUNC_TEMPLATE):
    def _add_bnbc_card(self)->None:
        if "BNBCD" not in self.cards:
            self.cards.append("BNBCD")

    
    def add_bnbc(self,nodes:list[int],fix:list[int])->None:
        self._add_bnbc_card()
        for node in nodes:
            self.bnbcd[node]=BNBCD(6,fix)
        
        
        
