all: build/main.pdf

# hier alle zu erstellenden Plots
plots: build/plot_detektorscan.pdf build/plot_messung.pdf

# für jeden zu erstellenden Plot:
build/plot_detektorscan.pdf: python/justierung.py | build
	python python/justierung.py

build/plot_messung.pdf: python/messung.py python/justierung.py | build
	python python/messung.py

build/main.pdf: plots

build/main.pdf: FORCE | build
	  TEXINPUTS=build: \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --lualatex \
	  --shell-escape \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	latex/main.tex

build:
	mkdir -p build

clean:
	rm -rf build

FORCE:

.PHONY: all clean plots
