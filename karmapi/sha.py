"""
Spherical Harmonic Analysis and markov models.

And also, plotting as you go.

Navigating data.
"""


from karmapi import ncdf, tpot

import pyshtools
import curio
import matplotlib
from matplotlib import pyplot as plt
from blume.table import table
from blume import magic

import numpy as np

import datetime
from collections import Counter
import math
import time

def spectrum(value):


    clm = ncdf.to_sha(value[1:])

    return clm, pyshtools.spectralanalysis.spectrum(clm)


async def generate_spectra(df, queue=None,
                           lmax=10, mmax=10, power=False, delta=False,
                           month=None, topn=0, **kwargs):

    print('Calculating means across years')
    df.sum_years()
    print('Done means across years')

    spectra = []
    last = None
    lastdate = None
    vmax = vmin = None
    vmax = None
    vmin = None
    fig = plt.figure()
    fig.set_facecolor('black')

    for ix, (date, value) in enumerate(df.generate_data()):

        value = df.deviation(date, value)

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

            start = lmax
            clm[:, start:ww, start:hh] = 0.0
        
            xxxx = pyshtools.expand.MakeGridDH(clm)
            plot = xxxx
            #print(type(xxxx), xxxx.shape)

            #if True:
            perc = np.percentile
            if not month or date.month == month:
                print('lmax:', lmax)

                if vmax is None:
                    vmax = perc(plot, 95.)
                    vmin = perc(plot, 5.)
                    print('vmax/vmin', vmax, vmin)

                print(date, perc(plot, 5),
                      perc(plot, 95), plot.mean())

                fig.clear()
                
                #ax = fig.add_axes((0,0,1,1), projection='mollweide')
                ax = fig.add_subplot(1, 1, 1,
                                     projection='mollweide')
                lon = np.linspace(-np.pi, np.pi, plot.shape[1])
                lat = np.linspace(-np.pi/2, np.pi/2, plot.shape[0])
                lon, lat = np.meshgrid(lon, lat)
                ax.pcolormesh(lon, lat, plot[::-1], cmap=plt.cm.jet,
                              vmax=vmax, vmin=vmin)
                ax.set_title(str(date), color='white')
                ax.axis('off')
                key = (date.month, date.day, date.hour)

                if False:
                    ax = fig.add_subplot(2, 1, 2,
                                         projection='mollweide')

                    xxxx = df.totals[key][1:]
                    lon = np.linspace(-np.pi, np.pi, xxxx.shape[1])
                    lat = np.linspace(-np.pi/2, np.pi/2, xxxx.shape[0])
                    lon, lat = np.meshgrid(lon, lat)
                    ax.axis('off')

                    ax.pcolormesh(lon, lat, xxxx[::-1], cmap=plt.cm.jet)
                                  #vmax=vmax, vmin=vmin)

                plt.grid(True)

                await queue.put(magic.fig2data(fig))
                await curio.sleep(0)

        spectra.append(value)

        if lastdate and lastdate > date:
            break
        lastdate = date

        if topn and ix > topn:
            break


    print(f'FULL SET OF SPECTRA {len(spectra)} {len(spectra[0])}')
    return spectra


def stats(data):
    """ Return some standard stats """
    print("DATA STATS (shape, mean, var, percentiles)")
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
    samp = norm(size=shape)

    # old code below scales to original distro
    print(samp.shape)

    samp *= stds
    samp += means

    return samp

def normalise(data):

    means = data.mean(axis=0)
    stds = data.std(axis=0)
    #print(f'normalise {means}')
    #print(f'normalise {stds}')
    stds = np.where(stds==0.0,
                    np.ones(shape=stds.shape),
                    stds)
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
            #B[obs, state] = (abs(dist) ** 0.5)
            #print('B', obs, state, dist, math.e ** (-1 * dist))
            B[obs, state] = math.e ** (-1 * dist)

    return observations, B        

class TeaPlot(magic.Ball):

    def __init__(self, nstates=10, **kwargs):
        
        super().__init__(**kwargs)

        self.tplot = tpot.TeaPlot(**kwargs)

        # Like to change this so input comes over queues
        # with an end of queue
        self.nstates = nstates

        self.ins.add('spectra')
        self.outs.add('image')

        self.event_map = dict(
            t=self.tea)

    async def tea(self):

        print('time for tea')

    def beer(self):
        
        super().beer()

        rebrew(self)

    async def start(self):

        spectra = self.spectra
        nstates = self.nstates

        sample = random_sample(spectra, nstates)

        observations, B = make_bmatrix(spectra, sample)
        print('b matrix:', B[0])
        self.OBSERVATIONS = observations
        
        # generate random eh?
        A = np.random.random(size=(nstates, nstates))
        for i in range(nstates):
            A[i, :] /= A[i, :].sum()

        P0 = np.random.random(size=nstates)
        P0 /= P0.sum()
        self.A = A
        self.B = B
        self.P0 = P0

        self.OBSERVATIONS = observations

        # do one tpot round
        self.brew()
        self.beer()
        self.stir()
        print("Initial score", self.SCORE)

        # show a plot?
        plot = gamma_plot(self)
        await self.image.put(plot)

    async def run(self):

        
        print('TPOT filled, away we go')
        print(self.A)
        print(self.P0)
        self.stew(iters=1, epsilon=2.0)

        plot = gamma_plot(self)
        await self.image.put(plot)

        print(f'q size {self.queue.qsize()}')

        #for x in self.GAMMA[:10]:
        #    print(f'Gamma: {x}')

        await curio.sleep(1)
        


