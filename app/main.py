#import mediapipe

import kivy
from kivy.app import App
from kivy.uix.label import Label


class ButtonApp(App):
    def build(self):
        self.label = Label(text="It's alive!")
        return self.label

    
root = ButtonApp()
root.run()
