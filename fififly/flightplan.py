#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:51:35 2021

@author: dfadda
"""
import json
import numpy as np
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def startDescription(aorfile):
    """
    Create a json file which contains the main features of the flight

    Parameters
    ----------
    aorfile : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    import json
    import os
    import io
    from collections import OrderedDict
    import xml.etree.ElementTree as ET
    tree = ET.parse(aorfile+'.misxml')
    root = tree.getroot()
    
    path, fname = os.path.split(aorfile)
    
    for flightplan in root.iter('FlightPlan'):
        flightName = flightplan.attrib['Id']
        departure = flightplan.attrib['DepartureTime']

    date = departure[:10]
    fname = flightName[10:]
    
    # Check obsblocks
    obsBlocks = []
    for leg in root.iter('Leg'):
        name = str(leg.find('Name').text)
        name = name.replace("_", "\_")
        obBlockID = leg.find('ObsBlkID')
        if obBlockID is not None:
            obBlockID = str(obBlockID.text)
            if obBlockID != 'None':
                obsBlocks.append(obBlockID)
    info = [
        ('FlightName', fname),
        ('SofiaFlight', 0),
        ('FifiFlight', 0),
        ('FlightDate', date),
        ('ObsBlocks', obsBlocks)
        ]

    # Observations
    data = OrderedDict(info)
    obsBlocks = []
    for leg in root.iter('Leg'):
        name = str(leg.find('Name').text)
        name = name.replace("_", "\_")
        obBlockID = leg.find('ObsBlkID')
        if obBlockID is not None:
            obBlockID = str(obBlockID.text)
            if obBlockID != 'None':
                print('obBlockID', obBlockID)
                # Get comment
                comment = str(leg.find('Comment').text)
                print('comment ', comment)
                comment.replace('<br>', '\\')
                comment.replace('#','')
                print('comment ', comment)
                aorid = obBlockID[3:10]
                # Grab info from aor file
                aordata = readAOR(aorid, path)
                title, abstract, PropID, PIname = aordata
                
                # Check if directory with images exist
                imagefile = os.path.join(path, aorid, '1.png')
                if os.path.isfile(imagefile):
                    pass
                else:
                    imagefile = None
                
                data[obBlockID] = {
                    'aorid': aorid,
                    'obsBlock': obBlockID,
                    'propid': PropID,
                    'piname': PIname,
                    'title': title,
                    'abstract': abstract,
                    'comment': comment,
                    'imagefile': imagefile
                    }
    outfile = os.path.join(path,fname+'.json')
    
    with io.open(outfile, mode='w') as f:
        str_= json.dumps(data, indent=2, separators=(',', ': '),
                                ensure_ascii=False, cls=MyEncoder)
        f.write(str_)
        
