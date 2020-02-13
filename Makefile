fetch-data:
	http https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/csv/DXYArea.csv --output DXYArea.csv

plots: others provinces

others:
	python3 main.py  --exclude 湖北 --save-file 'output/China-Excluding-Hubei'
	python3 main.py  --exclude 武汉 --save-file 'output/Hubei-Excluding-Wuhan'
	python3 main.py  --save-file 'output/China'
provinces:
	tail -n +2 DXYArea.csv|cut -d, -f 1|sort -u |xargs -n1 -I '{}' python3 main.py --province '{}' --save-file 'output/{}'

update-index:
	tree -H 'output' -L 1 --noreport --charset utf-8  ./output/ > outputs.html
