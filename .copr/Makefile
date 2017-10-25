srpm:
	spectool --define '_srcrpmdir $(outdir)' -C $(outdir) -g ducky-llvm.spec
	rpmbuild -bs --define '_sourcedir $(outdir)' --define '_srcrpmdir $(outdir)' ducky-llvm.spec
