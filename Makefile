.PHONY: install check build test clean

install:
	python3 -m pip install .

check:
	python3 -m pelican content -s pelicanconf.py -o /tmp/portfolio-pelican-check -t theme --fatal warnings

build:
	python3 -m pelican content -s publishconf.py -o ../pelican-output -t theme

test:
	python3 -m unittest discover -s tests -v

clean:
	python3 -c "import shutil; shutil.rmtree('output', ignore_errors=True)"
