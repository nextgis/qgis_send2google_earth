mkdir send2google_earth
xcopy *.py send2google_earth
xcopy README.md send2google_earth
xcopy metadata.txt send2google_earth
zip -r send2google_earth.zip send2google_earth
del /Q send2google_earth
rd send2google_earth