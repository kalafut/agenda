class Source:
    def __init__(self):
        self.obs = set()

    def attach(self, obs):
        self.obs.add(obs)

    def notify(self):
        for o in self.obs:
            o.update()

class Item(Source):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text
        self.notify()


class Section:
    def __init__(self, items=None):
        self.items = items or []

class View:
    def __init__(self, sections=None):
        self.sections = sections or []

i1 = Item('My first line')
sample_section1 = Section([
    i1,
    Item('My second line'),
    Item('My third line')
   ])

sample_section2 = Section([
    Item('Let It Go'),
    Item('A Hard Day\'s Night'),
    Item('Bouncing Around the Room'),
    i1
   ])

sample_view = View([sample_section1, sample_section2])
