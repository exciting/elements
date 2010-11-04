import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as etree

class Plot(object):
    def __init__(self):
        self.params = etree.parse('./const_parameters.xml')
        self.eos_data = etree.parse('./eos_data.xml')
        self.convergence = etree.parse('./convergence.xml')
        
        structure = self.params.getroot().find('structure').get('str')
        if structure in ['hcp','hex']:
            coaplot=True
        else:
            coaplot=False
        
        for i in range(5):
            msg = {}
            if coaplot:
                msg['msg_coa'] = '\nFor energy vs. c/a type: covera'
            else:
                msg['msg_coa'] = ''
            msg['msg_eos'] = '\nFor energy vs. volume type: eos'
            type = raw_input('What do you want to plot?%(msg_coa)s%(msg_eos)s\n>>>'%msg)
            if type == 'eos':
                self.eosplot_mpl()
                break
            elif type == 'covera' and coaplot == ', covera':
                self.coaplot_mpl()
                break
            else:
                print 'Please try again and type one of: eos%s'%coaplot
                
        #template = f.getroot().find('elementshome')
    def eosplot_mpl(self):
        vol = []
        energy = []
        expvol = []
        expenergy = []
        expvol_bad = []
        expenergy_bad = []
        par = []
        parname = []
        colLabel = []
        e_min = []
        v_min = []
        b0_min = []
        db0_min = []
        rowLabel = []
        cellText = []
            
        eosdata = etree.parse('./eosplot.xml')
        root = eosdata.getroot()
        graphs = root.getiterator('graph')
        n=0
        for graph in graphs:
            vol.append([])
            energy.append([])
            par.append(graph.get('param'))
            parname.append(graph.get('parname'))
            e_min.append(graph.get('energy_min'))
            v_min.append(graph.get('vol_min'))
            b0_min.append(graph.get('B0'))
            db0_min.append(graph.get('dB0'))
            points = graph.getiterator('point')
            for point in points:
                vol[n].append(float(point.get('volume')))
                energy[n].append(float(point.get('energy')))
            n=n+1
        graphs = root.getiterator('graph_exp')
        n=0
        for graph in graphs:
            expvol.append([])
            expenergy.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            for point in points:
                expvol[n].append(float(point.get('volume')))
                expenergy[n].append(float(point.get('energy')))
            n=n+1
            
        graphs = root.getiterator('graph_exp_bad')
        n=0
        for graph in graphs:
            expvol_bad.append([])
            expenergy_bad.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            for point in points:
                expvol_bad[n].append(float(point.get('volume')))
                expenergy_bad[n].append(float(point.get('energy')))
            n=n+1
            
        structure = self.params.getroot().find('structure').get('str')
        species = self.params.getroot().find('species').get('spc')
        
        n=0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Equation of state plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})

        colors = ['b','g','r','c','m','k','FF9933','006600','66CCFF','y']
        for graph in graphs:
            ax.plot(vol[n], energy[n], '', label='%(name)s = %(val)s'%{'name':parname[n], 'val':str(par[n])}, color=colors[n])
            ax.plot(expvol[n], expenergy[n], '.', color=colors[n])
            ax.plot(v_min[n], e_min[n], 'o')
            ax.plot(expvol_bad[n], expenergy_bad[n], '.')
            ax.set_xlabel(r'$volume$   $[{Bohr^3}]$')
            ax.set_ylabel(r'$total$ $energy$   $[{Hartree}]$')
            ax.legend(loc='best')
            #plt.title('Equation of state plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})
            rowLabel.append('%(name)s = %(val)s'%{'name':parname[n], 'val':str(par[n])})
            n=n+1
        
        width = 100

        cell = [v_min,e_min,b0_min,db0_min]
        for column in cell:
            cellText.append(['%s' % (x) for x in column])
        cellText.reverse()
        #table = plt.table(cellText=cellText, cellColours=None,
        #          cellLoc='right',colWidths=[0.1,0.1,0.1,0.1,0.1],
        #          rowLabels=[r'$(c/a)_min$',r'$V_0$',r'$E_tot$$_,min$',r'$(c/a)_min$'], rowColours=None, rowLoc='right',
        #          colLabels=rowLabel, colColours=None, colLoc='center',
        #          loc='right', bbox=None)
        #for column in cell:
        #table.scale(2,2)
        #table.auto_set_font_size()
        
        plt.show()
        #table.auto_set_font_size()
    def coaplot_mpl(self):
        vol = []
        volume = []
        energy = []
        expvol = []
        expenergy = []
        expvol_bad = []
        expenergy_bad = []
        par = []
        parname = []
        eosdata = etree.parse('./coaplot.xml')
        root = eosdata.getroot()
        graphs = root.getiterator('graph')
        n=0
        for graph in graphs:
            vol.append([])
            energy.append([])
            par.append(graph.get('param'))
            parname.append(graph.get('parname'))
            points = graph.getiterator('point')
            for point in points:
                vol[n].append(float(point.get('covera')))
                energy[n].append(float(point.get('energy')))
            n=n+1
        graphs = root.getiterator('graph_exp')
        n=0
        for graph in graphs:
            expvol.append([])
            expenergy.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            for point in points:
                expvol[n].append(float(point.get('covera')))
                expenergy[n].append(float(point.get('energy')))
            n=n+1
            
        graphs = root.getiterator('graph_exp_bad')
        n=0
        for graph in graphs:
            expvol_bad.append([])
            expenergy_bad.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            volume.append(graph.get('volume'))
            for point in points:
                expvol_bad[n].append(float(point.get('covera')))
                expenergy_bad[n].append(float(point.get('energy')))
            n=n+1
            
        structure = self.params.getroot().find('structure').get('str')
        species = self.params.getroot().find('species').get('spc')

        n=0
        for graph in graphs:
            plt.plot(vol[n], energy[n], '', label='volume: %(vol)s withs'%{'vol':volume[n],'parname':parname[n],'par':par[n]})
            plt.plot(expvol[n], expenergy[n], '.',color='k')
            plt.plot(expvol_bad[n], expenergy_bad[n], '.')
            plt.xlabel(r'$c/a$')
            plt.ylabel(r'$total$ $energy$   $[{Hartree}]$')
            plt.legend(loc='best')
            plt.title('c/a - plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})
            n=n+1
        plt.show()

test = Plot().eosplot_mpl()