def gamma_plot(tpot):

    T, nstates = tpot.GAMMA.shape
    
    bottom = np.zeros(T, dtype=float)
    index = list(range(T))
    fig = plt.figure()
    ax = fig.add_subplot(211)
    data = tpot.GAMMA
    
    print(f'data shape {data.shape}')
    ax.imshow(data.T, aspect='auto')
    #for i in range(nstates):
    #    ax.bar(index, data[:, i], bottom=bottom)
    #    bottom += data[:, i]


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

    return magic.fig2data(fig)




def lager(tplot):
    """ Generate new set of states using tpot.GAMMA """


    spectra, nstates = tplot.spectra, tplot.nstates
    nstates = tplot.nstates
    
    states = np.zeros(shape=(nstates, len(spectra[0])), dtype=float)

    for obs, gam in zip(spectra, tplot.GAMMA):
        for state in range(nstates):
            states[state] += gam[state] * obs

    for i in range(nstates):
        states[i] /= sum(tplot.GAMMA[:, i])
            
    return states

def rebrew(tplot):
    """ Do re-estimation """
    # re-estimate states based on gamma
    states = lager(tplot)
    for state in states:
        print('State:', state)
        
    observations, B = make_bmatrix(tplot.spectra, states)

    tpot.B = B
    tpot.OBSERVATIONS = observations


class Sphere(magic.Ball):    
    # FIXME: fix so teapot waits on a queue for spectra
    #        need a queue where None means end of data?
    #
    #        And have it all just working as edges in the farm 


    def __init__(self, **args):

        super().__init__()

        # Now passed in as keywords
        self.df = ncdf.CircularField(**dargs)
        self.args = args
        self.outs.add('image')
        self.outs.add('spectra')

    async def run(self):

        args = self.args
        self.filter_stamps(hour=args.hour, day=args.day)

        #stamp_stats(df.stamps)
        spectra = await generate_spectra(df, self.image, **dargs)
        spectra = np.array(spectra)

        print(f'spectra zero shape {spectra[0].shape}')
    
        # fixme - save spectra somewhere and do faster load.
        # cf repeatability too.
        # maybe just normalise spectra?
        if args.norm:
            nspectra = normalise(spectra)
            stats(nspectra)
            spectra = nspectra

        await self.spectra.put(spectra)
    
def main():

    parser = ncdf.argument_parser()

    parser.add_argument('--plot', action='store_true')
    parser.add_argument('--topn', type=int, default=0)
    parser.add_argument('--lmax', type=int, default=10)
    parser.add_argument('--power', action='store_true')
    parser.add_argument('--norm', action='store_true')
    parser.add_argument('--nstates', type=int, default=10)

    parser.add_argument('--month', type=int)
    parser.add_argument('--day', type=int)
    parser.add_argument('--hour', type=int)

    args = parser.parse_args()


    curio.run(run(args))

async def run(args):

    # might be interesting to try to turn args into
    # coroutines that allow the values in args to be controlled
    # not sure where all that belongs, but should pass args to Farm?
    farm = magic.Farm(args)

    carpet = farm.carpet
    #await carpet.more()
    #await carpet.more()

    farm.setup()
    await farm.start()

    runner = await curio.spawn(farm.run())

    # magic to go from argparse to a dict
    dargs = args.__dict__

    sphere = Sphere(**dargs)
    
    farm.add_node(sphere)


        

            
    print(f'spectra zero shape {spectra[0].shape}')
    # TeaPlotter
    tea_plotter = TeaPlot(spectra=spectra,
                          nstates=args.nstates)

    
    tea_plotter.queue = carpet.incoming

    print('STARTING TEA PLOT')
    await tea_plotter.start()

    tplot_task = await curio.spawn(tea_plotter.run())

    print(tplot_task)

    await runner.join()

    await tplot_task.cancel()

    

if __name__ == '__main__':

    main()
    #parser = ncdf.argument_parser()

    #args = parser.parse_args()

    #df = ncdf.CircularField(args)
