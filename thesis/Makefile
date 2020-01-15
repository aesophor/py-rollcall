MAINFILE = thesis.tex
BUILD_DIR = build

.PHONY = pdf clean

pdf:
	mkdir -p $(BUILD_DIR)
	cd src && pdflatex -output-directory ../$(BUILD_DIR) $(MAINFILE)

open:
	xdg-open build/thesis.pdf

clean:
	rm -rf $(BUILD_DIR)
	rm -f src/figures/*.pdf
