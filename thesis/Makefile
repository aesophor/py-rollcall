MAIN_FILE = thesis
BUILD_DIR = build

.PHONY = pdf clean

pdf:
	mkdir -p $(BUILD_DIR)
	cd src && pdflatex -output-directory ../$(BUILD_DIR) $(MAIN_FILE).tex

open:
	xdg-open build/$(MAIN_FILE).pdf

clean:
	rm -rf $(BUILD_DIR)
	rm -f src/figures/*.pdf
