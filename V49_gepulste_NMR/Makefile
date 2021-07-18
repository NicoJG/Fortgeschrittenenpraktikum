all: build/main.pdf

# hier alle zu erstellenden Plots
plots: build/plot_T1.pdf build/plot_Diff3.pdf build/plot_echo_Gradient.pdf build/plot_mgoff.pdf

# für jeden zu erstellenden Plot:
build/plot_T1.pdf: python/plot1.py data/*.csv | build
	python python/plot1.py

build/plot_Diff3.pdf: python/plot2.py data/*.csv | build
	python python/plot2.py

build/plot_echo_Gradient.pdf: python/plot3.py data/*.csv | build
	python python/plot3.py

build/plot_mgoff.pdf: python/plot4.py data/*.csv | build
	python python/plot4.py

	
build/main.pdf: plots

build/main.pdf: FORCE | build
	  TEXINPUTS=build: \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --lualatex \
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
