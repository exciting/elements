"""Set up calculations and submit to loadleveler

    arguments:  -parameters ..... optional calculation parameters
                    type::dictionary
    returns:    none
    
    set calculation parameters here!
"""
import xml.etree.ElementTree as etree
import subprocess
import os
import time

import search_dir
import check_for_existing

class CALC(object):
    def __init__(self, setup):
        ######################################################
        #      == Define calculation parameters here ==      #
        ######################################################

        ###########################################################
        ###########################################################
        #remove old status file:
        if os.path.exists('./finished'): 
            proc = subprocess.Popen(['rm ./finished'], shell=True)
            proc.communicate()
                       
        inpar = {}
        convpar = {}
        
        scale = setup['param']['scale']
        for key in setup['param'].keys():
            if setup['structure'] in ['hcp','hex'] and key == 'scale' and setup['mod'] != 'simple_conv':
                continue
            inpar[key] = "<param name='%s'>"%key #new old inpar['key'] = ""
            if key not in ['scale','covera']:
                convpar[key] = setup['param'][key]

            for value in setup['param'][key]:
                
                if setup['structure'] in ['hcp','hex'] and key == 'covera' and setup['mod'] != 'simple_conv':
                    for alatt in scale[str(value)]:
                        inpar[key] = inpar[key] + "<val>%s" % value
                        inpar[key] = inpar[key] + "<dep name='scale' val='%s'/>" % str(alatt)
                        inpar[key] = inpar[key] + "</val>"
                else:
                    inpar[key] = inpar[key] + "<val>%s</val>" % value
            inpar[key] = inpar[key] + "</param>"
        for key in setup.keys():
            
            if key not in ['param','species']:
                #inpar[key] = setup[key]
                continue
            elif key == 'species':
                inpar[key] = "<param name='species'><val>%s</val></param>" % setup[key]
        ###########################################################
        #            == Set new parameters here! ==               #
        #              also modify input template                 #
        ###########################################################
        paramset = """<?xml version="1.0" encoding="UTF-8"?><setup path="%s">"""%setup['calchome']
        paramset = paramset + inpar['species']
        for parkey in inpar.keys():
            if setup['structure'] in ['hcp','hex'] and setup['mod'] != 'simple_conv' and parkey == 'scale' or parkey == 'species':
                continue
            elif parkey == 'species':
                continue
            paramset = paramset + inpar[parkey]
        paramset = paramset + '</setup>'

        ############################################################
        ############################################################
        try:
            os.mkdir(setup['calchome'])
        except:
            print 'dir exists'
            
        os.chdir(setup['calchome'])
        
        f = open('./set.xml', 'w')
        f.write(paramset)
        f.close()
        
        
        # write constant calculation parameters to xml file:
        const_param = """
        <calc>
            <calchome path='%(calchome)s'/>
            <species spc='%(species)s'/>
            <structure str='%(structure)s'/>
            <speciespath spa = '%(speciespath)s'/>
            <elementshome elementsdir ='%(elementshome)stemplates/'/>
            <mode mod='%(mod)s'/>
        </calc>
        """ %setup
        
        f1 = open('./const_parameters.xml', 'w')
        f1.write(const_param)
        f1.close()
        
        convroot = etree.Element('convergence')

        for key in convpar.keys():
            convchild = etree.SubElement(convroot, 'n_param')
            if len(convpar[key]) > 1:
                convchild = etree.SubElement(convroot, 'n_param')
                convchild.set('name',str(key))
                convchild.set('val',str(convpar[key]))
        
        

        convroot.append(convchild)
        convtree = etree.ElementTree(convroot)
        convtree.write('./convergence.xml')
        if not os.path.exists(setup['calchome'] +  'parset.xml'):
            proc1 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + 'permute_set.xsl ' + setup['calchome'] + 'set.xml > ' + setup['calchome'] +  'parset.xml'], shell=True)
            proc1.communicate()
            print "created parset.xml"
            curr_calc = 'parset.xml'
        else:
            for i in range(50):
                if os.path.exists(setup['calchome'] +  'parset_%s.xml'%str(i)):
                    continue
                else:    
                    proc1 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + 'permute_set.xsl ' + setup['calchome'] + 'set.xml > ' + setup['calchome'] +  'parset_%s.xml'%str(i)], shell=True)
                    proc1.communicate()
                    newcalc = check_for_existing.Manipulate(setup['calchome'] +  'calc_filelist.xml', setup['calchome'] +  'parset_%s.xml'%str(i), setup['calchome'])
                    newcalc.append_calc()

                    curr_calc = 'parset_%s.xml'%str(i)
                    print 'appended new calculations to parset.xml'
                    break
        
        proc2 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + 'input_' + setup['structure'] + '.xsl ' + setup['calchome'] + curr_calc], shell=True)
        proc2.communicate()
        print "created dir tree-structure and inputs"
        
        if setup['calculate'] == 'True':
            
            exec_template = setup['exectemplate']
            if exec_template == 'shelcommand.xsl':
                if os.path.exists(setup['calchome'] + 'execute'):
                    proc3 = subprocess.Popen(['rm ' + setup['calchome'] + 'execute'], shell=True)
                    proc3.communicate()
                out = ' > execute'
            
            else: out =''
            proc4 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + exec_template + ' ' + setup['calchome'] + curr_calc + out], shell=True)
            proc4.communicate()
            if exec_template == 'shelcommand.xsl':
                proc5 = subprocess.Popen(['chmod u+x ' + setup['calchome'] + 'execute'], shell=True)
                proc5.communicate()
            if exec_template == 'loadleveler.xsl':
                print "created lljob script"
            
                proc6 = subprocess.Popen(['llsubmit lljob_tree'], shell=True)
                proc6.communicate()
                print "submitted lljob to cluster"
            
            #proc5 = subprocess.Popen(['cp '+ setup['elementshome'] + 'my_calcsetup.py ' + setup['calchome']], shell=True)
            #proc5.communicate()
            
            #check for calculation to be finished:
            #for i in range(100):
            #    if os.path.exists('finished'):
            #        print 'Calclation steps finished on cluster.'
            #        break
            #    time.sleep(60)
            
        elif setup['calculate'] == 'False':
            return
        else:
            print 'ERROR: calculation mode not defined (calculate = True/False)'
            
            
#test = CALC([])
