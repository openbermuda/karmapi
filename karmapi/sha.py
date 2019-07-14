
from karmapi import ncdf, tpot

import pyshtools

from matplotlib import pyplot as plt
from blume.table import table

import numpy as np

import datetime
from collections import Counter

def spectrum(value):


    clm = ncdf.to_sha(value[1:])

    return clm, pyshtools.spectralanalysis.spectrum(clm)


def generate_spectra(df, lmax=10, mmax=10, power=False, delta=False,
                     topn=0):

    spectra = []
    last = None
    lastdate = None
    for ix, (value, stamp) in enumerate(ncdf.generate_data(df.stamps, df.values)):
        ss, date, nix = stamp

        if last is None:
            last = value
            continue

        if delta:
            value = last - value

        clm, spect = spectrum(value)
        if power:
            print('SPECT:', spect)
            value = spect
        else:
            value = np.append(clm[0][:lmax, :lmax],
                              clm[1][:lmax, :lmax])
            junk, ww, hh = clm.shape

            start = 20
            clm[:, start:ww, start:hh] = 0.0
            
            xxxx = pyshtools.expand.MakeGridDH(clm)
            print(type(xxxx), xxxx.shape)
            print(date)
            if date.month == 1:
                fig = plt.figure()
                ax = fig.add_axes((0,0,1,1), projection='mollweide')
                ax.imshow(xxxx)
                plt.show()
            

            #value = value.flatten()
            #print('ix, value.shape', ix, value.shape)
            
        spectra.append(value)

        if lastdate and lastdate > date:
            break
        lastdate = date

        if topn and ix > topn:
            break

    print(f'FULL SET OF SPECTRA {len(spectra)} {len(spectra[0])}')
    return spectra


def plots(df):    

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

        #print(f'SPECT {spect.cumsum()/spect.sum()}')

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
    
def stats(data):
    """ Return some standard stats """
    print("DATA STAtS (shape, mean, var, percentiles)")
    print(data.shape)
    print(data.mean())
    print(data.var())
    print(np.percentile(data.cumsum(), [0.25, 0.5, 0.75, 0.9, 0.99]))
    print()
    means = data.mean(axis=0)
    print(f'means: {means.shape}')
    stds = data.std(axis=0)
    print(f'stds:  {stds.shape}') 

    for x in range(12):
        print(means[10*x:10 + (10 * x)])
    print()


def random_sample(data, n):

    norm = np.random.normal
    means = data.mean(axis=0)
    stds = data.std(axis=0)

    shape = [n] + list(means.shape)
    return norm(size=shape)

    # old code below scales to original distro
    print(samp.shape)

    samp *= stds
    samp += means

    return samp

def normalise(data):

    means = data.mean(axis=0)
    stds = data.std(axis=0)
    print(f'normalise {means}')
    print(f'normalise {stds}')
    data -= means
    data /= stds

    return data


def stamp_stats(stamps):

    dates = [x[1] for x in stamps]
    hours = Counter(x.hour for x in dates)
    hhours = Counter(x.hour for x in dates[:int(len(dates)/2)])
    months = Counter((x.year, x.month) for x in dates)

    print(hours)
    print(hhours)
    print(months)

def make_bmatrix(spectra, states):
    """ """
    nstates = len(states)
    # calculate probs given observations
    B = np.zeros(shape=(len(spectra), nstates), dtype=float)

    observations = []
    for obs, spect in enumerate(spectra):
        observations.append(obs)

        for state, ss in enumerate(states):
            dist = spect.dot(ss)

            #distance /= (ss + 1) ** 0.5

            # FIXME? need to convert distance to prob
            # but teapot will deal with any linear scaling
            # so prob e ** x or log(x) here ... or all ok?
            
            #print(obs, state, dist)
            B[obs, state] = (abs(dist) ** 0.5)

    return observations, B        


