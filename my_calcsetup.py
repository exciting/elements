import sys
elementshome = '/fshome/tde/git/my_calc/gen/elements/'
sys.path.append(elementshome)
import eos_calc_use_templ as calc

param = {}
usr = "tde"
scale = []
covera = []
volume = []

azero = 4.319       #lattice parameter
etamax = 0.05       #steps in lattice parameter
coverazero = 1.6    #c/a ratio
dcovera = 1.6/50    #steps in c/a
param['structure'] = ['hcp']

vzero = azero**3 * coverazero * 3**(1/2.)/2
dvolume = vzero/50 

#create lattice parameter steps
i=10
while i > -1:
    scale.append(azero - (i-5)*etamax)
    i = i-1
if param['structure'][0] == 'hcp':
    #create volume steps
    i=10    
    while i > -1:
        volume.append(vzero - (i-5)*dvolume)
        i = i-1
    #create c/a steps
    i=10    
    while i > -1:
        covera.append(coverazero - (i-5)*dcovera)
        i = i-1
    #create lattice parameters out of c/a steps
    scale = []
    for coa in covera:
        a = {}
        a[str(coa)] = []
        for v in volume:
            a[str(coa)].append((2/3.**(1/2)*v/coa)**(1/3))
        scale.append(a)
    
else:
    covera = [1.0]

param['scale'] = scale
param['rgkmax'] = [8,10,12]
param['ngridk'] = [8,10,12]
param['swidth'] = [0.01]
param['species'] = ['Be']
param['covera'] = covera
param['calchome'] = ["/fshome/tde/cluster/test1/"]
param['speciespath'] = ["/appl/EXCITING/versions/hydrogen/species/"]
param['templatepath'] = [elementshome + "templates/"]
param['mod'] = ['parallel']     # convergence or bulk-modulus

calc.CALC(param)
