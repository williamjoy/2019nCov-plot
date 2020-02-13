fetch-data:
	http https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/csv/DXYArea.csv --output DXYArea.csv

plots: others provinces

others:
	python3 main.py  --exclude 湖北 --save-file 'China-Exlcuding-Hubei'
	python3 main.py  --exclude 武汉 --save-file 'Hubei-Exlcuding-Wuhan'
	python3 main.py  --save-file 'China'
provinces:
	tail -n +2 DXYArea.csv|cut -d, -f 1|sort -u |xargs -n1 -I '{}' python3 main.py --province '{}' --save-file 'output/{}'
