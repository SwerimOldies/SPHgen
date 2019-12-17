# SPHgen

Fills a STL geometry with SPH particles output formatted according to
LS-Dyna input file structure 


### Main Features
* Reads an STL
* Fills the geometry with SPH particles of desired size
* Outputs the SPH part of a fixed format input-file for LS-Dyna 

The SPH part has the number 9 in the k-file.

It can be opened in LSprepost for model bulding. 
LS-PrePost is an advanced pre and post-processor that is delivered
at no cost with LS-DYNA. LS-Dyna is written, sold and supported by
Livermore Software Technology Corporation. LSprepost can be downloaded at:

```
http://www.lstc.com/lspp/
```

### How to run
```
git clone https://github.com/Xnst/SPHgen.git
cd SPHgen
python3 SPHgen.py -i ~/path/to/file.stl [-s size] [-o ~/path/to/outfile.k]
```


### Packages required
* python3 (already installed with ubuntu)
* python3-numpy
* numpy-stl (installed with pip3)

### built on

SPHgen is built on the FAME package

```
https://github.com/swerea/FAME.git

```

and on the stl-to-voxel package

```
https://github.com/rcpedersen/stl-to-voxel.git

```
