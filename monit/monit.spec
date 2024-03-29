# $Id$
# Authority: shuff
# Upstream: <info$mmonit,com>

%define logmsg logger -t %{name}/rpm
%define buildnumber %(date +%Y%m%d%H%M)

%define repo https://bitbucket.org/hippo_lin/monit.git 
%define branch master

Summary: Process monitor and restart utility
Name: monit
Version: 5.7
Release: %{buildnumber}%{?dist}
Epoch: 2
License: GPLv3
Group: Applications/Internet
URL: http://mmonit.com/monit/

#Source0: http://mmonit.com/monit/dist/monit-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: git
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: bison
BuildRequires: byacc
BuildRequires: flex
BuildRequires: gcc
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: perl
BuildRequires: /usr/bin/logger
BuildRequires: pam-devel

%description
Monit is an utility for monitoring daemons or similar programs running on
a Unix system. It will start specified programs if they are not running
and restart programs not responding.

%prep
%setup -q -T -c -n monit

git clone %{repo} .
git checkout -f %{branch}

%{__perl} -pi.orig -e 's|\bmonitrc\b|monit.conf|' src/monit.h
%{__perl} -pi.orig -e 's|^#\s+(include .*)$|$1|' monitrc

# store id and state files in /var/monit
%{__perl} -pi.orig -e 's|^#(\s+)set (id\|state)file /var/\.monit\.(id\|state)$|set $2file /var/monit/$3|' monitrc

# fix config path in /etc/init.d/monit
%{__perl} -pi.orig -e 's|monitrc|monit.conf|' contrib/rc.monit

./bootstrap

%build
%configure \
	--with-ssl-lib-dir="%{_libdir}"
%{__make}

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	BINDIR="%{buildroot}%{_bindir}" \
	MANDIR="%{buildroot}%{_mandir}/man1/"

%{__install} -Dp -m0755 contrib/rc.monit %{buildroot}%{_initrddir}/monit
%{__install} -Dp -m0600 monitrc %{buildroot}%{_sysconfdir}/monit.conf

%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/monit.d/
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/lib/monit/

# create folder where state and id are stored
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/monit/

%pre
if ! /usr/bin/id monit &>/dev/null; then
	/usr/sbin/useradd -M -r -d %{_localstatedir}/lib/monit -s /bin/sh -c "monit daemon" monit || \
		%logmsg "Unexpected error adding user \"monit\". Aborting installation."
fi

%post
/sbin/chkconfig --add monit

# Moving old style configuration file to conf standard location
if [ -f %{_sysconfdir}/monitrc ]; then
    mv -f %{_sysconfdir}/monitrc %{_sysconfdir}/monit.conf
fi

%preun
if [ $1 -eq 0 ]; then
	service monit stop &>/dev/null || :
	/sbin/chkconfig --del monit
fi

%postun
/sbin/service monit condrestart &>/dev/null || :
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel monit || %logmsg "User \"monit\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGES COPYING README*
%doc %{_mandir}/man?/*
%{_initrddir}/monit
%config %{_sysconfdir}/monit.d/
%config %{_localstatedir}/monit/
%{_localstatedir}/lib/monit/
%attr(0755, root, root) %{_bindir}/monit
%attr(0600, root, root) %config(noreplace) %{_sysconfdir}/monit.conf

%changelog
* Thu Sep 19 2013 David Hrbáč <david@hrbac.cz> - 5.5-2
- pam-devel build requirement

* Mon Dec 17 2012 David Hrbáč <david@hrbac.cz> - 5.5-1
- new upstream release

* Mon May 28 2012 David Hrbáč <david@hrbac.cz> - 5.4-1
- new upstream release

* Tue Apr 17 2012 Derek Tamsen <dtamsen@gmail.com> - 5.3.2-3
- Fixed monitor.h source path so it can be patched to reference /etc/monit.conf instead of /etc/monitrc
- Updated /etc/init.d/monit so config path is /etc/monit.conf
- Added /var/monit so the state and id files can be create upon monit startup
- Updated post section to move /etc/monitrc to /etc/monit.conf for os standardization

* Mon Jan 23 2012 David Hrbáč <david@hrbac.cz> - 5.3.2-2
- use upstream configuration file location

* Tue Jan 17 2012 David Hrbáč <david@hrbac.cz> - 5.3.2-1
- new upstream release

* Mon Apr 04 2011 David Hrbáč <david@hrbac.cz> - 5.2.5-1
- new upstream release

* Tue Feb 22 2011 David Hrbáč <david@hrbac.cz> - 5.2.4-1
- new upstream release

* Tue Nov 30 2010 Steve Huff <shuff@vecna.org> - 5.2.3-1
- Updated to release 5.2.3.

* Thu Sep 23 2010 Steve Huff <shuff@vecna.org> - 5.2-1
- Updated to release 5.2.

* Mon Apr 12 2010 Chris Butler <rf@crustynet.org.uk> - 5.1.1-1
- Updated to release 5.1.1

* Tue Dec 8 2009 Yury V. Zaytsev <yury@shurup.com> - 5.0.3-2
- Committed to RPMForge.

* Mon Nov 16 2009 Justin Shepherd <jshepher@rackspace.com> - 5.0.3-1
- Updated to release 5.0.3.
- Using the provided monit init script.

* Sat Apr 18 2009 Dries Verachtert <dries@ulyssis.org> - 5.0-1
- Updated to release 5.0.

* Mon Jun 18 2007 Dag Wieers <dag@wieers.com> - 4.9-2
- Enable the use of /etc/monit.d/ in the config-file. (Oren Held)

* Tue Feb 20 2007 Dag Wieers <dag@wieers.com> - 4.9-1
- Updated to release 4.9.

* Tue Jun 13 2006 Dag Wieers <dag@wieers.com> - 4.8.1-4
- Fixed type in %%preun that failed to stop monit. (Jim Robinson)

* Mon May 29 2006 Dag Wieers <dag@wieers.com> - 4.8.1-3
- Fixed reference to monitrc from monitor.h. (Tim Jackson)

* Thu May 18 2006 Dag Wieers <dag@wieers.com> - 4.8.1-2
- Fixed the nagios references in the monit user creation. (Tim Jackson)
- Removed the -o option to useradd. (Tim Jackson)

* Wed May 17 2006 Dag Wieers <dag@wieers.com> - 4.8.1-1
- Updated to release 4.8.1.
- Added %%{_sysconfdir}/monit.d/ and %%{_localstatedir}/lib/monit/. (Michael C. Hoffman)
- Creation/removal of user monit. (Michael C. Hoffman)

* Mon May 08 2006 Dag Wieers <dag@wieers.com> - 4.8-1
- Updated to release 4.8.

* Thu Jan 12 2006 Dag Wieers <dag@wieers.com> - 4.7-1
- Updated to release 4.7.

* Fri Sep 24 2004 Dag Wieers <dag@wieers.com> - 4.4-1
- Updated to release 4.4.

* Thu May 13 2004 Dag Wieers <dag@wieers.com> - 4.3-1
- Updated to release 4.3.

* Mon Apr 05 2004 Dag Wieers <dag@wieers.com> - 4.2.1-1
- Updated to release 4.2.1.

* Fri Mar 26 2004 Dag Wieers <dag@wieers.com> - 4.2.0-0
- Updated to release 4.2.0.

* Sun Nov 23 2003 Dag Wieers <dag@wieers.com> - 4.1.1-0
- Updated to release 4.1.1.

* Mon Oct 13 2003 Dag Wieers <dag@wieers.com> - 4.0-0
- Initial package. (using DAR)
