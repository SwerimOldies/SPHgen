#!/usr/bin/env python3

"""
Created on Thu Nov 19 06:37:35 2013

@author: Niclas Stenberg

"""


import numpy as np
import stltovoxel
import stltovoxel.stl_reader
from stltovoxel import slice
from stltovoxel import util

def readVoxels(inputFilePath,sphSize):
    
    mesh = list(stltovoxel.stl_reader.read_stl_verticies(inputFilePath))
    (scale, shift, bounding_box) = stltovoxel.slice.calculateScaleAndShift(mesh, sphSize)
    mesh = list(slice.scaleAndShiftMesh(mesh, scale, shift))
    #Note: vol should be addressed with vol[z][x][y]
    vol = np.zeros((bounding_box[2],bounding_box[0],bounding_box[1]), dtype=bool)
    for height in range(bounding_box[2]):
        print('Processing layer %d/%d'%(height+1,bounding_box[2]))
        lines = slice.toIntersectingLines(mesh, height)
        prepixel = np.zeros((bounding_box[0], bounding_box[1]), dtype=bool)
        stltovoxel.perimeter.linesToVoxels(lines, prepixel)
        vol[height] = prepixel
    vol, bounding_box = util.padVoxelArray(vol)
    return (vol,bounding_box,scale,shift)

    
def run(sphsize,STLFilename,outputFilename):
    import uuid
    uid=str(uuid.uuid4())
    (vol,bounding_box,scale,shift)=readVoxels(STLFilename,sphsize)
    print(bounding_box,scale,shift)
    totalLayers=0
    #
    volym=sphsize**3
    sphmassa=7.8e-09*volym
    #
    print('Generating SPHmesh...')

    fut=open('sphnodesX.txt','w')
    fut.write('*NODE\n')
    fut.write('$#   nid               x               y               z      tc      rc\n')
    fut.write('$#-----7--------------23--------------39--------------55------64------72\n')

    nodeNumBase= 0
    nodenum = nodeNumBase
    for k in range(bounding_box[2]):
        totalLayers+=1
        print('layer '+str(k+1)+' / '+str(bounding_box[2]))
        for j in range(bounding_box[1]):
            for i in range(bounding_box[0]):
                if vol[k][i][j]==True:
                    x=(i-1)/scale[0]-shift[0]
                    y=(j-1)/scale[1]-shift[1]
                    z=(k-1)/scale[2]-shift[2]
                    nodenum +=1
                    nodstrang = "                                                               0       0\n"
                    #  node number
                    plac = 7+1
                    for char in str("%7d" % nodenum)[::-1]:
                        plac+=-1
                        nodstrang = nodstrang[:plac] + char + nodstrang[plac + 1:]
                    # x coord
                    plac = 23+1
                    for char in str("%5.6e" % x)[::-1]:
                        plac+=-1
                        nodstrang = nodstrang[:plac] + char + nodstrang[plac + 1:]
                    # y coord
                    plac = 39+1
                    for char in str("%5.6e" % y)[::-1]:
                        plac+=-1
                        nodstrang = nodstrang[:plac] + char + nodstrang[plac + 1:]
                    # z coord
                    plac = 55+1
                    for char in str("%5.6e" % z)[::-1]:
                        plac+=-1
                        nodstrang = nodstrang[:plac] + char + nodstrang[plac + 1:]
                    # write to file
                    fut.write(nodstrang)
                    #       #  74490    3.685790e-02       -1.300000    3.224650e-03       0       0

    fut.close()
    fpid = open('sphpidX.pid','w')
    fpid.write("*KEYWORD  \n")
    fpid.write("*PART\n")

    fpid.write("$#   title\n")
    fpid.write("SphNode\n")
    fpid.write("$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid\n")
    fpid.write("         9         0         0         0         0         0         0         0\n")
    fpid.write("*ELEMENT_SPH\n")
    fpid.write("$#   nid     pid            mass    \n")
    #             130583       9    2.311110e-09

    for nodnum in range(nodeNumBase+1,nodenum+1):
        prstrang="       1       9                \n"
        #  node number
        plac = 7+1
        for char in str("%7d" % nodnum)[::-1]:
            plac+=-1
            prstrang = prstrang[:plac] + char + prstrang[plac + 1:]
        plac = 31+1
        for char in str("%5.6e" % sphmassa)[::-1]:
            plac+=-1
            prstrang = prstrang[:plac] + char + prstrang[plac + 1:]
        fpid.write(prstrang)
        
    fpid.close()

    fut=open(outputFilename,'w')
    fin2=open('sphnodesX.txt','r')
    fin1 = open('sphpidX.pid','r')
    for line in fin1:
        fut.write(line)
    for line in fin2:
        fut.write(line)
    fin1.close()
    fin2.close()
    fut.close()
    
                    
#   --   MAIN   ---
#
if __name__ == "__main__":
    print("""
    ------------------------------------------------
   |                     SPHgen                     |
   |        writes SPHnode card for LS-Dyna         |   
    ------------------------------------------------
    """)
    import getopt,sys,os
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'i:s:o:')
    except getopt.GetoptError as err:
        print(str(err))
        print('\n ---------- \n')
        print(' $ python3 SPHgen -i filename.stl [-s SPHsize(default=0.5)] [-o Output filename]\n')
        run=False
    sphsize=0.5
    outputFilename="default.sph"
    for o, a in opts:
        print(o,a)
        if o in '-i':
            STLFilename=a
        if o in '-s':
            sphsize=float(a)
        if o in '-o':
            outputFilename=a;

    inFileName, inFileExtension = os.path.splitext(STLFilename)
    if outputFilename == "default.sph":
        outputFilename = inFileName+".sph"
    
    # parameters=readParameters(parameterFilename)
    run(sphsize,STLFilename,outputFilename)
    
        
