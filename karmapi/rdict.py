""" Random Dictioary """


class rdict(dict):

    def __getitem__(self, item):

        try:
            return super().__item__(item)

        except KeyError as kerror:

            # FIXME: return a random value

            return random.randint(len(vars(self)))
