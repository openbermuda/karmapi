#!/usr/bin/env python

"""M CLOCK 2.0."""
import sys
from karmapi import pig
import math
import time
import curio

class GuidoClock(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        radius=200
        segments=9
        
        self.segments = segments

        self.canvas.configure(bg='black', width=2*radius, height=2*radius)

        
        self.canvas.bind("<Configure>", self.on_configure)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        if sys.platform == "win32":
            self.canvas.bind("<3>", self.on_zoom)
            self.credits += "\n(right button toggles full screen mode)"
        self.recalc(radius*2, radius*2)

    def on_configure(self, event):
        self.recalc(event.width, event.height)

    credits = ("M Clock 2.0\n"
               "by Guido van Rossum\n"
               "after a design by Rob Juda")

    creditid = None
    showtext = False

    def on_press(self, event):
        self.creditid = self.canvas.create_text(
            self.canvas.canvasx(event.x),
            self.canvas.canvasy(event.y),
            anchor="s", text=self.credits,
            font="Helvetica 16 bold", justify="center")
        self.showtext = not self.showtext

    def on_motion(self, event):
        creditid = self.creditid
        if creditid:
            oldx, oldy = self.canvas.coords(creditid)
            self.canvas.move(creditid,
                             self.canvas.canvasx(event.x) - oldx,
                             self.canvas.canvasy(event.y) - oldy)

    def on_release(self, event):
        creditid = self.creditid
        if creditid:
            self.creditid = None
            self.canvas.delete(creditid)

    def on_zoom(self, event):
        if self.root.wm_overrideredirect():
            self.root.wm_overrideredirect(False)
            self.root.wm_state("normal")
            self.root.wm_geometry("400x400")
        else:
            self.root.wm_overrideredirect(True)
            self.root.wm_state("zoomed")

    def recalc(self, width, height):
        radius = min(width, height) // 2
        self.width = width
        self.height = height
        self.radius = radius
        self.bigsize = radius * .975
        self.litsize = radius * .67
        self.canvas.configure(scrollregion=(-width//2, -height//2,
                                            width//2, height//2))

    def demo(self, speed=1, colors=(0, 1, 2), segments=None):
        if segments is not None:
            self.segments = segments
        if self.creditid:
            text = "N=%s\nv=%s\n%s" % (self.segments, speed, list(colors))
            self.canvas.itemconfigure(self.creditid, text=text)
        hh, mm, ss = time.localtime()[3:6]
        self.showtext = False
        while not self.showtext:
            try:
                self.draw(hh, mm, ss, colors)
            except Tkinter.TclError:
                break
            self.root.update()
            ss += speed
            mm, ss = divmod(mm*60 + ss, 60)
            hh, mm = divmod(hh*60 + mm, 60)
            hh %= 24

    async def run(self):

        while True:
            self.redraw()
            await curio.sleep(10)

            
    def redraw(self):
        t = time.time()
        hh, mm, ss = time.localtime(t)[3:6]
        self.draw(hh, mm, ss)

    ids = ()

    def draw(self, hh, mm, ss, colors=(0, 1, 2)):
        radius = self.radius
        bigsize = self.bigsize
        litsize = self.litsize
        # Delete old items
        if self.ids:
            self.canvas.delete(*self.ids)
        self.ids = []
        # Set bigd, litd to angles in degrees for big, little hands
        # 12 => 90, 3 => 0, etc.
        bigd = (90 - (mm*60 + ss) / 10) % 360
        litd = (90 - (hh*3600 + mm*60 + ss) / 120) % 360
        # Set bigr, litr to the same values in radians
        bigr = math.radians(bigd)
        litr = math.radians(litd)
        # Draw the background colored arcs
        self.drawbg(bigd, litd, colors)
        # Draw the hands
        b = self.canvas.create_line(0, 0,
                                    bigsize*math.cos(bigr),
                                    -bigsize*math.sin(bigr),
                                    width=radius/50, capstyle="round")
        l = self.canvas.create_line(0, 0,
                                    litsize*math.cos(litr),
                                    -litsize*math.sin(litr),
                                    width=radius/33, capstyle="round")
        self.ids.append(b)
        self.ids.append(l)
        # Draw the text
        if self.showtext:
            t = self.canvas.create_text(-bigsize, bigsize,
                                        text="%02d:%02d:%02d" % (hh, mm, ss),
                                        fill="white", anchor="sw",
                                        font="helvetica 16 bold")
            self.ids.append(t)
        if self.creditid:
            self.canvas.tag_raise(self.creditid)

    def drawbg(self, bigd, litd, colors=(0, 1, 2)):
        # This is tricky.  We have to simulate a white background with
        # three transparent discs in front of it; one disc is
        # stationary and the other two are attached to the big and
        # little hands, respectively.  Each disc has 9 pie segments in
        # sucessive shades of pigment applied to it, ranging from
        # fully transparent to only allowing one of the three colors
        # Cyan, Magenta, Yellow through.
        N = self.segments
        table = []
        for angle, colorindex in [(bigd - 180/N, 0),
                                  (litd - 180/N, 1),
                                  (  90 - 180/N, 2)]:
            angle %= 360
            for i in range(N):
                color = 255
                if colorindex in colors:
                    color = (N-1-i)*color//(N-1)
                table.append((angle, color, colorindex))
                angle += 360/N
                if angle >= 360:
                    angle -= 360
                    table.append((0, color, colorindex))
        table.sort()
        table.append((360, None))
        radius = self.radius
        fill = [0, 0, 0]
        for i, (angle, color, colorindex) in enumerate(table[:-1]):
            fill[colorindex] = color
            if table[i+1][0] > angle:
                extent = table[i+1][0] - angle
                if extent < 1.:
                    # XXX Work around a bug in Tk for very small angles
                    extent = 1.
                id = self.canvas.create_arc(-radius, -radius, radius, radius,
                                           fill="#%02x%02x%02x" % tuple(fill),
                                           outline="",
                                           start=angle,
                                           extent=extent)
                self.ids.append(id)

