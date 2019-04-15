srpm:
	dnf install -y rpmdevtools
	spectool --define '_srcrpmdir $(outdir)' -C $(outdir) -g $(spec)
	rpmbuild -bs --define '_sourcedir $(outdir)' --define '_srcrpmdir $(outdir)' $(spec)
