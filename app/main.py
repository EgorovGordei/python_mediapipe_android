import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
import time
import os

from plyer import gps
from plyer import camera
import requests

from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.clock import Clock
import numpy as np
import cv2


import imutils
import mediapipe as mp


mainkv = """
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        id: button_change_image_state
        text: 'Image state: 0'
        size_hint_y: None
        height: '48dp'
        on_press: root.change_image_state()
    MDTextField:
        id: input_colors
        hint_text: "Input colors"
        text: "80, 100, 220; 120, 255, 255"
        mode: "fill"
        fill_color: 0, 0, 0, .4
    Image:
        id: image
"""

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

class CameraClick(BoxLayout):
    image_state = 0
    clock_is_ticking = False

    def clock_tick(self, dt):
        self.capture()

    def capture(self):
        global mpDraw, mpPose, pose, mpFaceMesh, faceMesh, drawSpec
        if not self.clock_is_ticking:
            self.clock_is_ticking = True
            Clock.schedule_interval(self.clock_tick, 1.0 / 25)
        
        camera = self.ids['camera']
        camtexture = camera.texture

        height, width = camtexture.height, camtexture.width
        frame = np.frombuffer(camtexture.pixels, np.uint8)
        frame = frame.reshape(height, width, 4)



        imgRGB = frame
        if camera.texture.colorfmt == 'bgr':
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if camera.texture.colorfmt == 'rgba':
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        if camera.texture.colorfmt == 'bgra':
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        frame = imgRGB

        ###"""
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        results = faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACE_CONNECTIONS,
                                      drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                ih, iw, ic = frame.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
        ###"""
                

            
        buf = cv2.flip(frame, -1)
        buf = buf.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]))
        try:
            if self.image_state % 7 == 0:
                texture.blit_buffer(buf, colorfmt='rgb')
            if self.image_state % 7 == 1:
                texture.blit_buffer(buf, colorfmt='rgba')
            if self.image_state % 7 == 2:
                texture.blit_buffer(buf, colorfmt='bgra')
            if self.image_state % 7 == 3:
                texture.blit_buffer(buf, colorfmt='rgb')
            if self.image_state % 7 == 4:
                texture.blit_buffer(buf, colorfmt='bgr')
            if self.image_state % 7 == 5:
                texture.blit_buffer(buf, colorfmt=camtexture.colorfmt)
            if self.image_state % 7 == 6:
                texture = camtexture
            self.ids['image'].texture = texture
        except:
            pass

    def change_image_state(self):
        self.image_state += 1
        self.ids["button_change_image_state"].text = 'Image state:' +\
                                                    str(self.image_state % 7)


class TestCamera(MDApp):
    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA,
                                 Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.READ_EXTERNAL_STORAGE])
        Builder.load_string(mainkv)
        return CameraClick()


TestCamera().run()
