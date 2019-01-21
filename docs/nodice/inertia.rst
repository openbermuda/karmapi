=========
 Inertia
=========

When I started this story I was thinking about all sorts of inertia in
society.

It usually begins with a quantum leap, a new perspective on an old
idea?

Things that once took months or years now could be done in a day.

Spreadsheets were a revelation to many and made it easy to find new
in-sights.

The tools helped you learn what could be done.

All around others were discovering other tools, new computer
languages, perl, php, python and parrot.

Each making it orders of magnitude easier to get the task done, but
then an avalanche of new ideas as ridges are reached.

A paradigm shift, climb up a higher mountain and see what could only
be dreamed of before.

The new paradigm explains much, assumptions turn into facts, or rather
disappear from the discourse.

Take, *The big bang theory*, the universe is expanding, it must have been tiny
once, not so very long ago.

But what if our window on the universe is just that, a glimpse of
something larger, seen through the blur of the Hooke telescope
Monument?

And expanding and contracting at one and the same?

Now for some history of gravitational waves.


Michelsson-Morley experiment
============================

In 1887, Albert A. Michelson and Edward W. Morley conducted an
experiment in Cleveland, Ohio.

The experiment took a beam of light, split it into perpendicular
directions and measure the difference in the speed of light in the two
directions.

It was assumed there would be a difference, but there wasn't.

The beam of light took the same time in both directions regardless how
the equipment was orientated.

The apparatus was mounted on a slab of rock floating in a giant bath
of liquid mercury.

It was this experiment's failure that eventually led to Einstein's
special relativity.
 
LIGO
====

Fast-forward to today and we have a repeat of the Michelson-Morley
experiment, but on a giant scale.

The *Laser Interferometer Gravitational-wave Observatory* is an
international collaboration centred around two giant experiments, with
vaccuum tubes arranged in an **L** with each arm 4km long.

It has taken over 20 years to get it to the current sensitivity.

It splits a beam of light and sends each part of the light on a 20km
journey, up and down the arms and measures the time difference of
arrival of the waves.

On September 14th 2015 the observatory recorded a signal, the same
signal being observed at both observatories, with a 7ms delay.

The time difference was following a smooth wave, that rose in
frequency, until it reached the limit of the equiment sensitivity
(10-500Hz range?).

It had been speculated that black holes colliding with each other,
slowly spiralling into each other, with the spirals getting faster and
faster, until the holes merge into a single entity, would generate a
gravitational wave, in that it would send a ripple through space time,
that would cause a ripple in any light or matter passing that way.

Simulations have been run and a number of software packages that will
take a waveform and try a range of parameters for the masses of the
two bodies colliding and finding the best match to the data.

The software also gives an estimate of the distance based on the
intensity of the wave when received at LIGO compared to that at the
actual collision.



Black holes colliding
=====================


*m_1* mass of larger object


*m_2* mass of smaller object

*r* distance from observatory

Events are assumed to be rare, hence none so far none have been near to home.

When a detection is made the waveform is compared to a catalogue of
potential impacts and the closest match declared the answer.

There are multiple software libraries involved, but broad agreement of
how these collisions behave.

Some simplifying assumptions such as any rotation the two bodies have
are included.

It is likely that the Kerr metric (I need to do some digging in the
software here) has been used.

Alternatively, I can work from the parameters announced for each
collision, simulate what I think the wave should look like and compare
to the data.

Regardless of which metric is actually in play we can proceed as
follows:

1. Decide how we might expect (m_1, m_2, r) to be distributed.

2. Take a sample from that distribution and use it to generate a
   family of curves with your favourite model, *A*.

3. Feed the curves to model B, and see if the distribution of *m_i*
   and *r* are as expected.

I am not sure how much difference the metric will make in this case,
but at least I can take a look and in the process get a better feel
for state of the art black hole collision ideas.

Deciding how *m_1* and *m_2* might be distributed is likely biassed by
the model that is being used for the universe.

Just what sized objects do we actually expect to spiral into each
other?

Is it the case that some particular masses spiral more rapidly than
others which will very gently coalesce over time?

How are the current models handling the influence of the black holes
on propogation of any gravitational wave that the collision emits?


Neutron stars too
-----------------

There have been detections thought to be due to a neutron star
colliding with a black hole, or possibly another neutron star.


Gamma ray bursts
================

For at least two of the observations a short duration gamma ray burst
was observed a couple of seconds after the gravitational wave passed.

For one of the neutron star events, there were a lot of other
coincident observations: gamma ray bursts, xrays, visible light,
dropping in frequency and intensity over time.

It is suggested that with a neutron star involved all sorts of
additional radiation could be expected.


Another Paradigm
================

Colin Rourke's *Another paradigm for the universe* suggests that
gamma-ray bursts may in fact an optical illusion, as we see the
*quasi-infinite* past of a universe just arriving in our visible
universe.

It is all a result of the paths of the *geodesics* in the *de Sitter*
space used to model our part of the universe, our visible universe.

This opens up the intriguing possibility, that a new arrival will also
be a strong source of gravitational waves.

