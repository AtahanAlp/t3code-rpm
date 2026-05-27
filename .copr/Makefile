SPEC := t3code.spec

.PHONY: srpm
srpm:
	set -eu; \
	outdir="$${outdir:-$$(pwd)/dist}"; \
	version="$$(rpmspec -q --qf '%{VERSION}\n' "$(SPEC)" | head -n 1)"; \
	asset="T3-Code-$${version}-x86_64.AppImage"; \
	workdir="$$(mktemp -d)"; \
	trap 'rm -rf "$$workdir"' EXIT; \
	mkdir -p "$$outdir" "$$workdir/SOURCES" "$$workdir/SPECS"; \
	cp "$(SPEC)" "$$workdir/SPECS/"; \
	cp t3code.desktop "$$workdir/SOURCES/"; \
	cp LICENSE.upstream "$$workdir/SOURCES/"; \
	cp "sources/$${asset}.sha512" "$$workdir/SOURCES/"; \
	rpmbuild -bs \
		--target x86_64 \
		--define "_topdir $$workdir" \
		--define "_sourcedir $$workdir/SOURCES" \
		--define "_srcrpmdir $$outdir" \
		"$$workdir/SPECS/$(SPEC)"
