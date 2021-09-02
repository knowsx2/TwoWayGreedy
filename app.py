import wx


class App(wx.App):
    def OnInit(self):
        self.frame = [Frame()]
        # viene mostrata la finestra
        for a in self.frame: a.Show()
        # imposta la finestra principale
        self.SetTopWindow(self.frame[0])
        return 1

    def add_frame(self):
        self.frame.append(Frame())
        self.frame[-1].Show()
        self.SetTopWindow(self.frame[-1])


class Frame(wx.Frame):
    def __init__(self):
        # Chiama il costruttore di wxFrame.
        wx.Frame.__init__(self, None, -1, "Prova")
        self.pnl = wx.Panel(self)


def print_node_on_frame(node, frame):
    st = wx.StaticText(frame.pnl, label=display(node), style=wx.ALIGN_LEFT)
    #sizer = wx.BoxSizer(wx.VERTICAL)
    #sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
    #frame.pnl.SetSizer(sizer)

def display(node):
    lines, *_ = display_aux(node)
    string = ""
    for line in lines:
        string = string + line + '\n'
    return string


def display_aux(node):
    """Returns list of strings, width, height, and horizontal coordinate of the root."""
    # No child.
    if node.yes is None and node.no is None:
        line = '%s' % str(node)
        width = len(line)
        height = 1
        middle = width // 2
        return [line], width, height, middle

    # Only no child.
    if node.yes is None:
        lines, n, p, x = display_aux(node.no)
        s = '%s' % str(node)
        u = len(s)
        first_line = (x + 1) * '  ' + (n - x - 1) * '_' + s
        second_line = x * '  ' + '/' + (n - x - 1 + u) * '  '
        shifted_lines = [line + u * '  ' for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

    # Only yes child.
    if node.no is None:
        lines, n, p, x = display_aux(node.yes)
        s = '%s' % str(node)
        u = len(s)
        first_line = s + x * '_' + (n - x) * '  '
        second_line = (u + x) * '  ' + '\\' + (n - x - 1) * '  '
        shifted_lines = [u * '  ' + line for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

    # Two children.
    no, n, p, x = display_aux(node.no)
    yes, m, q, y = display_aux(node.yes)
    s = '%s' % str(node)
    u = len(s)
    first_line = (x + 1) * '  ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * '  '
    second_line = x * '  ' + '/' + (n - x - 1 + u + y) * '  ' + '\\' + (m - y - 1) * '  '
    if p < q:
        no += [n * ' '] * (q - p)
    elif q < p:
        yes += [m * ' '] * (p - q)
    zipped_lines = zip(no, yes)
    lines = [first_line, second_line] + [a + u * '  ' + b for a, b in zipped_lines]
    return lines, n + m + u, max(p, q) + 2, n + u // 2
