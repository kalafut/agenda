import urwid
from model import *


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


class SectionList(urwid.SimpleFocusListWalker):
    def __init__(self, section: Section):
        rows = []
        for item in section.items:
            e = ProxyEdit(item)
            e2 = ProxyEdit(item)
            c = urwid.Columns([e, e2, urwid.Text("This is great!")])
            rows.append(c)

        super().__init__(rows)
        #urwid.connect_signal(self, 'modified', self.save)

    def save(self, widget=None, new_text=None):
        raise Exception(widget)
        #print(widget, new_text)
        return
        with open('test.txt', 'w') as f:
            if widget and new_text:
                f.writelines(f'{new_text}\n' if x is widget else f'{x.edit_text}\n' for x in self)
            else:
                f.writelines(f'{x.edit_text}\n' for x in self)

    def move_up(self):
        focus = self.focus

        if self.focus > 0:
            self[focus], self[focus-1] = self[focus-1], self[focus]
            self.focus -= 1

    def move_down(self):
        focus = self.focus

        if self.focus < len(self) - 1:
            self[focus], self[focus+1] = self[focus+1], self[focus]
            self.focus += 1


class SectionListBox(urwid.ListBox):
    def __init__(self, section):
        body = SectionList(section)
        super().__init__(body)

    def keypress(self, size, key):
        key = super().keypress(size, key)

        if key == 'shift down':
            self.body.move_down()
            return
        elif key == 'shift up':
            self.body.move_up()
            return
        elif key == 'f4':
            del self.body[self.focus_position]
        elif key != 'enter':
            return key

        name = self.focus.edit_text
        if not name:
            raise urwid.ExitMainLoop()

        if self.focus_position == len(self.body) - 1:
            self.body.append(urwid.Edit())
            self.focus_position += 1

class ViewList(urwid.SimpleFocusListWalker):
    def __init__(self, view: View):
        rows = []
        for section in view.sections:
            for item in section.items:
                e = ProxyEdit(item)
                e2 = ProxyEdit(item)
                c = urwid.Columns([e, e2, urwid.Text("This is great!")])
                rows.append(c)
            rows.append(urwid.Text(''))

        super().__init__(rows)

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
urwid.MainLoop(ViewListBox(sample_view), palette).run()
