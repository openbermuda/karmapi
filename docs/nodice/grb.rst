==================
 Gamma Ray Bursts
==================

I am continuing to enjoy Colin Rourke's, "A new paradigm for the
universe".

*Appendix G: Gamma Ray Bursts* has my focus at the moment.

It is a summary of a joint paper with R MacKay::

  Are gamma-ray bursts optical illusions?

  Palestinian J Math 5(Spec.1) (2016) 175--197

  http://msp.warwick.ac.uk/~cpr/paradigm/GammaRayBursts.pdf

You can find it on the book on the web::

  http://msp.warwick.ac.uk/~cpr/paradigm/paradigm.pdf

Or you can get a paper copy::

  https://www.amazon.ca/new-paradigm-universe-Colin-Rourke-ebook/dp/B076PWQS7M/

I am finding the mathematics heavy going, but the commentary and the
ideas are making sense intuitively, at least if I am understanding
things correctly.

The paper posits that gamma ray bursts are in fact the result of an
emitter, that has been invisible to us for an essentially infinite [1]
amount of time, suddenly becomes visible.

The emitter is assumed(?) to be adjacent to a black hole, a point in
space time where time is slowed by the intense gravitational field.

View a black hole as a place where time slows down.

As such it acts as a giant capacitor, storing up energy before
releasing a burst to the surrounding universe.


Conversation with Colin and Johnny
==================================

Gamma ray bursts in wikipedia land
----------------------------------

introduction and background field
=================================

Below is a conversation based on an exchange of emails.

One thing I am finding is how easy it is to be spectacularly wrong,
yet a slight adjustment in perspective give significant insights.

So I have been reading Colin's book for a while now and it is truly a
fascinating universe.

The current focus relates to gama ray bursts, and Colin's explanation
of what they may be.

Johnny
------

Hi Colin,

I've been reading some wikipedia on gamma ray bursts.

There are some interesting data and other gems out there.

https://en.wikipedia.org/wiki/Gamma-ray_burst

This one, when the universe was just 630 million years old:

https://en.wikipedia.org/wiki/GRB_090423

Interesting as you unravel the observations from the explanations.

On the gamma ray bursts, particularly the energy calculations, seem
to be making assumptions about a wave radiating in all directions.

This one z=9:

https://en.wikipedia.org/wiki/GRB_090429B

The article talks about energy produced, the assumption being that a
giant wave went out in all directions.


In your model (de Sitter space), it is just the way the horizon
works, buffering light for a while.

Your model is very energy efficient, just a galaxy coming over the
horizon at the speed of light towards us, important to recognise
that from it's point of view, nothing dramatic happening, except
perhaps a burst in the other direction as our galaxy emerged in
their visible universe?

Likely will continue to have a velocity towards us, creating blue
shift, so things may be further away than they seem.

Then there is this:

https://en.wikipedia.org/wiki/Gamma-ray_burst#/media/File:BATSE_2704.jpg

And wondering how it might relate to CMB?

I haven't look closely, but as far as I can tell there are no
confirmed reports of GRB originating nearby, at least these giant
explosions of energy, which is just as well.

It would be useful if there was some way to predict the distribution
of velocities of the galaxies becoming visible that we might expect.

I guess it might be possible to reverse this and assume all GRB
(subject to some filtering?) originate at the edge of the universe
as a galaxy becomes visible.

Use the observed red shift to figure out the velocity, relative to us?   


Colin
-----

The red shifts are artefacts.  The GRB comes over the horizon at
nominally infinite speed, so infinite blueshift.  They get redshifts by
guessing a nearby galaxy, which in our model is just a galaxy in the
same direction.

There is nothing going on nearly.  These are optical illusions NOT
real explosions.

The horizon effect as described in the CMB appendix cuts the
infinite blueshift down the observed limit (high gamma ray frequency).
It all needs proper modelling.

Johnny
------
  
**Got it**.  No emitter actually has to make it into our visible
universe, just a beam of light from that emitter.  

I picture things as light beams like rubber bands that are stretched
and squeezed.

I've started to work through the "Are gamma-ray bursts optical illusions".

The mathematics hurts my head at times, but I find the plots of u
(emitter "true" time) versus t (receiver time) pretty much show what
is going on.

Thanks for the guidance here, the picture makes more and more sense.

If we just go with the assumptions 

1. that the universe is pretty uniform round our way 

2. our visible universe is just a window on a wider universe
   and maybe:

3. Our part appears to be expansive

Then these optical illusions should be a pretty regular occurrence.

I've been thinking a lot about -t, the potentially infinite past of the source.

Potentially, it is limited by the age of the universe where the light
is being emitted, but from the paradigm that can be a potentially
enormous age.

More generally, the length of -t would be limited by the relative
movement of the receiver and emitter in the distant past.

It seems we should be able to put some bounds on -t.

Oh and I see from your email there may be a CMB connection, that
reminds me I need to revisit the CMB.