def readAOR(aorid, path):
    """
    Extract data from the AOR file

    Parameters
    ----------
    aorid : TYPE
        DESCRIPTION.
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    import os
    import fitz
    import xml.etree.ElementTree as ET

    aorfile = os.path.join(path, aorid+'.aor')
    attachment = os.path.join(path, aorid+'_attachment.pdf')
    
    # Extract figures from the AOR attachment
    # Check if attachment exists
    
    if os.path.isfile(attachment):
        directory = os.path.join(path,aorid)
        if not os.path.exists(directory):
            os.makedirs(directory)
        doc = fitz.open(attachment)
        image_no = 1
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                print(os.path.join(directory,"%s.png") % (image_no))
                if pix.n < 5:       # this is GRAY or RGB
                    #pix.writePNG(os.path.join(directory,"p%s-%s.png") % (i, xref))
                    pix.writePNG(os.path.join(directory, "%s.png") % (image_no))
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    #pix1.writePNG(os.path.join(directory,"p%s-%s.png") % (i, xref))
                    pix1.writePNG(os.path.join(directory,"%s.png") % (image_no))
                    pix1 = None
                image_no += image_no
                pix = None
            
    # Extract abstract 
    print('aorfile ', aorfile)
    #tree = ET(file=aorfile)
    tree = ET.parse(aorfile)
    title = tree.find('list/ProposalInfo/ProposalTitle')
    abstract = tree.find('list/ProposalInfo/ProposalAbstract')
    print('abstract ', abstract.text[:20])
    # get Proposal ID
    PropID = tree.find('list/ProposalInfo/ProposalID').text
    if PropID == None:
        PropID = "00_0000"    # indicates no PropID
    PI = tree.find('list/ProposalInfo/Investigator')
    #PIname = PI.attrib['Honorific'] + ' ' + PI.attrib['FirstName'] + ' ' + PI.attrib['LastName']
    PIname = PI.attrib['FirstName'] + ' ' + PI.attrib['LastName']
    
    return title.text, abstract.text, PropID, PIname
        

def createAorMap():
    """
    Create a map using a DSS field and FIFI-LS maps (blue/red)
    Probably also guide stars

    Returns
    -------
    None.

    """
    pass

        
def flightTable(aorfile):
    """
    Read the *.misxml file describing the flight
    and creates a Latex table with the description of the legs

    Parameters
    ----------
    aorfile : TYPE  string
        DESCRIPTION name and path of the *misxml file describing the flight

    Returns
    -------
    table : TYPE  string
        DESCRIPTION. Latex table with description of the legs

    """
    import xml.etree.ElementTree as ET
    tree = ET.parse(aorfile+'.misxml')
    root = tree.getroot()
    
    for flightplan in root.iter('FlightPlan'):
        flightTime = flightplan.attrib['FltTime']
        flightName = flightplan.attrib['Id']
        departure = flightplan.attrib['DepartureTime']
        arrival = flightplan.attrib['ArrivalTime']

        
    table = []
    table.append(r'\begin{table}[h]')
    table.append(r'\begin{center}')
    table.append(r'\begin{tabular}{cccccccr}')
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'Leg & Target & Obs Block & Pr & Elevation & UTC start & Duration & Altitude\\')
    table.append(r'\hline')
    table.append(r'\hline')
    
    for leg in root.iter('Leg'):
        name = str(leg.find('Name').text)
        name = name.replace("_", "\_")
        start = leg.find('Start').text
        duration = leg.find('Duration').text
        altitude = leg.find('Alt').text
        planid = leg.find('ObsPlanID')
        obBlockID = leg.find('ObsBlkID')
        priority = leg.find('Priority')
        if planid is None:
            planid = ''
            obBlockID = ''
            priority = ''
        else:
            planid = str(planid.text)
            obBlockID = str(obBlockID.text)
            priority = str(priority.text)
            if obBlockID == 'None':
                obBlockID = ''
                priority = ''
            else:
                obBlockID = obBlockID[3:]
            # Substitute underscore with \_
            planid = planid.replace("_", "\_")
            obBlockID = obBlockID.replace("_", "\_")
            if planid is None:
                planid = ''
                obBlockID = ''
                priority = ''
        elevation = leg.find('Elev')
        if elevation is not None:
            elstart = elevation.attrib['start']
            elend = elevation.attrib['end']
            elevation = elstart+'-'+elend
        else:
            elend = ''
            elstart=''
            elevation = ''
        ID = leg.attrib['id']
        ftype = leg.attrib['type']
        if ftype == 'Absolute':
            name = 'Climb'
        elif ftype == 'Arrival':
            name = 'Arrival'
        planid = planid.replace('None','')
        obBlockID = obBlockID.replace('None','')
        fmt = r'{0:2s} & {1:s} & {2:s} & {3:s} & {4:s} & {5:s} & {6:s} & {7:s}\\'
        altitude = altitude.replace('000','')
        altitude = altitude.replace('ft','Kft')
        line = fmt.format(ID, name, obBlockID, priority, elevation, start, duration[0:5], altitude)
        table.append(line)
        print(line)
        
    ID = planid = elevation = duration = ' '
    name = 'Landing'
    start = arrival[11:19]
    altitude = '0 Kft'
    line = fmt.format(ID, name, planid, '', elevation, start, duration, altitude)
    table.append(line)
    #print(line)
    name = 'Total flight time'
    start = altitude = ''
    duration = flightTime[:-3]
    line = fmt.format(ID, name, planid, '', elevation, start, duration, altitude)
    table.append(line)
    #print(line)
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'\end{tabular}')
    table.append(r'\end{center}')
    table.append(r'\end{table}')

    return table

def parsTable(fifiparsfile):
    import json
    with open(fifiparsfile,'r') as f:
        fifipars = json.load(f)
        
    table = [
        r'\begin{table}[ht]',
        r'\large',
        r'\begin{center}'
        r'\begin{tabular}{ll}',
        r'\hline',
        r'\hline',
        r'\noalign{\vskip 2mm}',
        r'Chop angle in J2000 & \textbf{Counter}clockwise from North\\',
        r'FOV angle in J2000 & \textbf{Counter}clockwise from North (blue)\\',
        r'\noalign{\vskip 2mm}',
        r'\hline',
        r'\hline',
        r'\noalign{\vskip 2mm}',
        r'Focus Position (xml) & '+str(fifipars['Focus Position (xml)'])+r'~mm\\',
        r'Focus Relation & '+str(fifipars['Focus Relation'])+r' $\mu$m secondary move is -1mm Focus point move\\',
        r'Blue bias Voltages & 75~mV\\',
        r'Red bias Voltages & 60~mV\\',
        r'Chopper Phase & 356$^o$\\',
        r'D130/D105 switch blue M2 & [OIII]51.815$\mu$m + 5000~km/s\\',
        r'Blue grating switch positions & Home/far: 44000/1910000 induct\\',
        r'Red grating switch positions & Home/far: 37000/1753000 induct\\',
        r'Blue spexel size & '+str(fifipars['Spexel size blue'])+r' induct\\',
        r'Red spexel size & '+str(fifipars['Spexel size red'])+r' induct\\',
        r'\noalign{\vskip 2mm}',
        r'\hline',
        r'\hline',
        r'\noalign{\vskip 2mm}',
        r'TO: \hspace{2.2cm} Focus at & '+str(fifipars['TO focus'])+r' $\mu$m\\',
        r'\noalign{\vskip 2mm}',
        r'KOSMA: \hspace{1.3cm} Setpoint: & --X: '+str(fifipars['Setpoint X'])+r'~arcsec\\',
        r'& --Y: '+str(fifipars['Setpoint Y'])+r'~arcsec\\',
        r'\noalign{\vskip 2mm}',
        r'TEL\_hardware\_status:&Instr\_rotator\_axis\_x = '+str(fifipars['Instr_rotator_axis_x'])+r'~mm\\',
        r'& Instr\_rotator\_axis\_y = '+str(fifipars['Instr_rotator_axis_y'])+r'~mm\\',
        r'In Rx\_hardware\_status [mm]:&\\',
        r'\hspace{3cm} BD130 &' + 'Rx\_cx[2] = {0:5.2f},  Rx\_cy[2] = {1:5.2f}'.format(fifipars['BD130 Rx_cx'],fifipars['BD130 Rx_cy'])+r'\\',
        r'\hspace{3cm} BD105 &' + 'Rx\_cx[1] = {0:5.2f},  Rx\_cy[1] = {1:5.2f}'.format(fifipars['BD105 Rx_cx'],fifipars['BD105 Rx_cy'])+r'\\',
        r'\hspace{3cm} Red   &' + 'Rx\_cx[0] = {0:5.2f},  Rx\_cy[0] = {1:5.2f}'.format(fifipars['Red Rx_cx'],fifipars['Red Rx_cy'])+r'\\',
        r'\noalign{\vskip 2mm}',
        r'K-Mirror 0 Position: &'+str(fifipars['K-mirror 0 Position'])+r'~steps\\',
        r'\hline',
        r'\hline',
        r'\end{tabular}',
        r'\end{center}',
        r'\end{table}'
        ]

    return table

def makeCover(aorfile, cycle):
    import xml.etree.ElementTree as ET
    import json
    import os
    
    path, fname = os.path.split(aorfile)
    names = fname.split('_')    
    filedescription = os.path.join(path,names[2]+'.json')
    with open(filedescription, 'r') as f:
        flight = json.load(f)
    sofian = flight['SofiaFlight']
    fifin = flight['FifiFlight']
    date = flight['FlightDate']

    cover = [
        r'\begin{titlepage}',
        r'\begin{center}',
        r'\vspace*{1cm}',
        #r'\textbf{\Huge FIFI-LS\\}',
        r'\includegraphics[width=0.35\textwidth]{fifilogosmall}\\',
        r'\vspace{0.5cm}',
        r'{\Huge\bf Flight Description\\}',
        r'\vspace{1.cm}',
        r'\includegraphics[width=0.7\textwidth]{sofia}\\',
        r'\vspace{2.cm}',
        r'\textbf{\sl\Large Obs Cycle: '+cycle+r'}\\',
        r'\vspace{0.5cm}',
        r'\textbf{\Large Flight name: '+names[2]+r'}\\',
        r'\vspace{0.5cm}',
        r'\textbf{\Large SOFIA flight: '+str(sofian)+r'}\\',
        r'\vspace{0.5cm}',
        r'\textbf{\Large FIFI-LS flight: '+str(fifin)+r'}\\',
        r'\vspace{0.5cm}',
        r'\textbf{\Large Date: '+date+r'}\\',
        r'\vfill',
        r'\end{center}',
        r'\end{titlepage}'
    ]
    
    return cover

def makePreamble():
    
    preamble = [
        r'\documentclass[10pt]{article}',
        r'\topmargin      -10mm',
        r'\oddsidemargin  -10mm',
        r'\evensidemargin 17mm ',
        r'\textwidth      180mm',
        r'\textheight     220mm',
        r'\usepackage{graphicx}',
        r'\usepackage{fancyhdr}',
        r'\usepackage{lastpage}',
        r'\renewcommand{\headrulewidth}{2pt}',
        r'\pagestyle{fancy}',
        r'\fancyhf{}',
        r'\rhead{FIFI-LS Flight Description}',
        #r'\fancyhead[L]{\leftmark}',
        r'\fancyhead[L]{\itshape\nouppercase{\leftmark}}',
        r'\rfoot{Page \thepage / \pageref{LastPage}}',
        r'\begin{document}'
        ]
    
    return preamble
    

def writeLatex(aorfile, cycle):
    import os
    
    preamble = makePreamble()
    cover = makeCover(aorfile, cycle)
    ftable = flightTable(aorfile)
    path, fname = os.path.split(aorfile)
    flighttable = flightTable(aorfile)
    fifiparstable = parsTable(os.path.join(path, 'fifils-pars-'+cycle+'.json'))
    
    mapfile = os.path.join(path, fname+'.png')
    # Grab flight name from fname
    names = fname.split('_')    
    filedescription = os.path.join(path,names[2]+'.json')
    filename =  os.path.join(path,names[2]+'.tex')
    
    # Save flight table
    flighttablefile = os.path.join(path, 'fifils-pars-'+cycle+'.tex')
    with open(flighttablefile, 'w') as f:
        for t in fifiparstable:
            f.write(t+'\n')
        
    
    with open(filename, 'w') as f:
        # Preamble
        for p in preamble:
            f.write(p+'\n')
        # Cover page
        for c in cover:
            f.write(c+'\n')
        # Definitions & Parameters
        f.write(r'\section{Definitions \& Parameters}'+'\n')
        # Insert Table
        #for t in fifiparstable:
        #    f.write(t+'\n')
        f.write(r'\input{"'+'fifils-pars-'+cycle+'.tex'+r'"}' + '\n')   
        # Flight Plan
        f.write(r'\section{Flight Plan}'+'\n')
        # Insert Figure
        f.write(r'\begin{center}'+'\n')
        f.write(r'\includegraphics[width=0.70\textwidth]{'+mapfile+'}'+'\n')
        f.write(r'\end{center}'+'\n')
        # Insert Table
        for t in flighttable:
            f.write(t+'\n')
        # Write a page for each obs-block
        with open(filedescription,'r') as jf:
            data = json.load(jf)
        obsBlocks = data['ObsBlocks']
        for obsBlock in obsBlocks:
            block = data[obsBlock]
            propid = block['propid']
            comment = block['comment'].replace('<br>','; ').replace('#','')
            
            title = block['title']
            propid = propid.replace("_", "\_")
            f.write(r'\section{'+title+'}\n')
            if len(title) > 70:
                f.write(r'\sectionmark{'+title[:70]+'...}\n')
            f.write(r'{\large {\bf AOR ID:} '+propid+ r' {\bf PI:} '+block['piname']+r'}\\'+'\n')
            f.write(r'{\bf Comments:} '+comment+r'\\'+'\n')
            # Insert Figure
            imagefile = block['imagefile']
            if imagefile is not None:
                f.write(r'\begin{center}'+'\n')
                f.write(r'\includegraphics[width=0.60\textwidth]{'+imagefile+'}'+'\n')
                f.write(r'\end{center}'+'\n')
            else:
                f.write(r'\newline'+'\n')    
            # Insert abstract            
            abstract = block['abstract']
            abstract = abstract.replace('>','$>$').replace('<','$<$')
            f.write(abstract+'\n')
        f.write(r'\end{document}')


def runLatex(aorfile):
    import os
    import platform
    import subprocess
    import psutil


    path, fname = os.path.split(aorfile)
    names = fname.split('_')    
    tex_filename =  os.path.join(path, names[2]+'.tex')
    pdf_filename =  os.path.join(path, names[2]+'.pdf')
    print('path ', path)
    print('tex file ',tex_filename)
    print('pdf file ',pdf_filename)
    # compile TeX file
    if path == '':
        path = './'
    subprocess.run(['pdflatex', '-interaction=nonstopmode', 
                    '-output-directory='+path, tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        # First kill Adobe Acrobat Reader
        for p in psutil.process_iter():
            if p.name() == 'AdobeReader':
                p.kill()
        # Then open the new pdf file
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))
