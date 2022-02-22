#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:21:57 2022

@author: dfadda
"""

import os
import sys
import getopt
import numpy as np


def writescanfile(filename, lon, lat, dic, gb, gr, ord, i, j, step, l0, b0):
    """Generic scan taken from obsmaker, it should be updated"""
    import time
    with open(filename, 'w') as f:
        f.write('# Time stamp at last update: ' + str(time.time()) + '\n')
        f.write('#    ASTRONOMY\n')
        f.write('# ###############################################################################\n')
        f.write('## OBSLAM and OBSBET set by kvscans.py\n')       
        f.write('## point #[{0:d},{1:d}] of a 25x25 spiral around [{2:d},{3:d}], Step {4:d} dmm\n'.format(i,j,l0,b0,step))
        f.write('# ###############################################################################\n')
        f.write('%s%s%s' % ("AOR_ID".ljust(12),  # adjust ljust param
                              ('"NONE"').ljust(20), '# from DCS\n'))
        f.write('%s%s%s' % ("OBJ_NAME".ljust(12),
                               ('"TELSIM"').ljust(20),
                               '# Name of astronomical object observed\n'))
        f.write('%s%s%s' % ("COORDSYS".ljust(12),
                               ('"J2000"').ljust(20),
                               '# Target coordinate system\n'))
        f.write('%s%s%s' % ("OBSLAM".ljust(12),  # adjust ljust param
                            '{0:d}'.format(lon).ljust(20), '# in deg\n'))
        f.write('%s%s%s' % ("OBSBET".ljust(12),  # adjust ljust param
                            '{0:d}'.format(lat).ljust(20), '# in deg\n'))
        f.write('%s%s%s' % ("DET_ANGL".ljust(12),  # adjust ljust param
                               str(0.0).ljust(20),
                               '# Detector y-axis EofN\n'))
        f.write('%s%s%s' % ("CRDSYSMP".ljust(12),  # adjust ljust param
                               ('"J2000"').ljust(20),
                               '# Mapping coordinate system\n'))
        f.write('%s%s%s' % ("DLAM_MAP".ljust(12),
                                   str("%.1f" % 0.).ljust(20), '# arcsec\n'))
        f.write('%s%s%s' % ("DBET_MAP".ljust(12),
                                   str("%.1f" % 0.).ljust(20), '# arcsec\n'))
        f.write('%s%s%s' % ("CRDSYSOF".ljust(12),
            ('"J2000"').ljust(20),
            '# Off position coordinate system\n'))
        f.write('%s%s%s' % ("DLAM_OFF".ljust(12),
                            str("%.1f" % 0.).ljust(20), '# arcsec\n'))
        f.write('%s%s%s' % ("DBET_OFF".ljust(12),
                            str("%.1f" % 0.).ljust(20), '# arcsec\n'))            
        f.write('%s%s%s' % ("PRIMARAY".ljust(12),
            ('"RED"').ljust(20),
            '# Primary array\n'))
        f.write('%s%s%s' % ("LOSF_UPD".ljust(12),
                                str(0).ljust(20),
                                '# 0/1/2  block/allow/force updates\n'))
        f.write('\n#    DICHROIC SETTING\n')
        f.write('%s%s%s' % ("DICHROIC".ljust(12),
                            str(dic).ljust(20),
                            '# Dichroic wavelength in um\n'))
        f.write('\n#    GRATING\n# Blue\n')
        f.write('%s%s%s' % ("G_ORD_B".ljust(12),
                            str(ord).ljust(15),
                            '# Blue grating order to be used\n'))
        f.write('%s%s%s' % ("G_WAVE_B".ljust(12),
                            str("%.3f" % 64.0).ljust(15),
                            '# Wavelength to be observed in um INFO ONLY\n'))
        f.write('%s%s%s' % ("G_CYC_B".ljust(12),
                            str(1).ljust(15),
                            '# The number of grating cycles (up-down)\n'))
        f.write('%s%s%s' % ("G_STRT_B".ljust(12),
                            str(gb).ljust(15),
                            '# absolute starting value in inductosyn units\n'))
        f.write('%s%s%s' % ("G_PSUP_B".ljust(12),
                            str(1).ljust(15),
                            '# number of grating position up in one cycle\n'))
        f.write('%s%s%s' % ("G_SZUP_B".ljust(12),
                            str(0).ljust(15),
                            '# step size on the way up; same unit as G_STRT\n'))
        f.write('%s%s%s' % ("G_PSDN_B".ljust(12),
                            str(0).ljust(15),
                            '# number of grating position down in one cycle\n'))
        f.write('%s%s%s' % ("G_SZDN_B".ljust(12),
                            str(0).ljust(15),
                            '# step size on the way down; same unit as G_STRT\n'))
        f.write('# Red\n')
        f.write('%s%s%s' % ("G_WAVE_R".ljust(12),
                            str("%.3f" % 158.0).ljust(15),
                            '# Wavelength to be observed in um INFO ONLY\n'))
        f.write('%s%s%s' % ("G_CYC_R".ljust(12),
                            str(1).ljust(15),
                            '# The number of grating cycles (up-down)\n'))
        f.write('%s%s%s' % ("G_STRT_R".ljust(12),
                            str(gr).ljust(15),
                            '# absolute starting value in inductosyn units\n'))
        f.write('%s%s%s' % ("G_PSUP_R".ljust(12),
                            str(1).ljust(15),
                            '# number of grating position up in one cycle\n'))
        f.write('%s%s%s' % ("G_SZUP_R".ljust(12),
                            str(0).ljust(15),
                            '# step size on the way up; same unit as G_STRT\n'))
        f.write('%s%s%s' % ("G_PSDN_R".ljust(12),
                            str(0).ljust(15),
                            '# number of grating position down in one cycle\n'))
        f.write('%s%s%s' % ("G_SZDN_R".ljust(12),
                            str(0).ljust(15),
                            '# step size on the way down; same unit as G_STRT\n'))
        f.write('\n#    RAMP\n')
        f.write('%s%s%s' % ("RAMPLN_B".ljust(12),
                            str(32).ljust(15),
                            '# number of readouts per blue ramp\n'))
        f.write('%s%s%s' % ("RAMPLN_R".ljust(12),
                            str(32).ljust(15),
                            '# number of readouts per red ramp\n'))
        f.write('\n#    CHOPPER\n')
        f.write('%s%s%s' % ("C_SCHEME".ljust(12),
                            ('"4POINT"').ljust(15),
                            '# Chopper scheme; 2POINT or 4POINT\n'))
        f.write('%s%s%s' % ("C_CRDSYS".ljust(12),
                            ('"HORIZON"').ljust(15),
                            '# Chopper coodinate system\n'))
        f.write('%s%s%s' % ("C_AMP".ljust(12),
                            str(60).ljust(15),
                            '# chop amplitude in arcsec\n'))
        f.write('%s%s%s' % ("C_TIP".ljust(12),
                            str(1.0).ljust(15), '# fraction\n'))
        f.write('%s%s%s' % ("C_BEAM".ljust(12),
                            str("%.1f" % -1.0).ljust(15), '# nod phase\n'))
        f.write('%s%s%s' % ("C_POSANG".ljust(12),
                            str(0.0).ljust(15), '# deg, S of E\n'))
        f.write('%s%s%s' % ("C_CYC_B".ljust(12),
                            str(2).ljust(15),
                            '# chopping cycles per grating position\n'))
        f.write('%s%s%s' % ("C_CYC_R".ljust(12),
                            str(2).ljust(15),
                            '# chopping cycles per grating position\n'))
        f.write('%s%s%s' % ("C_PHASE".ljust(12),
                            str("%.1f" % float(130)).ljust(15),
                            '# chopper signal phase shift relative to R/O in deg\n'))
        f.write('%s%s%s' % ("C_CHOPLN".ljust(12),
                            str(64).ljust(15),
                            '# number of readouts per chop position\n'))
        f.write('\n#    CAPACITORS\n')
        f.write('%s%s%s' % ("CAP_B".ljust(12),
                            str(1330).ljust(15),
                            '# Integrating capacitors in pF\n'))
        f.write('%s%s%s' % ("CAP_R".ljust(12),
                            str(1330).ljust(15),
                            '# Integrating capacitors in pF\n'))
        f.write('\n#    CONVERTER\n# Blue\n')
        f.write('%s%s%s' % ("ZBIAS_B".ljust(12),
                            str("%.3f" % 60.0).ljust(15),
                            '# Voltage in mV\n'))
        f.write('%s%s%s' % ("BIASR_B".ljust(12),
                            str("%.3f" % 0).ljust(15), '# Voltage in mV\n'))
        f.write('%s%s%s' % ("HEATER_B".ljust(12),
                            str("%.3f" % 0).ljust(15), '# Voltage in mV\n'))
        f.write('# Red\n')
        f.write('%s%s%s' % ("ZBIAS_R".ljust(12),
                            str("%.3f" % 50.0).ljust(15),
                            '# Voltage in mV\n'))
        f.write('%s%s%s' % ("BIASR_R".ljust(12),
                            str("%.3f" % 0).ljust(15), '# Voltage in mV\n'))
        f.write('%s%s%s' % ("HEATER_R".ljust(12),
                            str("%.3f" % 0).ljust(15), '# Voltage in mV\n'))
        f.write('\n#    CALIBRATION SOURCE\n')
        f.write('%s%s%s' % ("CALSTMP".ljust(12),
                            str(0).ljust(15), '# Kelvin\n'))
        f.write('\nHERE_COMETH_THE_END\n')


def main(argv):
    lam = ''
    beta = ''
    outdir = '.'
    try:
        opts, args = getopt.getopt(argv, "hl:b:o:", ["lambda=","beta=","outdir="])
    except getopt.GetoptError:
        print ('Usage: kvscans.py -l <lambda> -b <beta> -o <outdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Usage: kvscans.py -l <lambda> -b <beta> -o <outdir>')
            print ('Lambda: central x position')
            print ('Beta: central y position')
            print ('Outdir: output directory')
            sys.exit()
        elif opt in ("-l", "--lambda"):
            lam = arg
        elif opt in ("-b", "--beta"):
            beta = arg
        elif opt in ( "-o", "--outdir"):
            outdir = arg
    if lam == '' and beta == '':
        print ('Usage: kvscans.py -l <lambda> -b <beta>')
        sys.exit()
    else:       
        print ('Lambda is ', lam)
        print ('Beta is ', beta)
        
    if outdir != '.':
        if os.path.isdir(outdir):
            pass
        else:
            print('Please create the directory', outdir)
            sys.exit(2)
        
    if lam.isnumeric() and beta.isnumeric():
        lam = int(lam)
        beta = int(beta)
    else:
        print('Please enter integer numbers for lambda and beta')
        sys.exit(2)

    offsets1 = np.array([
        [0,0],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],
        [2,0],[2,1],[2,2],[1,2],[0,2],[-1,2],[-2,2],[-2,1],[-2,0],
        [-2,-1],[-2,-2],[-1,-2],[0,-2],[1,-2],[2,-2],[2,-1],
        [3,0],[3,1],[3,2],[3,3],[2,3],[1,3],[0,3],[-1,3],[-2,3],[-3,3],[-3,2],[-3,1],[-3,0],
        [-3,-1],[-3,-2],[-3,-3],[-2,-3],[-1,-3],[0,-3],[1,-3],[2,-3],[3,-3],[3,-2],[3,-1],
        [4,0],[4,1],[4,2],[4,3],[4,4],[3,4],[2,4],[1,4],[0,4],[-1,4],[-2,4],[-3,4],
        [-4,4],[-4,3],[-4,2],[-4,1],[-4,0],[-4,-1],[-4,-2],[-4,-3],[-4,-4],[-3,-4],
        [-2,-4],[-1,-4],[0,-4],[1,-4],[2,-4],[3,-4],[4,-4],[4,-3],[4,-2],[4,-1],
        [5,0],[5,1],[5,2],[5,3],[5,4],[5,5],[4,5],[3,5],[2,5],[1,5],[0,5],
        [-1,5],[-2,5],[-3,5],[-4,5],[-5,5],[-5,4],[-5,3],[-5,2],[-5,1],[-5,0],
        [-5,-1],[-5,-2],[-5,-3],[-5,-4],[-5,-5],[-4,-5],[-3,-5],[-2,-5],[-1,-5],
        [0,-5],[1,-5],[2,-5],[3,-5],[4,-5],[5,-5],[5,-4],[5,-3],[5,-2],[5,-1],
        [6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[5,6],[4,6],[3,6],[2,6],[1,6],[0,6],
        [-1,6],[-2,6],[-3,6],[-4,6],[-5,6],[-6,6],[-6,5],[-6,4],[-6,3],[-6,2],[-6,1],[-6,0],
        [-6,-1],[-6,-2],[-6,-3],[-6,-4],[-6,-5],[-6,-6],[-5,-6],[-4,-6],[-3,-6],[-2,-6],[-1,-6],
        [0,-6],[1,-6],[2,-6],[3,-6],[4,-6],[5,-6],[6,-6],[6,-5],[6,-4],[6,-3],[6,-2],[6,-1]
    ])
    
    offsets2 = np.array( [
        [4,0],[4,1],[4,2],[4,3],[4,4],[3,4],[2,4],[1,4],[0,4],
        [-1,4],[-2,4],[-3,4],[-4,4],[-4,3],[-4,2],[-4,1],[-4,0],
        [-4,-1],[-4,-2],[-4,-3],[-4,-4],[-3,-4],[-2,-4],[-1,-4],
        [0,-4],[1,-4],[2,-4],[3,-4],[4,-4],[4,-3],[4,-2],[4,-1],
        [5,0],[5,1],[5,2],[5,3],[5,4],[5,5],[4,5],[3,5],[2,5],[1,5],[0,5],
        [-1,5],[-2,5],[-3,5],[-4,5],[-5,5],[-5,4],[-5,3],[-5,2],[-5,1],[-5,0],
        [-5,-1],[-5,-2],[-5,-3],[-5,-4],[-5,-5],[-4,-5],[-3,-5],[-2,-5],[-1,-5],
        [0,-5],[1,-5],[2,-5],[3,-5],[4,-5],[5,-5],[5,-4],[5,-3],[5,-2],[5,-1],
        [6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[5,6],[4,6],[3,6],[2,6],[1,6],[0,6],
        [-1,6],[-2,6],[-3,6],[-4,6],[-5,6],[-6,6],[-6,5],[-6,4],[-6,3],[-6,2],[-6,1],[-6,0],
        [-6,-1],[-6,-2],[-6,-3],[-6,-4],[-6,-5],[-6,-6],[-5,-6],[-4,-6],[-3,-6],[-2,-6],[-1,-6],
        [0,-6],[1,-6],[2,-6],[3,-6],[4,-6],[5,-6],[6,-6],[6,-5],[6,-4],[6,-3],[6,-2],[6,-1]
        ])
    
    dicgratord = np.array([
        [105,734,640,2],
        [105,971,822,2],
        [105,1249,1200,2],
        [105,1249,1200,2],
        [105,971,822,2],
        [105,734,640,2],
        [105,180,267,1],
        [105,431,754,1],
        [105,700,902,1],
        [105,700,902,1],
        [105,431,754,1],
        [105,180,267,1],
        [105,1600,1003,2],
        [105,1600,1003,2],
        [130,180,640,1],
        [130,431,822,1],
        [130,1062,1200,1],
        [130,1062,1200,1],
        [130,431,822,1],
        [130,180,640,1],
        [130,734,400,2],
        [130,971,754,2],
        [130,1249,902,2],
        [130,1249,902,2],
        [130,971,754,2],
        [130,734,400,2],
        [130,1600,1003,2],
        [130,1600,1003,2]
        ])
    
    step = 6 #dmm
    
    #path0,file0 = os.path.split(__file__)
    #print('Path is: ', path0)

    for ikv, kv in enumerate(dicgratord):
        dic, gb, gr, order = kv
        gb *= 1000
        gr *= 1000
        # Create directory
        folderpath = os.path.join(outdir,'KV{0:02d}'.format(ikv+1))
        print(folderpath)
        os.mkdir(folderpath)
        ifile = 0
        for o1 in offsets1:
            ifile += 1
            i, j = o1
            dx, dy = step * i, step * j
            lon = lam + dx
            lat = beta + dy
            filename = 'KV{0:02d}_@1x_{1:04d}_{2:d},{3:d}.scn'.format(ikv+1,ifile,i,j)
            filepath = os.path.join(folderpath, filename)
            #print(filepath)
            writescanfile(filepath, lon, lat, dic, gb, gr, order, i, j, step, lam, beta)
        for o2 in offsets2:
            ifile += 1
            i, j = o2
            dx, dy = 2 * step * i, 2 * step * j
            lon = lam + dx
            lat = beta + dy
            filename = 'KV{0:02d}_@2x_{1:04d}_{2:d},{3:d}.scn'.format(ikv+1,ifile,i,j)
            filepath = os.path.join(folderpath, filename)
            #print(filepath)
            writescanfile(filepath, lon, lat, dic, gb, gr, order, i, j, 2*step, lam, beta)

if __name__ == "__main__":
   main(sys.argv[1:])
