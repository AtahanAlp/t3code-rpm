%global app_id t3code
%global upstream_name T3-Code
%global upstream_asset %{upstream_name}-%{version}-x86_64.AppImage
%global install_dir /opt/%{app_id}
%global debug_package %{nil}
%global __provides_exclude_from ^%{install_dir}/.*$
%global __requires_exclude_from ^%{install_dir}/.*$

Name:           t3code
Version:        0.0.24
Release:        1%{?dist}
Summary:        AI coding desktop app
License:        MIT
URL:            https://github.com/pingdotgg/t3code
Source0:        https://github.com/pingdotgg/t3code/releases/download/v%{version}/%{upstream_asset}
Source1:        t3code.desktop
Source2:        %{upstream_asset}.sha512
Source3:        LICENSE.upstream

ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
Requires:       alsa-lib
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libdrm
Requires:       libX11
Requires:       libXScrnSaver
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXrandr
Requires:       libXtst
Requires:       libxkbcommon
Requires:       mesa-libgbm
Requires:       nss
Requires:       xdg-utils

%description
T3 Code is a desktop AI coding app from T3 Tools. This package repackages
the official upstream AppImage into an RPM-managed installation.

This is an unofficial community package.

%prep
%setup -q -c -T

(cd %{_sourcedir} && sha512sum -c %{SOURCE2})

cp -p %{SOURCE0} ./t3code.AppImage
chmod +x ./t3code.AppImage
./t3code.AppImage --appimage-extract

%build
# Prebuilt upstream desktop application.

%install
install -d %{buildroot}%{install_dir}
cp -a squashfs-root/. %{buildroot}%{install_dir}/

install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/t3code <<'EOF'
#!/bin/sh
exec /opt/t3code/AppRun "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/t3code

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/t3code.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/t3code.desktop

icon_file="$(find %{buildroot}%{install_dir} -type f \
  \( -path '*/icons/hicolor/*/apps/*' -o -path '*/.DirIcon' \) \
  \( -name '*.png' -o -name '*.svg' -o -name '.DirIcon' \) \
  | sort -Vr | head -n 1)"
if [ -z "${icon_file}" ]; then
  echo "No application icon found in extracted AppImage" >&2
  exit 1
fi
case "${icon_file}" in
  *.svg) icon_ext=svg ;;
  *) icon_ext=png ;;
esac
install -Dpm 0644 "${icon_file}" "%{buildroot}%{_datadir}/pixmaps/t3code.${icon_ext}"

install -Dpm 0644 %{SOURCE3} %{buildroot}%{_licensedir}/%{name}/LICENSE.upstream

%files
%license %{_licensedir}/%{name}/LICENSE.upstream
%{install_dir}
%{_bindir}/t3code
%{_datadir}/applications/t3code.desktop
%{_datadir}/pixmaps/t3code.*

%changelog
* Wed May 27 2026 Atahan Alp <atahan@example.com> - 0.0.24-1
- Initial RPM packaging from the official upstream AppImage
