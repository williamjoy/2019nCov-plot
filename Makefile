fetch-data:
	#http https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/csv/DXYArea.csv --output DXYArea.csv
	http https://health-infobase.canada.ca/src/data/covidLive/covid19.csv --output canada.csv

plots: others provinces

others:
	#python3 main.py  --exclude 湖北 --save-file 'output/China-Excluding-Hubei'
	#python3 main.py  --exclude 武汉 --province 湖北 --save-file 'output/Hubei-Excluding-Wuhan'
	#python3 main.py  --save-file 'output/China'
	python3 canada.py  --save-file 'output/Canada_Confirmed_Cases' --title 'Canada Confirmed Cases'
	python3 canada.py  --save-file 'output/Canada_Daily_New_Cases' --value-column numtoday --title 'Canada Daily New Cases'
	python3 canada.py  --save-file 'output/Canada_Tested_Cases' --value-column numtested --title 'Canada Tested Cases'
provinces:
	tail -n +2 DXYArea.csv|cut -d, -f 1|sort -u |xargs -n1 -I '{}' python3 main.py --province '{}' --save-file 'output/{}'

update-index:
	tree -H 'output' -L 1 --noreport --charset utf-8  ./output/ > outputs.html

all: fetch-data others update-index

open-github-page:
	open https://williamjoy.github.io/2019nCov-plot/output/Canada.svg
