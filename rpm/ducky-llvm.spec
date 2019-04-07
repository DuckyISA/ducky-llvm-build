%global llvm_commit 2b9bf4101bed0c66082f60e862a4a4c8eb7561a7

# disable debug package, otherwise error: Empty %files file …/debugfiles.list
%define debug_package %{nil}

Name:		ducky-llvm
Version:	7.0.1
Release:	9%{?dist}
Summary:	The Low Level Virtual Machine build for Ducky VM

License:	NCSA
URL:      https://duckyisa.github.io/
Source0:  https://github.com/DuckyISA/llvm-project/archive/%{llvm_commit}/llvm-project-%{llvm_commit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:	cmake
BuildRequires:	cmake-data
BuildRequires:  make

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

This build of LLVM is patched to produce assembly code for Ducky VM.

%prep
%autosetup -n llvm-project-%{llvm_commit}

%build
mkdir -p _build
cd _build

cmake ../llvm \
         -DCMAKE_BUILD_TYPE=Release \
         -DLLVM_ENABLE_ASSERTIONS=Off \
         -DLLVM_BUILD_TESTS=ON \
         -DLLVM_BUILD_DOCS=OFF \
         -DLLVM_OPTIMIZED_TABLEGEN=ON \
         -DLLVM_TARGETS_TO_BUILD="Ducky;X86" \
         -DLLVM_DEFAULT_TARGET_TRIPLE=ducky-unknown-none \
         -DCLANG_VENDOR=duckyisa/ducky \
         -DLLVM_ENABLE_PROJECTS="clang;llvm;lld" \
         -DCMAKE_INSTALL_PREFIX=%{buildroot}/opt/ducky

cmake --build .

%install
cd _build
cmake --build . --target install
ln -s /opt/ducky/bin/llvm-ar %{buildroot}/opt/ducky/ducky-unknown-none-ar
ln -s /opt/ducky/bin/llvm-ranlib %{buildroot}/opt/ducky/ducky-unknown-none-ranlib

%files
/opt/ducky/bin/*
/opt/ducky/include/*
/opt/ducky/lib/*
/opt/ducky/libexec/*
/opt/ducky/share/*

%changelog
