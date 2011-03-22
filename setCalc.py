
import xml.etree.ElementTree as etree
import auto_calc_setup

class setCalc(object):
    def __init__(self,lastpar,lastvar,autosetup,setupname,f,root,dir):
        self.lastpar = lastpar
        self.lastvar = lastvar
        self.autosetup = autosetup
        self.setupname = setupname
        self.f = etree.parse(dir + 'auto_conv.xml')
        self.root = self.f.getroot()
        self.dir = dir
        
    def zeroD(self):
        lastpar = self.lastpar
        lastvar = self.lastvar
        autosetup = self.autosetup
        setupname = self.setupname
        su = open(setupname)
        sustr= su.read()
        setup = eval(sustr)
        new = {}
        newvar = []
        
        i=1
        if type(autosetup['order'][str(i)]) == str:
            n=1
            newvar = float(lastvar[self.lastpar][-1]) + float(autosetup['stepsize'][lastpar])
            new[lastpar]= newvar
            for par in autosetup['order'].keys():
                new[autosetup['order'][par]] = setup['param'][autosetup['order'][par]]
                
            new['par'] = lastpar
        else:
            n=len(autosetup['order'][str(i)])
            while i<=n:
                newvar = float(lastvar) + float(autosetup['stepsize'][lastpar[i]])
                new['ngridk'] = setup['param']['ngridk']
                new['swidth'] = setup['param']['swidth']
                new[lastpar[i]]= [newvar]
                i+=1

        etree.SubElement(self.root, 'conv',{'par':str(lastpar), 'parval':str(new)})
        self.f.write(self.dir + 'auto_conv.xml')
        new.pop('par')
        autoset = auto_calc_setup.Autosetup(setupname)
        newset = autoset.setup({lastpar:[float(newvar)]})
        autoset.calculate(newset)
        return
        
    def oneD(self,steps):
        lastpar = self.lastpar
        lastvar = self.lastvar
        autosetup = self.autosetup
        setupname = self.setupname
        su = open(setupname)
        sustr= su.read()
        setup = eval(sustr)
        new = {}
        newvar = []
        
        i=1
        if type(autosetup['order'][str(i)]) == str:
            n=1
            newvar = []
            if lastpar == 'swidth' and lastvar[lastpar][-1] <= 0.1:
                autosetup['stepsize'][lastpar] = autosetup['stepsize'][lastpar]/10
            init = float(lastvar[lastpar][-1]) - float(autosetup['stepsize'][lastpar])
            for j in range(steps):
                newvar.append(init)
                init = init + float(autosetup['stepsize'][lastpar])
            new[lastpar]= newvar
            for par in lastvar.keys():
                if par != lastpar:
                    new[par] = lastvar[par]
                
            new['par'] = lastpar
        else:
            n=len(autosetup['order'][str(i)])
            while i<=n:
                newvar = float(lastvar) + float(autosetup['stepsize'][lastpar[i]])
                new['ngridk'] = setup['param']['ngridk']
                new['swidth'] = setup['param']['swidth']
                new[lastpar[i]]= [newvar]
                i+=1

        etree.SubElement(self.root, 'conv',{'par':str(lastpar), 'parval':str(new)})
        self.f.write(self.dir + 'auto_conv.xml')
        autoset = auto_calc_setup.Autosetup(setupname)
        new.pop('par')
        newset = autoset.setup(new)
        autoset.calculate(newset)
        return
    def twoD():
        return
        
    
        