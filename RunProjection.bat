::@ECHO OFF

rem You can copy the data directory to your own location and modify the scenarios
rem and inputs to your own situation. Then come back here and change the DATADIR
rem environment variable to point to the path for your data, such as:
rem     set "DATADIR=C:\Users\myuser\Documents\Farm-Projection-Data"
rem You may also change the scenario to be a specific one instead of all if desired,
rem and/or set the max acres to your known acreage. Zero disables the acreage limit.

set "FARMPROJECTION_ROOT=%cd%"
set SCENARIO=all
set MAXACRES=0
set "DATADIR=%FARMPROJECTION_ROOT%\data"

python.exe %FARMPROJECTION_ROOT%\bin\RunProjection.py %SCENARIO% --maxacres %MAXACRES% --datadir "%DATADIR%"
