%global VERSION 4.0.50
%global RELEASE 1

%global source_tag %{VERSION}-%{RELEASE}

# disable check-buildroot - buildroot is mentioned in binaries, some __FILE__ or what?
%define __arch_install_post %{nil}

# disable debug package, otherwise error: Empty %files file …/debugfiles.list
%define debug_package %{nil}

Name:     ducky-qemu
Version:  %{VERSION}
Release:  %{RELEASE}%{?dist}
Summary:  QEMU (https://www.qemu.org/) is a generic and open source machine & userspace emulator and virtualizer. This is a QEMU build with support for running binaries compiled for Ducky platform (https://duckyisa.github.io/).

License:  QEMU license
URL:      https://github.com/DuckyISA/ducky-qemu
Source0:  http://fanny.happz.cz/~happz/ducky-dist/ducky-qemu-%{source_tag}.tar.bz2

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  make
BuildRequires:  pixman-devel
BuildRequires:  python2
BuildRequires:  zlib-devel

%description
QEMU [1] is a generic and open source machine & userspace emulator and virtualizer.

This is a QEMU build with support for running binaries compiled for Ducky platform [2].

[1] https://www.qemu.org/
[2] https://duckyisa.github.io/

%prep
%autosetup -n ducky-qemu-%{source_tag}

%build
mkdir -p _build
cd _build

../configure --disable-user \
             --target-list=ducky-softmmu \
             --prefix=%{buildroot}/opt/ducky \
             --python=/usr/bin/python2

make %{?_smp_mflags}

%install
cd _build
make install

%files
/opt/ducky/bin/*
/opt/ducky/libexec/*
/opt/ducky/share/*
/opt/ducky/var/run

%changelog
