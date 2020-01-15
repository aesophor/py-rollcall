MAINFILE = pyrollcall.tex
BUILD_DIR = build

.PHONY = pdf clean

pdf:
	mkdir -p $(BUILD_DIR)
	cd src && pdflatex -output-directory ../$(BUILD_DIR) $(MAINFILE)

clean:
	rm -rf $(BUILD_DIR)
	rm -f src/*.pdf
