import pickle
from dataclasses import dataclass
from fem_interface.fem.write import WRITE
from fem_interface.fem.fem_modification import UPDATE

from fem_interface.func.node_func import NODE_FUNC
from fem_interface.func.element_func import ELEMENT_FUNC
from fem_interface.func.set_func import SET_FUNC
from fem_interface.func.load_func import LOAD_FUNC

#from fem_base import FEM_BASE
from fem_interface.fem.read import READ
@dataclass(frozen=False)
class FEM(READ,WRITE,NODE_FUNC,ELEMENT_FUNC,UPDATE,SET_FUNC,LOAD_FUNC):


    def save_obj(self,name:str)->None:
        with open(f'{name}', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
    
def load_obj(name)->FEM:   
    with open(f'{name}', 'rb') as f:
        return pickle.load(f) 

