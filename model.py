class Source:
    def __init__(self):
        self.obs = []

    def attach(self, obs):
        if obs not in self.obs:
            self.obs.append(obs)

    def notify(self):
        for o in self.obs:
            o.update()

class Item(Source):
    def __init__(self, text, categories: set=None):
        super().__init__()
        self.text = text
        self.categories = categories or set()
        self.process()

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text
        self.process()
        self.notify()

    def process(self):
        if 'line' in self.text:
            self.categories.add('line')
        else:
            self.categories.discard('line')


class Section(Source):
    def __init__(self, item_db, top_cat=None, show_cats=False):
        super().__init__()
        for item in item_db:
            item.attach(self)
        self.item_db = item_db
        self.top_cat = top_cat
        self.show_cats = show_cats
        self.proc()

    def proc(self):
        if self.top_cat:
            self.items = [x for x in self.item_db if self.top_cat in x.categories]
        else:
            self.items = self.item_db
        self.notify()

    def update(self):
        self.proc()

class View:
    def __init__(self, sections=None):
        self.sections = sections or []


items = set([
    Item('My first line'),
    Item('My second line', categories=set(['seconds'])),
    Item('My third line'),
    Item('Let It Go'),
    Item('A Hard Day\'s Night', categories=set(['hard'])),
    Item('Bouncing Around the Room')
    ])


sample_section1 = Section(items, show_cats=True)
sample_section2 = Section(items, top_cat='line', show_cats=True)

sample_view = View([sample_section1, sample_section2])
