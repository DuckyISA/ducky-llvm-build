%global llvm_commit 2b9bf4101bed0c66082f60e862a4a4c8eb7561a7

# disable debug package, otherwise error: Empty %files file …/debugfiles.list
%define debug_package %{nil}

Name:     ducky-compiler-rt
Version:	7.0.1
Release:	1%{?dist}
Summary:	The Low Level Virtual Machine build for Ducky VM

License:	NCSA
URL:      https://duckyisa.github.io/
Source0:  https://github.com/DuckyISA/llvm-project/archive/%{llvm_commit}/llvm-project-%{llvm_commit}.tar.gz

BuildRequires:  ducky-llvm
BuildRequires:  ducky-musl
#BuildRequires:  gcc-c++
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

LLVM_BUILD="/opt/ducky"

export CC="$LLVM_BUILD/bin/clang"
export CXX="$LLVM_BUILD/bin/clang++"

export CFLAGS="--target=ducky-unknown-none \
               -mllvm -disable-tail-duplicate \
               -mllvm -disable-early-taildup \
               -gsplit-dwarf \
               -fno-builtin \
               -nostdlib \
               -nostdinc -isystem $LLVM_BUILD/include"

cmake ../compiler-rt \
      -G Ninja \
      -DCC=$LLVM_BUILD/bin/clang \
      -DCMAKE_INSTALL_PREFIX=%{buildroot}/opt/ducky \
      -DCOMPILER_RT_STANDALONE_BUILD=ON \
      -DCOMPILER_RT_BUILD_BUILTINS=ON \
      -DCOMPILER_RT_BUILD_SANITIZERS=OFF \
      -DCOMPILER_RT_BUILD_XRAY=OFF \
      -DCOMPILER_RT_BUILD_LIBFUZZER=OFF \
      -DCOMPILER_RT_BUILD_PROFILE=OFF \
      -DCOMPILER_RT_INCLUDE_TESTS=ON \
      -DCMAKE_C_COMPILER=$LLVM_BUILD/bin/clang \
      -DCMAKE_AR=$LLVM_BUILD/bin/llvm-ar \
      -DCMAKE_NM=$LLVM_BUILD/bin/llvm-nm \
      -DCMAKE_RANLIB=$LLVM_BUILD/bin/llvm-ranlib \
      -DCMAKE_EXE_LINKER_FLAGS="-fuse-ld=lld" \
      -DCMAKE_C_COMPILER_TARGET="ducky-unknown-none" \
      -DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON \
      -DLLVM_CONFIG_PATH=$LLVM_BUILD/bin/llvm-config \
      -DCMAKE_C_FLAGS="$CFLAGS" \
      -DBUILTINS_TEST_TARGET_CFLAGS="$CFLAGS" \
      -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
      -DCOMPILER_RT_BAREMETAL_BUILD=ON \
      ../compiler-rt

cmake --build .

%install
cd _build
cmake --build . --target install

%files
/opt/ducky/lib/*

%changelog
