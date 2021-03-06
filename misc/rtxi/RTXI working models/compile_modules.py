import os
import sys
from time import strftime, localtime

# Usage
#   python compile_modules.py  -- compile and install listed modules
#   python compile_modules.py zip -- create backup zip file of all files
#   python compile_modules.py clean -- delete autogenerated files

# various files we care about to produce a useful RTXI environment
models = ['OUSyn/', 'SpikeDetect/', 'IZCell/', 'SpikeRateController/', \
          'KV/', 'Autapse/','Istep/', 'SumPSG/', 'acquire/', 'synch/', 'LIF/', 'Imi/', 'MeanVm/']
settings = ['settings/']
include = ['include/']
files = ['compile_modules.py']

# delete all the crud
def clean(mod, inc):
    for m in mod:
        os.chdir(m)
        os.system('make clean')
        #os.system('rm -rf ./libs')
        os.system('rm *~')
        os.chdir('..')

    os.chdir(inc[0])
    os.system('rm -rf ./.libs *.o *.lo *~')
    os.chdir('..')
    os.system('rm *~')
   

# create zip file will all files and a time stamp
def myzip(f):
    # print files
    output = 'working_models_%s.zip' % strftime('%Y-%m-%d', localtime())
    if (os.path.exists(output)):
        os.remove(output)  # incase file already exists
    cmd = 'zip -r %s %s' % (output, ' '.join(f))
    print cmd
    os.system(cmd)
    

# delete anything auto generated
if (len(sys.argv) == 2 and sys.argv[1] == 'clean'):
    clean(models, include)
    sys.exit(0)

# produce backup zip file
if (len(sys.argv) == 2 and sys.argv[1] == 'zip'):
    print('Cleaning ...')
    clean(models, include)
    print('Zipping ...')
    myzip(models + settings + include + files)
    sys.exit(0)
    

# install extra packages for OUSyn, newer RTXI seems to have this already
os.system('sudo apt-get install libgsl0-dev')

# go through and compile everything
for m in models:
    os.chdir(m)
    os.system('make; sudo make install')
    os.chdir('..')






