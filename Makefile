.PHONY: srpm spec-check clean

srpm:
	$(MAKE) -f .copr/Makefile srpm outdir="$(CURDIR)/dist"

spec-check:
	rpmspec -P t3code.spec >/dev/null
	desktop-file-validate t3code.desktop

clean:
	rm -rf dist
