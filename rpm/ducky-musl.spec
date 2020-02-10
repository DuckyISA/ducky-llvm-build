%global musl_commit 5b674266403f0342bd018a3618af4c6e7f152755

# disable debug package, otherwise error: Empty %files file …/debugfiles.list
%define debug_package %{nil}

Name:     ducky-musl
Version:	1.1.24
Release:	1%{?dist}
Summary:	musl (an MIT-licensed implementation of the standard C library) build for Ducky ISA

License:	MIT
URL:      https://duckyisa.github.io/
Source0:  https://github.com/DuckyISA/ducky-musl/archive/%{musl_commit}/ducky-musl-%{musl_commit}.tar.gz

BuildRequires: ducky-llvm
#BuildRequires:  gcc-c++
#BuildRequires:  ninja-build
#BuildRequires:	cmake
#BuildRequires:	cmake-data
#BuildRequires:  make

%description
musl, pronounced like the word "mussel", is an MIT-licensed
implementation of the standard C library targetting the Linux syscall
API, suitable for use in a wide range of deployment environments. musl
offers efficient static and dynamic linking support, lightweight code
and low runtime overhead, strong fail-safe guarantees under correct
usage, and correctness in the sense of standards conformance and
safety. musl is built on the principle that these goals are best
achieved through simple code that is easy to understand and maintain.

This build of musl library is patched to work with Ducky ISA boards.

%prep
%autosetup -n ducky-musl-%{musl_commit}

%build
mkdir -p _build
cd _build

# Musl calls $CROSS_COMPILE-{ar,ranlib} directly, without the path. hence extending PATH
# to let it find them.
export PATH="/opt/ducky/bin:$PATH"

export CC=/opt/ducky/bin/clang
export CFLAGS="--target=ducky-unknown-none \
               -mllvm -disable-tail-duplicate \
               -mllvm -disable-early-taildup \
               -gsplit-dwarf=single \
               -fno-builtin \
               -nostdlib \
               -nostdinc \
               -O2"

../configure --prefix=%{buildroot}/opt/ducky \
             --target=ducky-unknown-none \
             --disable-shared

make -j1

%install
cd _build
make install

%files
/opt/ducky/include/*
/opt/ducky/lib/*

%changelog
