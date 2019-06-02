@echo off
call pyuic5 GUI.ui -o GUI.py
call pyuic5 AddCamera.ui -o AddCamera.py
call pyuic5 Cameras.ui -o Cameras.py
call pyuic5 Fonts.ui -o Fonts.py
call pyuic5 UpdateCamera.ui -o UpdateCamera.py
call pyuic5 AddFont.ui -o AddFont.py
call pyuic5 Char.ui -o Char.py