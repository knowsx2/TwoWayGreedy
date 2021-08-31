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


def print_node_on_frame(node, frame, pos=None):
    pos = [0, 0] if pos is None else pos
    st = wx.StaticText(frame.pnl, pos=pos, size=wx.Size(30, 30), label=str(node), style=wx.ALIGN_RIGHT)
    font = st.GetFont()
    st.SetFont(font)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
    frame.pnl.SetSizer(sizer)
    return pos, wx.Size(30,30)