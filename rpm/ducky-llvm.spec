%global llvm_commit c08427226eda5683fac3495c348f3c85870948d2

# disable debug package, otherwise error: Empty %files file …/debugfiles.list
%define debug_package %{nil}

Name:		ducky-llvm
Version:	9.0.1
Release:	1%{?dist}
Summary:	The Low Level Virtual Machine build for Ducky VM

License:	NCSA
URL:        https://duckyisa.github.io/
Source0:    https://github.com/DuckyISA/ducky-llvm/archive/%{llvm_commit}/ducky-llvm-%{llvm_commit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:	cmake
BuildRequires:	cmake-data
BuildRequires:  make
# To deal with "ambiguous python shebang", we need pathfix.py
BuildRequires: /usr/bin/pathfix.py
BuildRequires:	python3-devel

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

This build of LLVM is patched to produce assembly code for Ducky VM.

%prep
%autosetup -n ducky-llvm-%{llvm_commit}

pathfix.py -i %{__python3} -pn \
    llvm/tools/opt-viewer/*.py \
    clang/tools/clang-format/clang-format-diff.py \
    clang/utils/hmaptool/hmaptool \
    clang/tools/scan-view/bin/scan-view \
    clang/tools/clang-format/git-clang-format

%build
mkdir -p _build
cd _build

cmake ../llvm \
         -DBUILD_SHARED_LIBS=ON \
         -DCLANG_VENDOR=duckyisa/ducky \
         -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_C_FLAGS=-gsplit-dwarf \
         -DCMAKE_CXX_FLAGS=-gsplit-dwarf \
         -DCMAKE_INSTALL_PREFIX=%{buildroot}/opt/ducky \
         -DLLVM_BUILD_DOCS=OFF \
         -DLLVM_BUILD_TESTS=ON \
         -DLLVM_DEFAULT_TARGET_TRIPLE=ducky-unknown-none \
         -DLLVM_ENABLE_ASSERTIONS=Off \
         -DLLVM_ENABLE_PROJECTS="clang;llvm;lld" \
         -DLLVM_OPTIMIZED_TABLEGEN=ON \
         -DLLVM_TARGETS_TO_BUILD="Ducky;X86"

cmake --build .

%install
cd _build
cmake --build . --target install
cp bin/FileCheck %{buildroot}/opt/ducky/bin/FileCheck
ln -s /opt/ducky/bin/llvm-ar %{buildroot}/opt/ducky/bin/ducky-unknown-none-ar
ln -s /opt/ducky/bin/llvm-ranlib %{buildroot}/opt/ducky/bin/ducky-unknown-none-ranlib

%files
/opt/ducky/bin/*
/opt/ducky/include/*
/opt/ducky/lib/*
/opt/ducky/libexec/*
/opt/ducky/share/*

%changelog
