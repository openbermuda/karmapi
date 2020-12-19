
import random
import datetime
import sense_hat


class HatInfo:

    def __init__(self):

        self.hat = sense_hat.SenseHat()
        self.stick = sense_hat.SenseStick()
        
        self.hat.rotation = 90

    def whattimeisit(self):

        return f'{datetime.datetime.now():%H:%M}'

    def run(self):

        h = self.hat
        while True:

            messages = [
                f'T: {h.temp:0.1f}',
                f'P: {h.pressure:0.1f}',
                f'H: {h.humidity:0.1f}',
                f'TT: {self.whattimeisit()}']        


            for message, colour in zip(messages, colours):
                
                h.show_message(message, text_colour=colour,
                               scroll_speed=0.2)


if __name__ == '__main__':

    h = HatInfo()

    h.run()
