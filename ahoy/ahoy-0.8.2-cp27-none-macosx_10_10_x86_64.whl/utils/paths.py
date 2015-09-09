from glob import glob

chi_scan_dirname_sets = [
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,Dr=1,chi=*,side=1,type=S,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,Dr=1,chi=*,side=1,type=T,dtMem=0.1,tMem=5,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,Dr=1,chi=*,side=2,type=S,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,Dr=1,chi=*,side=2,type=T,dtMem=0.1,tMem=5,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,p=1,chi=*,side=1,type=S,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,p=1,chi=*,side=1,type=T,dtMem=0.1,tMem=5,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,p=1,chi=*,side=2,type=S,noObs'),
    glob('ships_2D,dt=0.01,n=5000,align=0,origin=1,v=20,p=1,chi=*,side=2,type=T,dtMem=0.1,tMem=5,noObs'),
]