One other thought, the relative movement of the emitter and receiver
allows for a lot of variation in the exact structure of the grb --
which is indeed what we see.

I've read reports of GRB bursts where on detection they point powerful
telescopes in the x-ray and visible spectrums and see a decay from the
GRB through x-ray to a red shift which then fades -- which I believe
is exactly what we might expect to see from the paper.

In other cases, the telescopes have just picked up a galaxy in the
general direction of the GRB.  I am guessing if you look deep enough
you will generally find something close enough.  Indeed, the further
you look the more likely you are to find a good match, so source
galaxies would be biassed to distant ones.

Near galaxies would presumably block these rays, if it wasn't for
gravitational lensing.

I've started a new karmapi module, grb.py, working through the paper.
I'll let do a release and let you know if it becomes interesting.

Thanks again for the pointers.

Johnny

(PS)
----

Just occurred that the chance that the emitter is actually in the
direction we see it from is probably vanishingly small given all the
lensing effects, or gravitational fog as you put it.

F.8 in the book is key: earth has moved a lot since the wave set on its way.

Indeed it is that movement, over the Hubble time, that modulates the
signals we see from each direction.

And yet, our movement is driven by the same gravitational fields, so I
still feel there might be some correlation to find between GRB and
CMB.

I'm starting to think about simulating some of this, but it is a slow
process, figuring out just what to simulate.

I can't get over the simplicity of the model you present, together
with how quickly it becomes complex.
 
Johnny

(Draft)
-------

This is intriguing::

   https://en.wikipedia.org/wiki/Cosmic_background_radiation#/media/File:Cobe-cosmic-background-radiation.gif

   Temperature of the cosmic background radiation spectrum as
   determined with the COBE satellite: uncorrected (top), corrected
   for the dipole term due to our peculiar velocity (middle), and
   corrected for contributions from the dipole term and from our
   galaxy (bottom).


This one too::

   https://lambda.gsfc.nasa.gov/product/cobe/cobe_images/m_d_53s_1111.gif

The raw uncorrected image of the galactic microwave background is beautiful.

This might help locate its centre ;)

I'm curious about the exact nature of the corrections performed here.
Another rabbit hole.

One other thought is if a correction is made (and whether one is
needed?) for the Oort cloud?

Johnny

Colin
-----

Hi

One or two comments::

  Got it.  No emitter actually has to make it into our visible universe,
  just a beam of light from that emitter.

Not quite right.  All we ever see of anything is light.  Sending light
to us is the same as being in our universe::

  If we just go with the assumptions

  1. that the universe is pretty uniform round our way

We only see a tiny patch of the universe, so of course it seems pretty
uniform.  Just like a patch on the earth's surface is roughly a plane::

  2. our visible universe is just a window on a wider universe
     
Yes, yes.::

  3. Our part appears to be expansive

It's both expanding AND contracting.  That's the whole point of the de
Sitter space model.  It's just different coords on the same manifold.
Think of it like one of those Escher patterns that do two opposite
things at the same time.::

  Then these optical illusions should be a pretty regular occurrence.

The GRBs are part of the contractive flow and the usual observations are
the expansive flow (the "Hubble flow").  Look at the RHS of figure 4 in
our Pal J paper::

   http://msp.warwick.ac.uk/~cpr/paradigm/GammaRayBursts.pdf

You see a source arriving as part of the contractive flow (blue shifted)
and then moving over to the expansive flow (red shifted).  The big deal
is this: the blue shift part occupies a small part of the time we see
the source whilst the red shift part is seen for an infinite time.
That's why we think the whole thing is expanding.  Nearly every source
is part of the expansive flow.  The two flows are in exact balance but
it SEEMS that nearly all is expanding.  It an observer selection
phenomenon.

The GRBs are a very regular occurrence.  The light from every galaxy we
see started out as a GRB and then settled down to be a well-behaved red
shifted galaxy in the Hubble flow.::

  In other cases, the telescopes have just picked up a galaxy in the
  general direction of the GRB.  I am guessing if you look deep enough
  you will generally find something close enough.  Indeed, the further
  you look the more likely you are to find a good match, so source
  galaxies would be biassed to distant ones.

That's pretty much correct,::

  Near galaxies would presumably block these rays, if it wasn't for
  gravitational lensing.

Not true.  They are so intense they soar through the obstruction.
Lensing has nothing to do with it.  It's not a lensing phenomenon.  It's
the way null geodesics work when a source comes over the horizon into
the visible universe.::

  Just occurred that the chance that the emitter is actually in the
  direction we see it from is probably vanishingly small given all the
  lensing effects, or gravitational fog as you put it.

No.  The emitter is in the direction we see it.  The fog just delays the
appearance a tiny bit and cuts the received energy down from infinite
(OUCH) to finite.::

  F.8 in the book is key: earth has moved a lot since the wave set on
  its way.  Indeed it is that movement, over the Hubble time, that
  modulates the signals we see from each direction.