Since the gravitational field of a galaxy's central black hole extends
well beyond the visible universe, it is reasonable to assume that the
onset of the arrival of the gravitational wave will precede the
arrival of any light from the galaxy.

Further, it should be noted that the gravitational wave also modulates
the light, as it is in essence, part of the carrier wave.


Why no gravitational waves for long duration gamma-ray bursts?
--------------------------------------------------------------

This is a puzzle for the time being.  The current detectors have upper
and lower bound on the frequency that they can detect.

I am also not sure how the waves get modulated when you take into
account the way the central black hole itself distorts space time.

I believe *anoptu* discusses geodesics can follow a cusp-like path?

This would allow lots of opportunity for modulation of the wave.


Personal View
=============

What is not in doubt is what a remarkable international collaboration
the work to detect these gravitational waves.

It is a truly stunning achievement.

The LIGO (and Virgo) observatories are indeed detecting stunning
ripples in space time.   

The accepted interpretation is that the waves we are seeing are actually
caused by distant collisions of black holes.

This is open to question, although such question should be supported
by another explanation for the waves, preferably one that is testable
by experiment.

Pending the arrival of more observations, it may be useful to run some
simulations to see in what ways the various models and assumptions
vary in terms of the observations we see.

I believe that it will soon become clear whether there really is a
deficit of local events.   This would likely be a first indication
that the current explanation is incorrect, although the picture may be
murky for a while longer.


Virgo
=====

More recently a third detector has become operational, based in Italy.


Spring 2019
===========

Expecting lots of new data to come from the spring LIGO production
runs.

With multiple detectors running there will also be better sky
localisation of the source of any waves.

Foot note
=========

I have been re-reading *Another Paradigm for the Universe*, particular
chapter two, which talks about inertial drag fields and develops a
model where the influence a distant mass has on the local inertial
frame is proportional to that mass and inversely proportional to its
*distance*.

Or, to put another way, the effect of the gravitational wave drops off
linearly with distance.  There is a lot in this chapter to support the
$1/r$ relationship.

When I have read this before I was happy to take this as a given and
now I had to think why so?

I had been thinking of concentric circles (slices along a great circle
through nested spheres), with the diameter of the n'th circle being
$n$.

In short assuming the amplitude of the wave would drop from the n-th
to the (n+1)th circle by just enough to add an extra copy of the wave.


Now consider, a dumbel with the same mass at each end with a bar one
unit long separating the masses, rotating with some angular velocity,
$\omega$.


Now imagine how this wave might sweep out to concentric circles of
diameter 2, 3, 4, 5,.. units away.

Each band is just $\pi$ units longer than the previous band.  Rather
think of the wave itself spiralling outwards.

Suppose there is a steady source of waves (a nearby rotating black
hole?).
 
 
As the wave radiates from the source, little energy is lost as the
wave moves out to wider and wider circles.  Energy, in the form of
gravitational waves dissipates into the surrounding region, but each
shell of unit size contains the same energy.


Each band is just one wavelength longer than the previous so there is
just one extra wave to spread the energy across.

With steady new waves being created at the central ring.

So the energy at a distance n from the source wave is just 1 / n times
the energy in the inner band.


So the energy in the inner, unit circle spread out to a 2-unit
circle, the wave height halving.

From 2 to 3 the energy for unit area drops to 2/3 of level 2.

In general, going from level n to n + 1, the energy drops by
$n / (n + 1)$. But now there are n+1 waves, so the total energy is preserved.

Prod (i / (i + 1)) for i in 1, 2, 3, ...., n

But isn't it just 1 / n?  Yes, in the sense of n waves going round a
circle of length n, each with amplitude 1/n of the inner wave.

Did I forget about time?

If we get too close to the black hole we see the effects of general
relativity and things get complicated very quickly.

Fortunately, we can set our unit of distance so that we start a
respectable distance from the centre of the black hole, where we can
assume that the gravitational waves are propogating at close to the
speed of light, relative to the black hole.

Within a few radii, the effect will be negligible.





Or maybe
--------

Imagine the ripples on a calm lake created by an apple dropping from a
tree.  Or rather a ripples created by the tip of a long branch,
dipping into a calm pond.  You can gently rock the branch to create
waves.

Swirl it round in a gentle circle and watch the waves move out across
the lake, a self-supporting spiral of waves.


Arrival of a new galaxy
=======================

There is something rather elegant in the idea that when a new galaxy
enters our visible universe it greets us, at a respectful distance of
12 billion light years with an update on it's entire history prior to
this, or our last meeting if per chance we have met before.

This update could be viewed as an adjustment to our inertial frame to
represent the distant matter that is just now beginning to affect our
inertial frame.


References
==========

For Colin's work, I recommend his home page at Warwick University::

  http://msp.warwick.ac.uk/~cpr


  
  https://arxiv.org/abs/astro-ph/0311033


For data and information on gravitational waves, the Gravitational
Wave Open Science Centre is invaluable::

   https://www.gw-openscience.org/
  

  

For more details, https://wikipedia.org has been an invaluable
starting point.  
