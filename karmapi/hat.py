
import random
import datetime
import sense_hat
import time

class HatInfo:

    def __init__(self):

        self.hat = sense_hat.SenseHat()
        self.stick = sense_hat.SenseStick()
        
        self.hat.rotation = 90

        self.colour = (220, 100, 100)

        self.stats = False

    def whattimeisit(self):

        return f'{datetime.datetime.now():%H:%M}'

    def run(self):

        h = self.hat
        while True:

            if self.stats:
            
                messages = [
                    f'T: {h.temp:0.1f}',
                    f'P: {h.pressure:0.1f}',
                    f'H: {h.humidity:0.1f}',
                    f'TT: {self.whattimeisit()}']        

                colours = [
                    [255, 255, 0],
                    [255, 0, 255],
                    [0, 255, 255],
                    [255, 255, 255],
                ]
                     

                for message, colour in zip(messages, colours):
                    
                    h.show_message(message, text_colour=colour,
                                   scroll_speed=0.2)

            else:
                self.hat.set_pixels([self.colour] * 64)
                
                time.sleep(2)
                continue

if __name__ == '__main__':

    h = HatInfo()

    h.run()
