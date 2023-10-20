mkdir send2google_earth
mkdir send2google_earth\icons
mkdir send2google_earth\i18n
xcopy icons\ send2google_earth\icons
xcopy *.py send2google_earth
xcopy *.ui send2google_earth
xcopy README.md send2google_earth
xcopy metadata.txt send2google_earth
xcopy i18n\send2google_earth_ru.ts send2google_earth\i18n\send2google_earth_ru.ts
lrelease send2google_earth\i18n\send2google_earth_ru.ts
del send2google_earth\i18n\send2google_earth_ru.ts
zip -r send2google_earth.zip send2google_earth
del /s /Q send2google_earth
rd /s /q send2google_earth