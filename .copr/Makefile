SPEC := t3code.spec

.PHONY: srpm
srpm:
	set -eu; \
	outdir="$${outdir:-$$(pwd)/dist}"; \
	version="$$(rpmspec -q --qf '%{VERSION}\n' "$(SPEC)" | head -n 1)"; \
	asset="T3-Code-$${version}-x86_64.AppImage"; \
	url="https://github.com/pingdotgg/t3code/releases/download/v$${version}/$${asset}"; \
	cache_dir="$${cache_dir:-$$(pwd)/dist/cache}"; \
	workdir="$$(mktemp -d)"; \
	trap 'rm -rf "$$workdir"' EXIT; \
	mkdir -p "$$outdir" "$$cache_dir" "$$workdir/SOURCES" "$$workdir/SPECS"; \
	cp "$(SPEC)" "$$workdir/SPECS/"; \
	cp t3code.desktop "$$workdir/SOURCES/"; \
	cp LICENSE.upstream "$$workdir/SOURCES/"; \
	cp "sources/$${asset}.sha512" "$$workdir/SOURCES/"; \
	if [ -f "$$cache_dir/$${asset}" ]; then \
		cp "$$cache_dir/$${asset}" "$$workdir/SOURCES/$${asset}"; \
	else \
		curl -L --fail --show-error --output "$$workdir/SOURCES/$${asset}" "$$url"; \
		cp "$$workdir/SOURCES/$${asset}" "$$cache_dir/$${asset}"; \
	fi; \
	(cd "$$workdir/SOURCES" && sha512sum -c "$${asset}.sha512"); \
	rpmbuild -bs \
		--define "_topdir $$workdir" \
		--define "_sourcedir $$workdir/SOURCES" \
		--define "_srcrpmdir $$outdir" \
		"$$workdir/SPECS/$(SPEC)"
