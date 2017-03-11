import urwid
from model import *

class ItemCat(urwid.Text):
    def __init__(self, item, *args, **kwargs):
        super().__init__('')
        self.item = item
        self.item.attach(self)
        self.update()

    def update(self):
        self.set_text(','.join(self.item.categories))

class ProxyEdit(urwid.Edit):
    def __init__(self, source, *args, **kwargs):
        super().__init__('', source.get_text())
        self.source = source
        self.source.attach(self)
        self._in_update = False

        urwid.connect_signal(self, 'change', self.change)

    def change(self, widget, new_text):
        if not self._in_update:
            self.source.set_text(new_text)

    def update(self):
        self._in_update = True
        self.set_edit_text(self.source.get_text())
        self._in_update = False


class SectionPile(urwid.Pile):
    def __init__(self, section):
        self.section = section
        section.attach(self)
        super().__init__(self.calc_rows())

    def calc_rows(self):
        rows = []
        for item in self.section.items:
            e = ProxyEdit(item)
            if self.section.show_cats:
                c = urwid.Columns([e, ItemCat(item)])
            else:
                c = urwid.Columns([e])
            rows.append(c)

        return rows

    def update(self):
        self.contents = [(x,('pack', None)) for x in self.calc_rows()]


class ViewList(urwid.SimpleFocusListWalker):
    def __init__(self, view: View) -> None:
        #for section in view.sections:
        #    section.attach(self)

        self.view = view
        rows = self.draw_view(view)
        super().__init__(rows)

    def draw_view(self, view):
        rows = []
        for section in view.sections:
            rows.append(self.draw_section(section))
            rows.append(urwid.Text(''))
        return rows

    def draw_section(self, section):
        return SectionPile(section)

    def update(self):
        self[:] = self.draw_view(self.view)


class ViewListBox(urwid.ListBox):
    def __init__(self, view):
        body = ViewList(view)
        super().__init__(body)

palette = [('I say', 'default,bold', 'default'),
        ('bg', 'white', 'dark blue')]
#main = urwid.Padding(ConversationListBox(), left=2, right=2)
#main3 = urwid.AttrMap(main, 'bg')
#top = urwid.Overlay(main3, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
#    align='center', width=('relative', 60),
#    valign='middle', height=('relative', 60),
#    min_width=20, min_height=9)

#class T1(urwid.ListBox):
#    def __init__(self):
#        body = urwid.0
urwid.MainLoop(ViewListBox(sample_view), palette).run()
