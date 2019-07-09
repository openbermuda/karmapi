
from karmapi import ncdf

import pyshtools

from matplotlib import pyplot as plt

import numpy as np

import datetime

def spectrum(value):


    clm = ncdf.to_sha(value[1:])

    return clm, pyshtools.spectralanalysis.spectrum(clm)


def main():

    parser = ncdf.argument_parser()

    args = parser.parse_args()

    df = ncdf.CircularField(args)

    last = None

    spectra = []
    for value, stamp in ncdf.generate_data(df.stamps, df.values):
        ss, date, ix = stamp
        print(date)

        if last is None:
            last = value
            continue

        delta = last - value

        clm, spect = spectrum(delta)
        spectra.append(spect)

        print(f'SPECT {spect.cumsum()/spect.sum()}')

        if date >= datetime.datetime(1990, 1, 1):
            break

        #continue

        plt.plot(spect.cumsum()/spect.sum())
        plt.grid(True)
        plt.show()


        grid = pyshtools.SHCoeffs.from_random(spect).expand()
        plt.subplot(1, 3, 1)
        plt.imshow(grid.to_array())

        plt.subplot(1, 3, 2)
        plt.imshow(delta)

        print(type(clm))
        #clm[:,:,20:] = 0.0
        fgrid = pyshtools.expand.MakeGridDH(clm)
        plt.subplot(1, 3, 3)
        plt.imshow(fgrid)
        break

        #plt.plot(power[3:])
        #plt.grid(True)
        #plt.plot(power)
        
        plt.title(date)
        plt.imshow(grid)
        break

        last = value
        
        if ix >= 12:
            break
        


    plt.show()

    sp = np.array(spectra)

    print(sp.mean(axis=0))
    print(sp.var(axis=0))
    print(sp.shape)
    


if __name__ == '__main__':

    main()
    #parser = ncdf.argument_parser()

    #args = parser.parse_args()

    #df = ncdf.CircularField(args)
