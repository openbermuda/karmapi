
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
        messages = [
            f'Temp: {h.temp:0.1f}',
            f'Pres: {h.pressure:0.1f}',
            f'Humi: {h.humidity:0.1f}',
            f'Time: {self.whattimeisit()}']        

        while True:
            ix = random.randint(0, len(messages)-1)

            h.show_message(messages[ix],
                           scroll_speed=0.2)


if __name__ == '__main__':

    h = HatInfo()

    h.run()
