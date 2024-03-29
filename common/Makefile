RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "dist .remi" \
              --define "nophptag 1" \
              --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"
all: src build


arch:
	mv *.src.rpm /data/rpms/SRPMS.remi/ && echo done || echo Nothing to do
	mv x86_64/*.rpm /workspace/udntv_repository/centos/6/x86_64/

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 *.src.rpm

srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

devsrpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-dev.spec

build53:
	time rpmbuild $(RPMDEFINES) --define "phpname php53" --define "runselftest 0" -bb $(NAME).spec

bi53:
	time rpmbuild $(RPMDEFINES) --define "phpname php53" --define "runselftest 0"  -bi --short-circuit  $(NAME).spec

srpm53:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) --define "phpname php53" -bs $(NAME).spec

devsrpm53:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) --define "phpname php53" -bs $(NAME)-dev.spec

build:
	time rpmbuild $(RPMDEFINES) -bb $(NAME).spec

buildtest:
	time rpmbuild $(RPMDEFINES) -bb --with tests $(NAME).spec

buildmini:
	time rpmbuild $(RPMDEFINES) --define "runselftest 0" --without tests -bb $(NAME).spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

bc:
	rpmbuild $(RPMDEFINES) -bc --short-circuit $(NAME).spec

bi:
	rpmbuild $(RPMDEFINES) --define "runselftest 0" -bi --short-circuit $(NAME).spec

devbp:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bp $(NAME)-dev.spec

devbi:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bi --short-circuit $(NAME)-dev.spec

devbl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME)-dev.spec

bl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME).spec

devbuild:
	time rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec

devbuildmini:
	time rpmbuild $(RPMDEFINES) --define "runselftest 0" -bb $(NAME)-dev.spec

devbuildtest:
	time rpmbuild $(RPMDEFINES) --with tests -bb $(NAME)-dev.spec

sign:
	rpmsign --addsign *.src.rpm

/tmp/$(NAME)-filtered.spec: $(NAME).spec
	sed -e "s/%{phpname}/php/g;s/%{phpconfdir}/%{_sysconfdir}/g;s/%{phpbindir}/%{_bindir}/g;s/%{phpincldir}/%{_includedir}/g;s/%{_origsysconfdir}/%{_sysconfdir}/g;s/%{_origincludedir}/%{_includedir}/g" $(NAME).spec >/tmp/$(NAME)-filtered.spec

diff: /tmp/$(NAME)-filtered.spec
	colordiff -u  /tmp/$(NAME)-filtered.spec /home/extras/GIT/$(NAME)/$(NAME).spec 2>/dev/null

devdiff: /tmp/$(NAME)-filtered.spec
	colordiff -u  /tmp/$(NAME)-filtered.spec $(NAME)-dev.spec

rpmdiff:
	rpmdiff -i T -i L $(NAME) */$(NAME)*rpm

src:
	spectool -g -S $(NAME).spec

