

from fem_interface.fem.fem import FEM

from vectormath import Vector3
import logging
import sys


import time
from fem_interface.compare import compare,compare2,compare3
from shapely.geometry import Point
from fem_interface.fem.cards.beuslo import BEUSLO 

def main():





    
    # setup logging
    log_file:str="log.txt"
    logging.basicConfig(                   
                    handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG) 
    logger = logging.getLogger(__name__)


   

    #setup5()
    
    fem_obj_3d=FEM()
    start_time = time.time()  # Start measuring time
    
            


    fem_obj_3d.read_fem(r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\T11.FEM')
    end_time = time.time()  # End measuring time
    execution_time = end_time - start_time
    logger.info(f'Execution time Read: {execution_time} seconds')

    beu=BEUSLO(loadtyp=2,complx=1,layer=1,ndof=18,intno=1,side=1,rload=[])
    import math
    def shear_rotate30(x,y,z):
     
    
  
        return 10000*math.sin(6.65*abs(x)),10000*math.sin(6.65*abs(y)),z




    def linz(z,value):
        if z<151.9359911:
            return value*(151.9359911-z)
        else:
            return 0
        
    p1=Point(5.245,-1.5,1.8)
    p2=Point(5.245,0.0,1.8)
    p3=Point(-0.145,-1.5,1.8)

    a=fem_obj_3d.gelmnt1[2767].nodin
    v=fem_obj_3d.get_elements_containg_nodes(a)

    sa=fem_obj_3d.get_element_sides(a,2767)

    print("all")

    fem_obj_3d.add_beuslo_to_plane(p1,p2,p3,1,beu,shear_rotate30)
    #fem_obj_3d.create_beuslo(1,1,beu,1,linz,value=1)
    fem_obj_3d.write(f'T11.FEM')
    



    


    fem_obj_3d.translate_nodes(Vector3(1,1,1))
    
    start_time = time.time()  # Start measuring time
    #filename=r'C:\DNVGL\STEPnSUPER\T51.FEM'
    fem_obj_3d.write2(f'T11.FEM')
    end_time = time.time()  # End measuring time
    execution_time = end_time - start_time
    logger.info(f'Execution time Write: {execution_time} seconds')


    fem_obj_3d.save_obj("nka.pkl")
    print("test")

   
    print("stopp")

def add_xtract_el(name:str,supnum:int,elements:list[int],out_file:str):
    #et new "New set (292)"
    #New set "New set (292)" created
    #Set name "New set (292)" ""
    #Name (and description) of current set changed.
    #Set "New set (292)" updated.
    #set addelements "SEL21.IND1" 432423
    #Set "New set (292)" updated.
    #233set addelements "SEL21.IND1" 432423
    out_list=[]
    out_list.append(f'set new "{name}"\n')
    out_list.append(f'set name "{name}" "{name}"')
    for element in elements:
        out_list.append(f'set addelements "SEL{supnum}.IND1" {element}\n')

    with open(f'{out_file}', "w") as text_file:
            
            for out in out_list:                
                text_file.writelines(out)

def get_sum_force(fem_obj:FEM,res_dict:dict[int,float],nodes:list[int],lc:int)->float:
        
        conv_dict={v.nodex:k for k,v in fem_obj.gnode.items()}
        t_list=[]
        for k,v in res_dict.items():
            if k not in conv_dict:
                print(f"Waring {k} don't exist")
                continue
            if int(conv_dict[k]) in nodes:
                t_list.append(v[lc-1])
        return sum(t_list)  

from fem_interface.support import read_sestra,get_sum_force, combine_force,save_obj,calc_support_reaction

def comb_forces_i(init:dict[int,float],final:dict[int,list[float]])->float:
    init_1=0
    final_1=0
    final_2=0
    for k,v in init.items():
        init_1+=v[0]
    
    for k,v in final.items():
        final_1+=v[0]
        final_2+=v[1]
    #force_in+force_tot_2-force_tot_1
    return init_1+final_2-final_1



def setup5():
    ses_final=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\sestra.lis'
    ses_init=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Initial\sestra.lis'

    init_21=read_sestra(ses_init,21)
    init_22=read_sestra(ses_init,22)
    init_11=read_sestra(ses_init,11)
    init_12=read_sestra(ses_init,12)
    init_50=read_sestra(ses_init,50)

    
    init_50_1=0
    for k,v in init_50.items():
        init_50_1+=v[0]

    final_21=read_sestra(ses_final,21)
    final_22=read_sestra(ses_final,22)
    final_11=read_sestra(ses_final,11)
    final_12=read_sestra(ses_final,12)
    final_50=read_sestra(ses_final,50)

    final_50_1=0
    final_50_2=0
    for k,v in final_50.items():
        final_50_1+=v[0]
        final_50_2+=v[1]
    
    total_sum=comb_forces_i(init_11,final_11) +comb_forces_i(init_12,final_12) +comb_forces_i(init_21,final_21) +comb_forces_i(init_22,final_22)+comb_forces_i(init_50,final_50)



    fem_file_11=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\T11.FEM'
    fem_file_12=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\T12.FEM'
    fem_file_21=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\T21.FEM'
    fem_file_22=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\T22.FEM'
    fem_file_22=r'Y:\Shared\SunRise_Common\STEPnSUPER_T200N\Final\T50.FEM'
    fem_11=FEM()
    fem_11.read_fem(fem_file_11)

    
    fem_12=FEM()
    fem_12.read_fem(fem_file_12)

    fem_21=FEM()
    fem_21.read_fem(fem_file_21)

    fem_22=FEM()
    fem_22.read_fem(fem_file_22)

    p_12_11=Point(-0.29,-2.74,-0.78)
    p_12_21=Point(3.04,-2.74,-0.78)
    p_12_12=Point(-0.29,-0.32,-0.78)
    p_12_22=Point(3.04,-0.32,-0.78)
    v_12=Vector3(3.65-3.04,-2.12+2.74,0.02)

    p_12_c=Point(1.35,-2.01,-0.81)
    v_12_c=Vector3(2.91-1.35,-0.47+2.01,0.02)



    p_11_12=Point(-0.29,2.12,-0.78)
    p_11_22=Point(3.04,2.12,-0.78)
    p_11_11=Point(-0.29,-0.28,-0.78)
    p_11_21=Point(3.04,-0.28,-0.78)
    v_11=Vector3(3.65-3.04,-2.12+2.74,0.02)

    p_11_c=Point(1.35,0.45,-0.81)
    v_11_c=Vector3(2.91-1.35,-0.47+2.01,0.02)

    p_22_11=Point(-3.31,-1.51,-2.58)
    p_22_21=Point(-3.31, 0.89,-2.58)
    p_22_12=Point(2.69,-1.51,-2.58)
    p_22_22=Point(2.69, 0.89,-2.58)
    p_22_c=Point(-0.81,-0.81,-2.58)

    v_22=Vector3(3.31-2.74,0.62,0.02)
    v_22_c=Vector3(1.62,1.62,0.02)


    p_21_11=Point(-3.31,-1.51,-2.58)
    p_21_21=Point(-3.31, 0.89,-2.58)
    p_21_12=Point(2.69,-1.51,-2.58)
    p_21_22=Point(2.69, 0.89,-2.58)
    p_21_c=Point(-0.81,-0.81,-2.58)

    v_21=Vector3(3.31-2.74,0.62,0.02)
    v_21_c=Vector3(1.62,1.62,0.02)


    sup12_11=fem_12.get_exe_nodes_inBox_vector(p_12_11,v_12)
    sup12_12=fem_12.get_exe_nodes_inBox_vector(p_12_12,v_12)
    sup12_21=fem_12.get_exe_nodes_inBox_vector(p_12_21,v_12)
    sup12_22=fem_12.get_exe_nodes_inBox_vector(p_12_22,v_12)
    sup12_c=fem_12.get_exe_nodes_inBox_vector(p_12_c,v_12_c)

    #same geometry for 12 and 11, thefore using points for 12
    sup11_11=fem_11.get_exe_nodes_inBox_vector(p_11_11,v_11)
    sup11_12=fem_11.get_exe_nodes_inBox_vector(p_11_12,v_11)
    sup11_21=fem_11.get_exe_nodes_inBox_vector(p_11_21,v_11)
    sup11_22=fem_11.get_exe_nodes_inBox_vector(p_11_22,v_11)
    sup11_c=fem_11.get_exe_nodes_inBox_vector(p_11_c,v_11_c)

   
    sup22_11=fem_22.get_exe_nodes_inBox_vector(p_22_11,v_22)
    sup22_12=fem_22.get_exe_nodes_inBox_vector(p_22_12,v_22)
    sup22_21=fem_22.get_exe_nodes_inBox_vector(p_22_21,v_22)
    sup22_22=fem_22.get_exe_nodes_inBox_vector(p_22_22,v_22)
    sup22_c=fem_22.get_exe_nodes_inBox_vector(p_22_c,v_22_c)

    sup21_11=fem_21.get_exe_nodes_inBox_vector(p_21_11,v_21)
    sup21_12=fem_21.get_exe_nodes_inBox_vector(p_21_12,v_21)
    sup21_21=fem_21.get_exe_nodes_inBox_vector(p_21_21,v_21)
    sup21_22=fem_21.get_exe_nodes_inBox_vector(p_21_22,v_21)
    sup21_c=fem_21.get_exe_nodes_inBox_vector(p_21_c,v_21_c)


    

    res_12_11=calc_support_reaction(fem_12,init_12,final_12,sup12_11)
    res_12_12=calc_support_reaction(fem_12,init_12,final_12,sup12_12)
    res_12_21=calc_support_reaction(fem_12,init_12,final_12,sup12_21)
    res_12_22=calc_support_reaction(fem_12,init_12,final_12,sup12_22)
    res_12_c=calc_support_reaction(fem_12,init_12,final_12,sup12_c)

    print("-----------T12--------------")
    st_12_11=f'Element 12  11 {res_12_11}'
    st_12_12=f'Element 12  12 {res_12_12}'
    st_12_21=f'Element 12  21 {res_12_21}'
    st_12_22=f'Element 12  22 {res_12_22}'
    st_12_c = f'Element 12 center {res_12_c}'

    print(st_12_11)
    print(st_12_12)
    print(st_12_21)
    print(st_12_22)
    print(st_12_c)
    print("-------------------------")
    
    
    res_11_11=calc_support_reaction(fem_11,init_11,final_11,sup11_11)
    res_11_12=calc_support_reaction(fem_11,init_11,final_11,sup11_12)
    res_11_21=calc_support_reaction(fem_11,init_11,final_11,sup11_21)
    res_11_22=calc_support_reaction(fem_11,init_11,final_11,sup11_22)
    res_11_c=calc_support_reaction(fem_11,init_11,final_11,sup11_c)

    st_11_11=f'Element 11  11 {res_11_11}'
    st_11_12=f'Element 11  12 {res_11_12}'
    st_11_21=f'Element 11  21 {res_11_21}'
    st_11_22=f'Element 11  22 {res_11_22}'
    st_11_c = f'Element 11 center {res_11_c}'
    
    print("-----------T11--------------")
    print(st_11_11)
    print(st_11_12)
    print(st_11_21)
    print(st_11_22)
    print(st_11_c)
    print("-------------------------")



    res_22_11=calc_support_reaction(fem_22,init_22,final_22,sup22_11)
    res_22_12=calc_support_reaction(fem_22,init_22,final_22,sup22_12)
    res_22_21=calc_support_reaction(fem_22,init_22,final_22,sup22_21)
    res_22_22=calc_support_reaction(fem_22,init_22,final_22,sup22_22)
    res_22_c=calc_support_reaction(fem_22,init_22,final_22,sup22_c)


    print("-----------T22--------------")
    st_22_11=f'Element 22  11 {res_22_11}'
    st_22_12=f'Element 22  12 {res_22_12}'
    st_22_21=f'Element 22  21 {res_22_21}'
    st_22_22=f'Element 22  22 {res_22_22}'
    st_22_c = f'Element 22 center {res_22_c}'

    print(st_22_11)
    print(st_22_12)
    print(st_22_21)
    print(st_22_22)
    print(st_22_c)
    print("-------------------------")

    res_21_11=calc_support_reaction(fem_21,init_21,final_21,sup21_11)
    res_21_12=calc_support_reaction(fem_21,init_21,final_21,sup21_12)
    res_21_21=calc_support_reaction(fem_21,init_21,final_21,sup21_21)
    res_21_22=calc_support_reaction(fem_21,init_21,final_21,sup21_22)
    res_21_c=calc_support_reaction(fem_21,init_21,final_21,sup21_c)

    print("-----------T21--------------")
    st_21_11=f'Element 21  11 {res_21_11}'
    st_21_12=f'Element 21  12 {res_21_12}'
    st_21_21=f'Element 21  21 {res_21_21}'
    st_21_22=f'Element 21  22 {res_21_22}'
    st_21_c = f'Element 21 center {res_21_c}'

    print(st_21_11)
    print(st_21_12)
    print(st_21_21)
    print(st_21_22)
    print(st_21_c)
    print("-------------------------")



    print("stopp")
    





def setup4():
    
   
    file_final=r'Y:\Shared\SunRise_Common\STEPnSUPER\Final\SESTRA.LIS'
    #file_init=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\SESTRA.LIS'
    #file_init=r'C:\DNVGL\Workspaces\upd_super\pres_init\SESTRA.LIS'
    file_init=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\SESTRA.LIS'

    init_21=read_sestra(file_init,21)
    init_11=read_sestra(file_init,11)
    init_61=read_sestra(file_init,61)


    final_21=read_sestra(file_final,21)
    final_11=read_sestra(file_final,11)
    final_61=read_sestra(file_final,61)

       
    
    fem_21=FEM()
    fem_11=FEM()
    fem_61=FEM()
  
    #filename1=r'C:\DNVGL\Workspaces\ReactionTest\T9.FEM' 
    #filename1=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\T21.FEM'
    filename_21=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\T21.FEM'
    filename_11=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\T11.FEM'
    filename_61=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\T61.FEM'

    #filename_21=r'C:\DNVGL\Workspaces\upd_super\pres_init\T21.FEM'
    #filename_11=r'C:\DNVGL\Workspaces\upd_super\pres_init\T11.FEM'

    
    fem_21.read_fem(filename_21)
    
    fem_21.translate_nodes(Vector3(23.1,1.2,0))
    fem_11.read_fem(filename_11)
    fem_11.translate_nodes(Vector3(0,0,-1.8))
    fem_61.read_fem(filename_61)
    fem_61.translate_nodes(Vector3(56.055, -0.03,-1.8))

    fem_21.save_obj("obj_21.pkl")
    #fem_21=load_obj("obj_21.pkl")
    fem_11.save_obj("obj_11.pkl")
    #fem_11=load_obj("obj_11.pkl")


    tran_x=0
    tran_y=0

    p1x=-0.29
    p1y=-0.29

    p2x=-0.29
    p2y=2.12

    p3x=3.04
    p3y=2.12

    p4x=3.04
    p4y=-0.29




      
    p01x=2.6+tran_x
    p02x=2.6+tran_x
    p01y=-1.5+tran_y

    p02y=0.8+tran_y
    p03x=-3.4+tran_x

    p04x=-3.4+tran_x
    p03y=-1.5+tran_y
    p04y=0.8+tran_y
    pxz=-2.6
    pxz11=-0.79
    vect=Vector3(1,1,0.03)
    p_circ=Point(-1+tran_x,-1+tran_y,pxz)

    p11_circ=Point(1.32,0.42,-0.79)


    p21_1=Point(p01x,p01y,pxz)
    print(p21_1)
    p21_2=Point(p02x,p02y,pxz)
    p21_3=Point(p03x,p03y,pxz)
    p21_4=Point(p04x,p04y,pxz)
    p21_5=p_circ

    p11_1=Point(p1x,p1y,pxz11)
    p11_2=Point(p2x,p2y,pxz11)
    p11_3=Point(p3x,p3y,pxz11)
    p11_4=Point(p4x,p4y,pxz11)
    p11_5=p11_circ

    p61_1=Point(1.54,-0.29,-0.78)
    p61_2=Point(1.54,2.1,-0.78)
    p61_3=Point(4.1,-0.29,-0.78)
    p61_4=Point(4.1,2.1,-0.78)
    p61_5=Point(2.2,0.4,-0.78)



    sup21_1=fem_21.get_exe_nodes_inBox_vector(Point(p01x,p01y,pxz),vect)
    sup21_2=fem_21.get_exe_nodes_inBox_vector(Point(p02x,p02y,pxz),vect)

    sup21_3=fem_21.get_exe_nodes_inBox_vector(Point(p03x,p03y,pxz),vect)
    sup21_4=fem_21.get_exe_nodes_inBox_vector(Point(p04x,p04y,pxz),vect)

    sup21_5=fem_21.get_exe_nodes_inBox_vector(p_circ,Vector3(2,2,0.03))

    sup11_1=fem_11.get_exe_nodes_inBox_vector(Point(p1x,p1y,pxz11),vect)
    sup11_2=fem_11.get_exe_nodes_inBox_vector(Point(p2x,p2y,pxz11),vect)
    sup11_3=fem_11.get_exe_nodes_inBox_vector(Point(p3x,p3y,pxz11),vect)
    sup11_4=fem_11.get_exe_nodes_inBox_vector(Point(p4x,p4y,pxz11),vect)
    sup11_5=fem_11.get_exe_nodes_inBox_vector(p11_circ,Vector3(1.8,1.8,0.03))

    sup61_1=fem_61.get_exe_nodes_inBox_vector(Point(1.54,-0.29,-0.78),vect)
    sup61_2=fem_61.get_exe_nodes_inBox_vector(Point(1.54,2.1,-0.78),vect)
    sup61_3=fem_61.get_exe_nodes_inBox_vector(Point(4.1,-0.29,-0.78),vect)
    sup61_4=fem_61.get_exe_nodes_inBox_vector(Point(4.1,2.1,-0.78),vect)
    sup61_5=fem_61.get_exe_nodes_inBox_vector(Point(2.2,0.4,-0.78),Vector3(1.8,1.8,0.3))

    sup11_a=fem_11.get_exe_nodes_inBox_vector(Point(-100,-100,-2.58),Vector3(200,200,0.03))
    sup21_a=fem_21.get_exe_nodes_inBox_vector(Point(-100,-100,-2.58),Vector3(200,200,0.03))
    sup61_a=fem_61.get_exe_nodes_inBox_vector(Point(-100,-100,-2.58),Vector3(200,200,0.03))


    e=[]
    f=[]
    import numpy as np
    for n in sup11_a:
        f.append(n)
        e.append(np.array([fem_11.gcoord[n].xcoord,fem_11.gcoord[n].ycoord,n,11]))

    for n in sup21_a:
        f.append(n)
        e.append(np.array([fem_21.gcoord[n].xcoord,fem_21.gcoord[n].ycoord,n,21]))
    
    for n in sup61_a:
        f.append(n)
        e.append(np.array([fem_61.gcoord[n].xcoord,fem_61.gcoord[n].ycoord,n,61]))


    



    save_obj(e,rf'C:\DNV\at1.pkl')



    a=automatic_grouping_of_point(e,0.5)

    conv_dict_21={v.nodex:k for k,v in fem_21.gnode.items()}
    conv_dict_11={v.nodex:k for k,v in fem_11.gnode.items()}
    conv_dict_61={v.nodex:k for k,v in fem_61.gnode.items()}



    ea21_1= combine_force(conv_dict_21,init_21,final_21,sup21_1)
    ea21_2= combine_force(conv_dict_21,init_21,final_21,sup21_2)
    ea21_3= combine_force(conv_dict_21,init_21,final_21,sup21_3)
    ea21_4= combine_force(conv_dict_21,init_21,final_21,sup21_4)
    ea21_5= combine_force(conv_dict_21,init_21,final_21,sup21_5)


    ea11_1= combine_force(conv_dict_11,init_11,final_11,sup11_1)
    ea11_2= combine_force(conv_dict_11,init_11,final_11,sup11_2)
    ea11_3= combine_force(conv_dict_11,init_11,final_11,sup11_3)
    ea11_4= combine_force(conv_dict_11,init_11,final_11,sup11_4)
    ea11_5= combine_force(conv_dict_11,init_11,final_11,sup11_5)

    ea61_1= combine_force(conv_dict_61,init_61,final_61,sup61_1)
    ea61_2= combine_force(conv_dict_61,init_61,final_61,sup61_2)
    ea61_3= combine_force(conv_dict_61,init_61,final_61,sup61_3)
    ea61_4= combine_force(conv_dict_61,init_61,final_61,sup61_4)
    ea61_5= combine_force(conv_dict_61,init_61,final_61,sup61_5)

    print(f'{21} {p21_1}  {ea21_1:.2f}')
    print(f'{21} {p21_2}  {ea21_2:.2f}')
    print(f'{21} {p21_3}  {ea21_3:.2f}')
    print(f'{21} {p21_4}  {ea21_4:.2f}')
    print(f'{21} {p21_5}  {ea21_5:.2f}')

    print(f'{11} {p11_1}  {ea11_1:.2f}')
    print(f'{11} {p11_2}  {ea11_2:.2f}')
    print(f'{11} {p11_3}  {ea11_3:.2f}')
    print(f'{11} {p11_4}  {ea11_4:.2f}')
    print(f'{11} {p11_5}  {ea11_5:.2f}')

    print(f'{61} {p61_1}  {ea61_1:.2f}')
    print(f'{61} {p61_2}  {ea61_2:.2f}')
    print(f'{61} {p61_3}  {ea61_3:.2f}')
    print(f'{61} {p61_4}  {ea61_4:.2f}')
    print(f'{61} {p61_5}  {ea61_5:.2f}')
    


    


    






    print("stopp")
    
    pass


def setup3():
    init_dict_21=dict()
    final_dict_21=dict()

    init_dict_11=dict()
    final_dict_11=dict()

    init_dict_50=dict()
    final_dict_50=dict()

    file_final=r'Y:\Shared\SunRise_Common\STEPnSUPER\Final\SESTRA.LIS'
    #file_init=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\SESTRA.LIS'
    file_init=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\SESTRA.LIS'
    
    #file_final=r'C:\DNVGL\Workspaces\upd_super\presel_final\SESTRA.LIS'
    #file_init=r'C:\DNVGL\Workspaces\upd_super\pres_init\SESTRA.LIS'

    def read_sestra(file:str,sup_id:int):
        in_dict=dict()
        with open(file_init, 'r') as f1:
            for line in f1:
                data=line.split()
                if len(data)==4:
                    if data[0].strip()=="21":

                        if int(float(data[2])) not in init_dict_21:
                            init_dict_21[int(float(data[2]))]=float(data[3])




    with open(file_init, 'r') as f1:
        for line in f1:
            data=line.split()
            if len(data)==4:
                if data[0].strip()=="21":

                    if int(float(data[2])) not in init_dict_21:
                        init_dict_21[int(float(data[2]))]=float(data[3])


            if len(data)==4:
                if data[0].strip()=="11":

                    if int(float(data[2])) not in init_dict_11:
                        init_dict_11[int(float(data[2]))]=float(data[3])

            if len(data)==4:
                if data[0].strip()=="50":

                    if int(float(data[2])) not in init_dict_50:
                        init_dict_50[int(float(data[2]))]=float(data[3])

    to_init_1=sum([i for i in init_dict_50.values()]) 





    
    with open(file_final, 'r') as f1:
        for line in f1:
            data=line.split()
            
            if len(data)==4:
                if data[0].strip()=="21":

                  

                    if int(float(data[2])) not in final_dict_21:
                        final_dict_21[int(float(data[2]))]=[]

                    
                    
                    final_dict_21[int(float(data[2]))].append(float(data[3]))

                if data[0].strip()=="11":

                  

                    if int(float(data[2])) not in final_dict_11:
                        final_dict_11[int(float(data[2]))]=[]

                    
                    
                    final_dict_11[int(float(data[2]))].append(float(data[3]))


                if data[0].strip()=="50":

                  

                    if int(float(data[2])) not in final_dict_50:
                        final_dict_50[int(float(data[2]))]=[]

                    
                    
                    final_dict_50[int(float(data[2]))].append(float(data[3]))
    to_final_1=sum([i[0] for i in final_dict_50.values()])   
    to_final_2=sum([i[1] for i in final_dict_50.values()]) 



    fem_21=FEM()
    fem_11=FEM()
  
    #filename1=r'C:\DNVGL\Workspaces\ReactionTest\T9.FEM' 
    #filename1=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\T21.FEM'
    filename_21=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\T21.FEM'
    filename_11=r'Y:\Shared\SunRise_Common\STEPnSUPER\Initial\T11.FEM'
    fem_21.read_fem(filename_21)
    fem_11.read_fem(filename_11)
    tran_x=0
    tran_y=0

    p1x=-0.29
    p1y=-0.29

    p2x=-0.29
    p2y=2.12

    p3x=3.04
    p3y=2.12

    p4x=3.04
    p4y=-0.29




      
    p01x=2.6+tran_x
    p02x=2.6+tran_x
    p01y=-1.5+tran_y

    p02y=0.8+tran_y
    p03x=-3.4+tran_x

    p04x=-3.4+tran_x
    p03y=-1.5+tran_y
    p04y=0.8+tran_y
    pxz=-2.6
    pxz11=-0.79
    vect=Vector3(1,1,0.03)
    p_circ=Point(-1+tran_x,-1+tran_y,pxz)

    p11_circ=Point(1.32,0.42,pxz11)

    sup1=fem_21.get_exe_nodes_inBox_vector(Point(p01x,p01y,pxz),vect)
    sup2=fem_21.get_exe_nodes_inBox_vector(Point(p02x,p02y,pxz),vect)

    sup3=fem_21.get_exe_nodes_inBox_vector(Point(p03x,p03y,pxz),vect)
    sup4=fem_21.get_exe_nodes_inBox_vector(Point(p04x,p04y,pxz),vect)

    sup5=fem_21.get_exe_nodes_inBox_vector(p_circ,Vector3(2,2,0.03))

    sup11_1=fem_11.get_exe_nodes_inBox_vector(Point(p1x,p1y,pxz11),vect)
    sup11_2=fem_11.get_exe_nodes_inBox_vector(Point(p2x,p2y,pxz11),vect)
    sup11_3=fem_11.get_exe_nodes_inBox_vector(Point(p3x,p3y,pxz11),vect)
    sup11_4=fem_11.get_exe_nodes_inBox_vector(Point(p4x,p4y,pxz11),vect)
    sup11_5=fem_11.get_exe_nodes_inBox_vector(p11_circ,Vector3(1.8,1.8,0.03))

    sup11_a=fem_11.get_exe_nodes_inBox_vector(Point(-100,-100,pxz11),Vector3(200,200,0.03))




    # p2= (500,500,-2.1)
    print(f'Len {len(sup1)}')


    test_dict_11={v.nodex:k for k,v in fem_11.gnode.items()}

    test_dict_21={v.nodex:k for k,v in fem_21.gnode.items()}

   

    t211_list1=[]
    t211_list2=[]
    t211_list3=[]
    t211_list4=[]
    t211_list5=[]

    t212_list1=[]
    t212_list2=[]
    t212_list3=[]
    t212_list4=[]
    t212_list5=[]

   



    for k,v in final_dict_21.items():
        #print(f'Check {k}{fem_1.gcoord[k]}')
        #print(f'Check {k}{fem_1.gcoord[test_dict[k]]}')
        if int(test_dict_21[k]) in sup1:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t211_list1.append(v[0])
            t212_list1.append(v[1])
        if int(test_dict_21[k]) in sup2:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t211_list2.append(v[0])
            t212_list2.append(v[1])
        if int(test_dict_21[k]) in sup3:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t211_list3.append(v[0])
            t212_list3.append(v[1])
        if int(test_dict_21[k]) in sup4:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t211_list4.append(v[0])
            t212_list4.append(v[1])
        if int(test_dict_21[k]) in sup5:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t211_list5.append(v[0])
            t212_list5.append(v[1])
   

    st_1=f'Support point at pos  {p01x}  {p01y} -> {sum(t211_list1):.2f} -> {sum(t212_list1):.2f}'
    st_2=f'Support point at pos {p01x}  {p02y} -> {sum(t211_list2):.2f} -> {sum(t212_list2):.2f}'
    st_3=f'Support point at pos {p01x}  {p03y} -> {sum(t211_list3):.2f} -> {sum(t212_list3):.2f}'
    st_4=f'Support point at pos {p01x}  {p04y} -> {sum(t211_list4):.2f} -> {sum(t212_list4):.2f}'
    st_5=f'Support point at pos {p_circ.x}  {p_circ.y} -> {sum(t211_list5):.2f} -> {sum(t212_list5):.2f}'



    t111_list1=[]
    t111_list2=[]
    t111_list3=[]
    t111_list4=[]
    t111_list5=[]
    t111_a=[]

    t112_list1=[]
    t112_list2=[]
    t112_list3=[]
    t112_list4=[]
    t112_list5=[]
    t112_a=[]


    for k,v in final_dict_11.items():
        #print(f'Check {k}{fem_1.gcoord[k]}')
        #print(f'Check {k}{fem_1.gcoord[test_dict[k]]}')
        if int(test_dict_11[k]) in sup11_1:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t111_list1.append(v[0])
            t112_list1.append(v[1])
        if int(test_dict_11[k]) in sup11_2:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t111_list2.append(v[0])
            t112_list2.append(v[1])
        if int(test_dict_11[k]) in sup11_3:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t111_list3.append(v[0])
            t112_list3.append(v[1])
        if int(test_dict_11[k]) in sup11_4:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t111_list4.append(v[0])
            t112_list4.append(v[1])
        if int(test_dict_11[k]) in sup11_5:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            t111_list5.append(v[0])
            t112_list5.append(v[1])

        if int(test_dict_11[k]) in sup11_a:
            t111_a.append(v[0])
            t112_a.append(v[1])

   

    st_11_1=f'Support point at pos  {p01x}  {p01y} -> {sum(t111_list1):.2f} -> {sum(t112_list1):.2f}'
    st_11_2=f'Support point at pos {p01x}  {p02y} -> {sum(t111_list2):.2f} -> {sum(t112_list2):.2f}'
    st_11_3=f'Support point at pos {p01x}  {p03y} -> {sum(t111_list3):.2f} -> {sum(t112_list3):.2f}'
    st_11_4=f'Support point at pos {p01x}  {p04y} -> {sum(t111_list4):.2f} -> {sum(t112_list4):.2f}'
    st_11_5=f'Support point at pos {p_circ.x}  {p_circ.y} -> {sum(t111_list5):.2f} -> {sum(t112_list5):.2f}'



   
    
    i_list1=[]
    i_list2=[]
    i_list3=[]
    i_list4=[]
    i_list5=[]
    for k,v in init_dict_21.items():
        #print(f'Check {k}{fem_1.gcoord[k]}')
        #print(f'Check {k}{fem_1.gcoord[test_dict[k]]}')
        if int(test_dict_21[k]) in sup1:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i_list1.append(v)
        if int(test_dict_21[k]) in sup2:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i_list2.append(v)
        if int(test_dict_21[k]) in sup3:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i_list3.append(v)
        if int(test_dict_21[k]) in sup4:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i_list4.append(v)
        if int(test_dict_21[k]) in sup5:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i_list5.append(v)

       
    print(len(i_list1))
    print(len(i_list2))
    print(len(i_list3))
    print(len(i_list4))
    print(len(i_list5))

    sti_1=f'Support point at pos  {p01x}  {p01y} -> {sum(i_list1):.2f}'
    sti_2=f'Support point at pos {p02x}  {p02y} -> {sum(i_list2):.2f}'
    sti_3=f'Support point at pos {p03x}  {p03y} -> {sum(i_list3):.2f}'
    sti_4=f'Support point at pos {p04x}  {p04y} -> {sum(i_list4):.2f}'
    sti_5=f'Support point at pos {p_circ.x}  {p_circ.y} -> {sum(i_list5):.2f}'



    i11_list1=[]
    i11_list2=[]
    i11_list3=[]
    i11_list4=[]
    i11_list5=[]
    i11_a=[]
    for k,v in init_dict_11.items():
        #print(f'Check {k}{fem_1.gcoord[k]}')
        #print(f'Check {k}{fem_1.gcoord[test_dict[k]]}')
        if int(test_dict_11[k]) in sup11_1:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i11_list1.append(v)
        if int(test_dict_11[k]) in sup11_2:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i11_list2.append(v)
        if int(test_dict_11[k]) in sup11_3:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i11_list3.append(v)
        if int(test_dict_11[k]) in sup11_4:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i11_list4.append(v)
        if int(test_dict_11[k]) in sup11_5:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i11_list5.append(v)
        if int(test_dict_11[k]) in sup11_a:
            #print( f' Inter_node1:{k}  {fem_1.gcoord[test_dict[k]]}')
            i11_a.append(v)
    print(len(i11_list1))
    print(len(i11_list2))
    print(len(i11_list3))
    print(len(i11_list4))
    print(len(i11_list5))

    sti11_1=f'Support point at pos  {p01x}  {p01y} -> {sum(i11_list1):.2f}'
    sti11_2=f'Support point at pos {p02x}  {p02y} -> {sum(i11_list2):.2f}'
    sti11_3=f'Support point at pos {p03x}  {p03y} -> {sum(i11_list3):.2f}'
    sti11_4=f'Support point at pos {p04x}  {p04y} -> {sum(i11_list4):.2f}'
    sti11_5=f'Support point at pos {p_circ.x}  {p_circ.y} -> {sum(i11_list5):.2f}'





  

    print(f'{sum(i_list1)+sum(t212_list1)-sum(t211_list1)} {p01x} {p01y}')
    print(f'{sum(i_list2)+sum(t212_list2)-sum(t211_list2)} {p02x} {p02y}')
    print(f'{sum(i_list3)+sum(t212_list3)-sum(t211_list3)} {p03x} {p03y}')
    print(f'{sum(i_list4)+sum(t212_list4)-sum(t211_list4)} {p04x} {p04y}')
    print(sum(i_list5)+sum(t212_list5)-sum(t211_list5))


    print(f'{sum(i11_list1)+sum(t112_list1)-sum(t111_list1)} {p1x} {p1y} ')
    print(f'{sum(i11_list2)+sum(t112_list2)-sum(t111_list2)} {p2x} {p2y} ')
    print(f'{sum(i11_list3)+sum(t112_list3)-sum(t111_list3)} {p3x} {p3y} ')
    print(f'{sum(i11_list4)+sum(t112_list4)-sum(t111_list4)} {p4x} {p4y} ')

    print(f'{sum(i11_list5)}')
    print(sum(i11_list5)+sum(t112_list5)-sum(t111_list5))
    print(sum(i11_a)+sum(t112_a)-sum(t111_a))

    print(to_init_1+to_final_2-to_final_1)


    print(sum(t112_a)+to_final_2)
    print("stopp")


    


def setup2():
    restul_dict=dict()
    file1=r'C:\DNVGL\Workspaces\ReactionTest\SESTRA.LIS' 
    #file1=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\SESTRA.LIS'
    with open(file1, 'r') as f1:
        for line in f1:
            data=line.split()
            if len(data)==4:
                if data[0].strip()=="9":

                    if int(float(data[2])) not in restul_dict:
                        restul_dict[int(float(data[2]))]=float(data[3])

    print(len(restul_dict))

    fem_1=FEM()
  
    filename1=r'C:\DNVGL\Workspaces\ReactionTest\T9.FEM' 
    #filename1=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\T21.FEM'

    fem_1.read_fem(filename1)

    #for k,v in restul_dict.items():
        
    #    print( f' Inter_node:{k}  {fem_1.gcoord[fem_1.gnode[k].nodex]}')

    sup1=fem_1.get_exe_nodes_inBox_vector(Point(-50,-50,-2.6),Vector3(100,100,0.05))

    for s in sup1:
        print( f'  {fem_1.gcoord[s].zcoord}')


    for k,v in restul_dict.items():
        if int(fem_1.gnode[k].nodex) in sup1:
            print( f' Inter_node:{k}  {fem_1.gcoord[fem_1.gnode[k].nodex]}')

    print("stopp")


        
      


    
def setup1():
    
    restul_dict=dict()
            
    #file1=r'C:\DNVGL\Workspaces\ReactionTest\SESTRA.LIS' 
    file1=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\SESTRA.LIS'
    with open(file1, 'r') as f1:
        for line in f1:
            data=line.split()
            if len(data)==4:
                if data[0].strip()=="21":

                    if int(float(data[2])) not in restul_dict:
                        restul_dict[int(float(data[2]))]=float(data[3])

    print(len(restul_dict))


    filename1=r'C:\DNVGL\Workspaces\STEPnSUPER_SOM\Presel_init\T21.FEM'
    filename2=r'T21.FEM'
   
    
    #21 TRANSLATE 23.1 1.2 0.0
    tran_x=0
    tran_y=0
    tran_z=0.0

    fem_1=FEM()
    start_time = time.time()  # Start measuring time
    fem_2=FEM()
            


    fem_1.read_fem(filename1)
    fem_2.read_fem(filename2)
    for k,v in fem_1.gelmnt1.items():
        if v==fem_2.gelmnt1[k]:
            continue
        else:
            print(f"not ok {v} ")

    for k,v in fem_1.gelref1.items():
        if v==fem_2.gelref1[k]:
            continue
        else:
            print(f"not ok {v} ")

    
    for k,v in fem_1.gsetmemb.items():
        if v==fem_2.gsetmemb[k]:
            continue
        else:
            print(f"not ok {v} ")

    
    for k,v in fem_1.beuslo.items():
        if v==fem_2.beuslo[k]:
            continue
        else:
            print("not ok")



    print("stopp")


    #print(fem_obj_3d.gcoord[720954])
    #print(fem_obj_3d.gcoord[fem_obj_3d.gnode[720954].nodex])
    res=fem_1.get_max_min_coor()

    #print(fem_obj_3d.gcoord[478580])
    #print(fem_obj_3d.gcoord[fem_obj_3d.gnode[478580].nodex])

    print(res)  
    p01x=2.6+tran_x
    p02x=2.6+tran_x
    p01y=-1.5+tran_y

    p02y=0.8+tran_y
    p03x=-3.4+tran_x

    p04x=-3.4+tran_x
    p03y=-1.5+tran_y
    p04y=0.8+tran_y
    pxz=-2.6
    vect=Vector3(1,1,0.03)
    p_circ=Point(-1+tran_x,-1+tran_y,pxz)

    sup1=fem_1.get_exe_nodes_inBox_vector(Point(p01x,p01y,pxz),vect)
    sup2=fem_1.get_exe_nodes_inBox_vector(Point(p02x,p02y,pxz),vect)

    sup3=fem_1.get_exe_nodes_inBox_vector(Point(p03x,p03y,pxz),vect)
    sup4=fem_1.get_exe_nodes_inBox_vector(Point(p04x,p04y,pxz),vect)

    sup5=fem_1.get_exe_nodes_inBox_vector(p_circ,Vector3(2,2,0.03))
    #fem_obj_3d.add_bnbc(sup1,[1,1,1,1,1,1])
    fem_1.write("T21.FEM")

    print(len(sup1))
    print(len(sup2))
    print(len(sup3))
    print(len(sup4))
    print(len(sup5))
    total_nodes=len(sup1)+len(sup2)+len(sup3)+len(sup4)+len(sup5)
    print(total_nodes)




    vtta=fem_1.get_nodes_between_z_coor(-2.6,2.2)

    env=[]

    for n in vtta:
        env.append(int(fem_1.gnode[n].nodex))


    ast=fem_1.get_nodes_inBox(Point(2.59,-1.81,-2.6),Point(3.31,-2.6,-2.571))
    res_1=[]
    res_2=[]
    res_3=[]
    res_4=[]
    res_5=[]

    for k,v in restul_dict.items():
        
        print( f' Inter_node:{k} external_node{fem_1.gnode[k]} {fem_1.gcoord[k]} {fem_1.gcoord[fem_1.gnode[k].nodex]}')
        
        


        if k in sup1:
            res_1.append(v)
        if k in sup2:
            res_2.append(v)
        if k in sup3:
            res_3.append(v)
        if k in sup4:
            res_4.append(v)
        if k in sup5:
            res_5.append(v)


       
        
    print("stopp")


print("stopp")

if __name__ == '__main__':

    main()
   