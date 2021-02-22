@echo off
title Davka pro overeni nocnich prekladu  
echo.

cd C:\Helios\Repository\kontrolaNocnichPrekladu\
run.py

echo automaticke pozdrzeni davky na 2 sec 
choice /C A /D A /T 30 > nul
