@echo off
setlocal enabledelayedexpansion
set b=z1
for /L %%a in (1 4999 148092) do (
 cd input
 del /q *
 cd ..
 for /L %%b in (0 1 4999) do (
  set /a c=%%a+%%b
  copy input_temp\"!c!".mp4 input
 )
 PIX2NVS R 1 N 2 F 0.3 C 1
)