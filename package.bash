  #!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

rm -f send2google_earth.zip

mkdir -p send2google_earth
cp *.py send2google_earth/
cp README.md send2google_earth/
cp metadata.txt send2google_earth/
cp -R icons/ send2google_earth/icons/
zip -r send2google_earth.zip send2google_earth
rm -rf send2google_earth