def brew(spectra, nstates=10):
    """ Perform tpot algorithm """

    sample = random_sample(spectra, nstates)

    observations, B = make_bmatrix(spectra, sample)

    # generate random eh?
    A = np.random.random(size=(nstates, nstates))
    for i in range(nstates):
        A[i, :] /= A[i, :].sum()

    P0 = np.random.random(size=nstates)
    P0 /= P0.sum()

    tpot.A = A
    tpot.B = B
    tpot.P0 = P0

    tpot.OBSERVATIONS = observations

    print('TPOT filled, away we go')
    nsteps = 100
    lastscore = None
    for step in range(nsteps):

        tpot.brew()

        print(f'Step {step} score {tpot.SCORE}')

        # re-estimage A, B, P0
        tpot.beer()
        rebrew(spectra, nstates)
        tpot.stir()

        if step % 25 == 0:
            print(tpot.A)
            gamma_plot()

        if step > 25:
            if (tpot.SCORE - lastscore) < 1.0:
                break

        lastscore = tpot.SCORE
        
    gamma_plot()
    for x in tpot.GAMMA[:10]:
        print(f'Gamma: {x}')


def gamma_plot():

    T, nstates = tpot.GAMMA.shape
    
    bottom = np.zeros(T, dtype=float)
    index = list(range(T))
    fig = plt.figure()
    ax = fig.add_subplot(211)
    data = tpot.GAMMA
    print(f'data shape {data.shape}')
    for i in range(nstates):
        ax.bar(index, data[:, i], bottom=bottom)
        bottom += data[:, i]


    from matplotlib import colors, cm
    norm = colors.Normalize()

    colours = cm.get_cmap()(norm(tpot.A))
    alpha = 0.2
    colours[:, :, 3] = alpha
        
    ax = fig.add_subplot(212)
    ax.axis('off')
    tab = table(ax,
                cellColours=colours,
                cellEdgeColours=colours,
                bbox=(0, 0, 1, 1))
    plt.show()


def lager(spectra, nstates):
    """ Generate new set of states using tpot.GAMMA """

    states = np.zeros(shape=(nstates, len(spectra[0])), dtype=float)

    for obs, gam in zip(spectra, tpot.GAMMA):
        for state in range(nstates):
            states[state] += gam[state] * obs

    for i in range(nstates):
        states[i] /= sum(tpot.GAMMA[:, i])
            
    return states

def rebrew(spectra, nstates):
    """ Do re-estimation """
    # re-estimate states based on gamma
    states = lager(spectra, nstates)
        
    observations, B = make_bmatrix(spectra, states)

    tpot.B = B
    tpot.OBSERVATIONS = observations


def main():

    parser = ncdf.argument_parser()

    parser.add_argument('--plot', action='store_true')
    parser.add_argument('--topn', type=int, default=0)
    parser.add_argument('--power', action='store_true')
    parser.add_argument('--norm', action='store_true')
    parser.add_argument('--day', type=int)
    parser.add_argument('--hour', type=int)

    args = parser.parse_args()

    df = ncdf.CircularField(args)

    df.filter_stamps(hour=args.hour, day=args.day)

    if args.plot:
        plots(df)
        return

    topn = 20
    #stamp_stats(df.stamps)
    spectra = np.array(generate_spectra(
        df,
        topn=args.topn,
        power=args.power,
        delta=args.delta))
    print(f'spectra zero shape {spectra[0].shape}')

    # fixme - save spectra somewhere and do faster load.
    # cf repeatability too.

    stats(spectra)

    # maybe just normalise spectra?
    if args.norm:
        nspectra = normalise(spectra)
        stats(nspectra)
        spectra = nspectra

    sample = random_sample(spectra, 10)

    stats(sample)

    brew(spectra, 10)


if __name__ == '__main__':

    main()
    #parser = ncdf.argument_parser()

    #args = parser.parse_args()

    #df = ncdf.CircularField(args)