Don't understand that.  The motion of the earth is very slow compared to
the speed of light at which GRBs propagate.::

  I can't get over the simplicity of the model you present, together
  with how quickly it becomes complex.

Thanks.

Colin

Johnny
------

**Got it** *No emitter actually has to make it into our visible universe, just a
beam of light from that emitter.*

::
   Not quite right.  All we ever see of anything is light.  Sending light
   to us is the same as being in our universe

That is very helpful.

So a galaxy enters the visible universe, so does it's giant rotating
mass, and a stored up history that we perhaps should see as a gravitational wave.

I did a quick hunt, there have been attempts to look for gravitational
waves, although the papers date back to 2010 or previous.

I would expect to see a *twist* in the direction of rotation of the
galaxy (assume distribution of orientations is random?), roughly following the
intensity curve of the GRB.

This will drop of in strength linearly with distance, so it is not
clear we would detect it with current detectors.

In 2014 it was deemed to be two black holes, roughly 30 solar masses
colliding a billion years ago.

So a galaxy of 10^9 solar masses just 10 times the distance away ought
to make an impression?

Unless our universe already has accounted for its motion which is in
harmony with its surroundings, as are we, modulo the cosmic microwave
background.

Moving on.  **Our part appears to be expansive**::

   It's both expanding AND contracting.  That's the whole point of the de
   Sitter space model.  It's just different coords on the same manifold.
   Think of it like one of those Escher patterns that do two opposite
   things at the same time.::

And there is an isometry between the two sets of coordinates, that
respects causality, courtesy of the Minkowski metric?

I like the escher analogy.

Then these optical illusions should be a pretty regular occurrence.::

   The GRBs are part of the contractive flow and the usual observations are
   the expansive flow (the "Hubble flow").  Look at the RHS of figure 4 in
   our Pal J paper::

      http://msp.warwick.ac.uk/~cpr/paradigm/GammaRayBursts.pdf

   You see a source arriving as part of the contractive flow (blue shifted)
   and then moving over to the expansive flow (red shifted).

   The big dealis this::

     the blue shift part occupies a small part of the time we see the
     source whilst the red shift part is seen for an infinite time.

     That's why we think the whole thing is expanding.

     Nearly every source is part of the expansive flow.

     The two flows are in exact balance but it SEEMS that nearly all
     is expanding.

     It an observer selection phenomenon.


Thanks.  This clears up much.

Everything that is in the visible universe is in the expansive part
for all but a vanishingly small part of its life.

Arrive with a gamma flash.  Live and slowly fade away.

Arrival and departure rates in balance.

Now, back to how often do we see these GRB's::
   
   The GRBs are a very regular occurrence.  The light from every galaxy we
   see started out as a GRB and then settled down to be a well-behaved red
   shifted galaxy in the Hubble flow.

I read somewhere about one a day was being detected, with networks of
satellites to help with triangulation.

So 500 billion galaxies, 12 billion year journey, one a day arrival
feels about right.
   

Returning to: **Near galaxies would presumably block these rays, if it
wasn't for gravitational lensing.**::

   Not true.  They are so intense they soar through the obstruction.
   Lensing has nothing to do with it.  It's not a lensing phenomenon.  It's
   the way null geodesics work when a source comes over the horizon into
   the visible universe.::

And: **Just occurred that the chance that the emitter is actually in
the direction we see it from is probably vanishingly small given all
the lensing effects, or gravitational fog as you put it.**::

   No.  The emitter is in the direction we see it.  The fog just delays the
   appearance a tiny bit and cuts the received energy down from infinite
   (OUCH) to finite.::

And finally, **F.8 in the book is key: earth has moved a lot since the
wave set on its way.  Indeed it is that movement, over the Hubble
time, that modulates the signals we see from each direction.**::

   Don't understand that.  The motion of the earth is very slow compared to
   the speed of light at which GRBs propagate.

Here I was talking about the actual shape of the burst being modulated
by the relative movement of emitter and receiver sincd time -t.

**I can't get over the simplicity of the model you present, together
with how quickly it becomes complex.**

Thanks.

Johnny

Recap
=====

If we just go with the assumptions 

1. that the universe is pretty uniform round our way 

2. our visible universe is just a window on a wider universe
   and maybe:

3. Our part appears to be expansive

Then these optical illusions should be a pretty regular occurrence.

Regarding 3., our universe is both expansive and contractive.

However, we get to observe the expansive part for almost all of an
emitter's life.

All we ever see of anything is light.  Sending light to us is the same
as being in our universe.

Gravitational waves propogate in the same manner as light.


de sitter geodesic isometry

both causality preserving.
 
  
Mixing of inertial fields
=========================


Random?
=======


Synchronisation
===============


Pseudo Harmonic
===============

Solar System
============

Earth
=====

El Nino
-------
