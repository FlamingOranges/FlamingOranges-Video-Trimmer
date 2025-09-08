import wx
import pyvidplayer2 as p2
from datetime import timedelta
import os
class HelloFrame(wx.Frame):


    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(None, title = "FlamingOranges Video Trimmer", size=(1200, 700))

        # create a panel in the frame
        self.mainpnl = wx.Panel(self)

        self.videoPanel = wx.Panel(self.mainpnl, size=(480, 270))


        self.titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleText = wx.StaticText(self.mainpnl, label="Imported File:  ", style=wx.ALIGN_LEFT)
        titleText.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.location = wx.StaticText(self.mainpnl, label = '')

        # and create a sizer to manage the layout of child widgets
        self.sizer = wx.BoxSizer(wx.VERTICAL)
    
        self.titleSizer.Add(titleText)
        self.titleSizer.Add(self.location)
        self.sizer.Add(self.titleSizer, 0, wx.EXPAND | wx.ALL, 5)  
        self.sizer.Add(self.videoPanel, wx.ALIGN_LEFT)   
        self.mainpnl.SetSizer(self.sizer)


        # make playback controls
        self.makePlaybackControls()
        self.makeTextBoxes()
        self.Layout()
        

        # create a menu bar
        self.makeMenuBar()



    


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        importFile = fileMenu.Append(0, "Import File\tCtrl+A", "Import video file")
        exportFile = fileMenu.Append(1, "Export File\tCtrl+S", "Export trimmed video file")

        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnImport, importFile)
        self.Bind(wx.EVT_MENU, self.exportFile, exportFile)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)

    def makePlaybackControls(self):
        self.sliderSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.playbackTime = wx.StaticText(self.mainpnl, label = "00:00")
        self.vidDuration = wx.StaticText(self.mainpnl, label = "/ 00:00")

        self.slider = wx.Slider(self.mainpnl, value=0, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL, )
        self.sliderSizer.Add(self.playbackTime, wx.ALIGN_LEFT, border=5)
        self.sliderSizer.Add(self.slider, 1, wx.EXPAND)
        self.sliderSizer.Add(self.vidDuration)
        self.sizer.Add(self.sliderSizer, 0, wx.EXPAND | wx.ALL, 5)



        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.buttonSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        endTimeBtn = wx.Button(self.mainpnl, label="Set End Time")
        startStopBtn = wx.Button(self.mainpnl, label="Start/Stop")
        currentTimeBtn = wx.Button(self.mainpnl, label="Set Start Time")

        self.buttonSizer.Add(currentTimeBtn)
        self.buttonSizer.Add(startStopBtn)
        self.buttonSizer.Add(endTimeBtn)
        
        
        
        currentTimeBtn.Bind(wx.EVT_BUTTON, self.currentTime)
        startStopBtn.Bind(wx.EVT_BUTTON, self.startStop)
        endTimeBtn.Bind(wx.EVT_BUTTON, self.currentTime)
        self.slider.Bind(wx.EVT_SLIDER, self.videoSlider)
        self.sizer.Layout()
    
    def makeTextBoxes(self):
        self.startTimeBox = wx.TextCtrl(self.mainpnl)
        self.endTimeBox = wx.TextCtrl(self.mainpnl)
        self.textBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.textBoxSizer.Add(wx.StaticText(self.mainpnl, label="Start Time: ")) 
        self.textBoxSizer.Add(self.startTimeBox, border = 25, flag=wx.RIGHT)
        self.textBoxSizer.Add(wx.StaticText(self.mainpnl, label="End Time: "))
        self.textBoxSizer.Add(self.endTimeBox)

        self.sizer.Add(self.textBoxSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # this one is special so it doesnt go in the main sizer it gets a new one
        self.specialSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.specialSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.specialSizer.Add(wx.StaticText(self.mainpnl, label="Output File Name: "))

        self.fileNameBox = wx.TextCtrl(self.mainpnl, value="output.mp4")
        self.specialSizer.Add(self.fileNameBox)
        self.sizer.Layout()

    def currentTime(self, event):
        if self.vid:
            self.currentTimeSecs = timedelta(seconds = round(self.vid.frame))
            if event.GetEventObject().GetLabel() == "Set Start Time":
                self.startTimeBox.SetValue(str(self.currentTimeSecs))
            elif event.GetEventObject().GetLabel() == "Set End Time":
                self.endTimeBox.SetValue(str(self.currentTimeSecs))
            print(str(self.currentTimeSecs))
        self.Layout()
    

    def startStop(self, event):
        if self.vid:

            if not self.vid.paused:
                self.vid.pause()
                print(self.vid.active)
            elif self.vid.paused:

                self.vid.resume()
    def videoSlider(self, event):
        if self.vid:
            val = self.slider.GetValue()
            frame = int((val / 100) * self.vid.frame_count)
            self.vid.seek_frame(frame)


    def OnImport(self, event):
        self.vid = None
        with wx.FileDialog(self, "Open video file", wildcard="Video files (*.mp4;*.mov;*.avi)|*.mp4;*.mov;*.avi", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
             if fileDialog.ShowModal() == wx.ID_OK:
                self._originalFile = fileDialog.GetPath()
             else:            
                return 

        self.location.SetLabel(self._originalFile)
        self.sizer.Layout()
        self.startVideo()
             
    def exportFile(self, event):
        if self.vid:
            startTime = self.startTimeBox.GetValue()
            endTime = self.endTimeBox.GetValue()
            if startTime == '':
                startTime = '0:00:00'
            if endTime == '':
                endTime = str(timedelta(seconds = round(self.vid.duration)))
            filename = self.fileNameBox.GetValue()
            if filename == '':
                filename = 'output.mp4'
            if filename[-4:] != '.mp4':
                filename = filename + '.mp4'
                print(filename)

            #shorter variable
            s = self._originalFile
            outputPath = s[:s.rfind("\\")] + "\\" + filename
            print(f'ffmpeg -i {self._originalFile} -ss {startTime} -t {endTime} -c:v copy -c:a copy {outputPath}')
            print()
            os.system(f'ffmpeg -i "{self._originalFile}" -ss {startTime} -t {endTime} -c:v copy -c:a copy "{outputPath}"')
            os.startfile(outputPath)
            wx.MessageBox("Exported to " + outputPath)
        else:
            wx.MessageBox("No video loaded")

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def startVideo(self):
        if self.vid: 
            self.vid.stop()
            self.vid = None
        self.vid = p2.VideoWx(self._originalFile)
        
        self.vidDuration.SetLabel("/ " + str(timedelta(seconds = round(self.vid.duration))) + "s")
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.videoPanel.Bind(wx.EVT_PAINT, self.draw)
        self.vid.resize((480, 270))
        self.vid.play()
        self.timer.Start(int(1000 / self.vid.frame_rate))
        

    # Functions copied from pyvidplayer2 tutorial
    def update(self, event):
            if self.vid:
                self.slider.SetValue(int((self.vid.frame / self.vid.frame_count) * 100))
                self.playbackTime.SetLabel(str(timedelta(seconds = round(self.vid.frame))) + "s")
            self.videoPanel.Refresh(eraseBackground=False)
    def draw(self, event):
        if self.vid:
            self.vid.draw(self.videoPanel, (0, 0), False)

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()