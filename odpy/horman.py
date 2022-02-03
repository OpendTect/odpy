import numpy as np
import tempfile as tp
import os, shutil
from odpy.common import isLux, isWin

def create_horizon_file(data, inl_range, crl_range):
    """ Creates horizon file in .char format

    Parameters:
        * data (arr): 2D array of Z values; inlines in first dimension, and xlines in second dimension
        * inl_range(range): of absolute (survey) inlines range
        * crl_range (range): of absolute (survey) crosslines range

    Returns:
    * str: file name of created horizon data stored in present working directory
    """

    undef = 1e+30
    fd, fpath = tp.mkstemp(suffix='.char', prefix='', dir=None, text=True)
    with open(fpath, mode='w') as file:
        for inl,idx in zip(range(inl_range.start, inl_range.stop+1,inl_range.step),range(data.shape[0])):
            for crl,jdx in zip(range(crl_range.start, crl_range.stop+1, crl_range.step),range(data.shape[1])):
                Z = np.round(data[idx][jdx], 1)
                if Z < undef:
                    file.write(f'{idx} {jdx} {Z}\n')
                    
    os.close(fd)
    shutil.copy(file.name, './')
    os.remove(fpath)
    if isWin():
        return fpath.split('\\')[-1]
    elif isLux():
        return fpath.split('/')[-1]