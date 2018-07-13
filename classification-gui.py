from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class EmailClassification(GridLayout):
    def __init__(self,*args):
        super(EmailClassification,self).__init__(*args)
        self.cols = 3
        '''
        self.add_widget(Label(text = "SRC_DIR"))
        self.src_dir = TextInput(multiline = False)
        self.add_widget(self.src_dir)
        
        self.add_widget(Label(text='DST_DIR'))
        self.dst_dir = TextInput(multiline = False)
        self.add_widget(self.dst_dir)

        self.add_widget(Label(text='EXCEL_LOC'))
        self.excel_loc = TextInput(multiline = False)
        self.add_widget(self.excel_loc)
        '''


    pass

class EmailClassificationApp(App):
    def build(self):
        return EmailClassification()

if __name__=='__main__':
    EmailClassificationApp().run()