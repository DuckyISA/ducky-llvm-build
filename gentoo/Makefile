ROOTDIR ?= /tmp
PREFIX ?= /opt/llvm
JOBS ?= 1
LLVM_REPO ?= https://github.com/happz/llvm.git
CLANG_REPO ?= https://github.com/happz/clang.git
UPLOAD_DIR ?= /tmp/llvm-upload

NINJA ?= ninja

LLVM_OPTIONS := -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_ASSERTIONS=Off -DLLVM_BUILD_TESTS=OFF -DLLVM_BUILD_DOCS=OFF \
                -DCMAKE_INSTALL_PREFIX=$(PREFIX) -DLLVM_OPTIMIZED_TABLEGEN=ON \
		-DLLVM_TARGETS_TO_BUILD=Ducky -DLLVM_DEFAULT_TARGET_TRIPLE=ducky-none-none -DCLANG_VENDOR=happz/ducky


llvm_repo_dir := $(ROOTDIR)/llvm-repo
llvm_build_dir := $(ROOTDIR)/llvm-build-Release

llvm_package := $(ROOTDIR)/llvm-release.tar.gz


all: upload


llvm-fetch-repos:
	$(Q) rm -rf $(llvm_repo_dir)
	$(Q) git clone $(LLVM_REPO) $(llvm_repo_dir)
	$(Q) git clone $(CLANG_REPO) $(llvm_repo_dir)/tools/clang


llvm-build: llvm-fetch-repos
	$(Q) rm -rf $(llvm_build_dir)
	$(Q) mkdir -p $(llvm_build_dir)
	$(Q) cd $(llvm_build_dir) && cmake -G Ninja $(LLVM_OPTIONS) $(llvm_repo_dir)
	$(Q) cd $(llvm_build_dir) && $(NINJA) -j$(JOBS)


llvm-install: llvm-build
	$(Q) cd $(llvm_build_dir) && $(NINJA) install


$(llvm_package): llvm-install
	$(Q) tar czf $(llvm_package) $(PREFIX)


package: $(llvm_package)

upload: package
	cp $(llvm_package) $(UPLOAD_DIR)/


clean:
	$(Q) rm -rf $(llvm_repo_dir)
	$(Q) rm -rf $(llvm_build_dir)
	$(Q) rm -rf $(llvm_package)
