::@ECHO OFF

rem You can copy the data directory to your own location and modify the scenarios
rem and inputs to your own situation. Then come back here and change the DATADIR
rem environment variable to point to the path for your data, such as:
rem     set "DATADIR=C:\Users\myuser\Documents\Farm-Projection-Data"
rem You may also change the scenario to be a specific one instead of all if desired.

set "FARMPROJECTION_ROOT=%cd%"
set SCENARIO=all
set "DATADIR=%FARMPROJECTION_ROOT%\data"

python.exe %FARMPROJECTION_ROOT%\bin\RunProjection.py %SCENARIO% "--datadir=%DATADIR%"
