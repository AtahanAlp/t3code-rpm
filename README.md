# t3code-rpm

Unofficial RPM/COPR packaging for [T3 Code](https://github.com/pingdotgg/t3code).

This package repackages the official upstream Linux AppImage into an RPM-managed
installation. It installs the extracted app under `/opt/t3code`, adds a
`/usr/bin/t3code` launcher, and installs a desktop entry so Fedora/RHEL-family
users can install, upgrade, and remove T3 Code with normal RPM tooling.

## Status

- Package name: `t3code`
- Current upstream version: `0.0.24`
- Architecture: `x86_64`
- Source artifact: `T3-Code-0.0.24-x86_64.AppImage`
- Verification: pinned upstream SHA-512 digest

This is a community package, not an official T3 Tools release. Confirm upstream
redistribution expectations before publishing a public COPR.

## How This Works

- RPM is the package format used by Fedora, RHEL, CentOS Stream, openSUSE, and
  related distributions.
- DNF is Fedora's package manager. It installs RPM packages from enabled
  repositories and handles upgrades/removal.
- COPR is Fedora's community build service. It builds RPMs and hosts a package
  repository that users can enable with `dnf copr enable`.
- This repository is the packaging source. It tells COPR how to turn the
  official T3 Code AppImage into an installable RPM.

The package is intentionally pinned to a specific upstream release and checksum.
That means every build of a given package version downloads the same AppImage,
and a changed or corrupted download fails before extraction.

## Build Locally

Install the local RPM tooling:

```sh
sudo dnf install rpm-build rpmdevtools desktop-file-utils curl make
```

Build a source RPM:

```sh
make srpm
```

Build the binary RPM from the generated SRPM:

```sh
rpmbuild --rebuild dist/t3code-*.src.rpm
```

## COPR

Create a COPR project, for example `t3code`, and add this repository as an SCM
package source.

Use:

- Clone URL: this repository URL
- Build SRPM with: `make_srpm`
- Spec file: `t3code.spec`
- Chroots: Fedora `x86_64` targets only
- Networking: enabled

For the first release, do not enable Mageia or openSUSE chroots. The spec uses
Fedora/RHEL dependency names and has only been validated for Fedora-family
builds.

After the COPR build is published, users can install with:

```sh
sudo dnf copr enable <copr-user>/t3code
sudo dnf install t3code
```

Updates are normal package updates:

```sh
sudo dnf upgrade t3code
```

Removal is also normal:

```sh
sudo dnf remove t3code
```

## Updating To A New T3 Code Release

The repository includes a GitHub Actions workflow that checks the latest
upstream T3 Code release daily. When upstream publishes a new Linux AppImage,
the workflow updates `t3code.spec` and the pinned SHA-512 file, then opens a
pull request.

Run:

```sh
./scripts/update-version.sh 0.0.25
```

Use the script manually when you want to force an update before the scheduled
workflow runs. After merging the update PR, COPR can rebuild automatically if
the package is configured with the repository webhook.

## Publishing Flow

1. Push this repository to GitHub.
2. Create a `t3code` project on https://copr.fedorainfracloud.org.
3. Add this repository as an SCM package source using `make_srpm`.
4. Enable Fedora `x86_64` chroots.
5. Keep networking enabled so the build can download the official upstream
   AppImage and verify its pinned checksum.
6. Enable the COPR webhook for the GitHub repository.
7. Trigger the first build.

Users can then run:

```sh
sudo dnf install dnf-plugins-core
sudo dnf copr enable <fedora-username>/t3code
sudo dnf install t3code
```

When a new upstream version is merged and COPR rebuilds it, users receive it
with normal system updates:

```sh
sudo dnf upgrade t3code
```

The package still needs an owner for trust and breakage response, but routine
version bumps can be handled by the scheduled workflow.

## Maintainer Model

Users do not need to manage AppImages or manually track versions after enabling
the COPR repository. They install once and update through DNF.

The packaging repository still needs an owner. In practice that means:

- creating and owning the COPR project
- merging or approving automated update pull requests
- checking failed COPR builds when upstream changes the AppImage layout
- responding if users report install/runtime issues
- deciding whether to publish builds for new Fedora releases

For normal upstream releases, the GitHub Actions workflow should do most of the
mechanical work: detect the release, update the pinned checksum, and open a pull
request. If the PR is merged and the COPR webhook is enabled, COPR publishes the
new package and users receive it through `dnf upgrade`.

## Maintainer Checks

Before publishing a new build:

```sh
make spec-check
make srpm
rpmlint dist/t3code-*.src.rpm
```

For a release-quality check, install the built RPM on a clean Fedora VM and
verify:

- `t3code` launches from a terminal
- the desktop entry appears and launches
- the icon renders
- upgrade from the previous RPM works
- `dnf remove t3code` removes package-owned files cleanly
