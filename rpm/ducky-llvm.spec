%global llvm_commit d01c085120d92eeaafd83a3d0473a9110232833b
%global clang_commit 8e7197d38ef7c8bb812fc78e67c3cd9475c61265

Name:		ducky-llvm
Version:	4.0.0
Release:	1%{?dist}
Summary:	The Low Level Virtual Machine build for Ducky VM

License:	NCSA
URL:		https://github.com/happz/llvm
Source0:  https://github.com/happz/ducky-llvm/archive/%{llvm_commit}/ducky-llvm-%{llvm_commit}.tar.gz
Source1:  https://github.com/happz/ducky-clang/archive/%{clang_commit}/ducky-clang-%{clang_commit}.tar.gz

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
%autosetup -n ducky-llvm-%{llvm_commit}
mkdir -p tools/clang
tar xzf %{_sourcedir}/ducky-clang-%{clang_commit}.tar.gz -C tools/clang --strip 1

%build
mkdir -p _build
cd _build

cmake .. -DCMAKE_BUILD_TYPE=Release \
         -DLLVM_ENABLE_ASSERTIONS=Off \
         -DLLVM_BUILD_TESTS=OFF \
         -DLLVM_BUILD_DOCS=OFF \
         -DLLVM_OPTIMIZED_TABLEGEN=ON \
         -DLLVM_TARGETS_TO_BUILD=Ducky \
         -DLLVM_DEFAULT_TARGET_TRIPLE=ducky-none-none \
         -DCLANG_VENDOR=happz/ducky
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} -C _build

%files
/usr/local/*
%exclude /usr/lib/*

%changelog
