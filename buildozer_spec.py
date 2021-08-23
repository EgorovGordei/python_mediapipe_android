f = open("buildozer.spec", 'r')
s = f.read()
f.close()


s = s.replace("#android.api = 27", "android.api = 30")
s = s.replace("log_level = 1", "log_level = 2")
s = s.replace("# android.accept_sdk_license = False", "android.accept_sdk_license = True")
s = s.replace("requirements = python3,kivy", "requirements = python3==3.7.9,hostpython3==3.7.9,kivy==master,mediapipe")
s = s.replace("#p4a.branch = master", "p4a.branch = develop")
s = s.replace("osx.python_version = 3", "osx.python_version = 3.7.9")

#s = s.replace("android.arch = armeabi-v7a", "android.arch = arm64-v8a")
s = s.replace("android.arch = armeabi-v7a", "android.arch = x86_64")
#s = s.replace("#android.add_libs_x86 = libs/android-x86/*.so", "android.add_libs_x86_64 = libs/android-x86-64/*.so")


f = open("buildozer.spec", 'w')
f.write(s)
f.close()
