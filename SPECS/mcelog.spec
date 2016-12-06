%define	last_tar_git_commit d2e13bf0
%define	last_git_commit e4aca63

Summary:	Tool to translate x86-64 CPU Machine Check Exception data
Name:		mcelog
Version:	136
Release:	2.%{last_git_commit}%{?dist}
Epoch:		3
Group:		System Environment/Base
License:	GPLv2
Source0:	mcelog-%{last_tar_git_commit}.tar.bz2
# note that this source OVERRIDES the one on the tarball above!
Source1:	mcelog.conf
Source2:	mcelog.service
Source10:	mcelog.setup
Patch0:		mcelog-fix-trigger-path-and-cacheing.patch
# BZ 1039183: Add Haswell and correct Ivy Bridge
Patch1:		mcelog-update-2577aeb.patch
Patch2:		mcelog-update-f30da3d.patch
# BZ 1138319: Add additional Haswell support (see patch for additional info)
Patch3:		mcelog-haswell-support.patch
Patch4:		mcelog-update-9de4924.patch
Patch5:		mcelog-update-e7e0ac1.patch
Patch6:		mcelog-patch-1bd2984.patch
Patch7:		mcelog-update-e4aca63.patch
URL:		https://github.com/andikleen/mcelog.git
Buildroot:	%{_tmppath}/%{name}-%{version}-root
ExclusiveArch:	i686 x86_64
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
BuildRequires: systemd

%description
mcelog is a utility that collects and decodes Machine Check Exception data
on x86-32 and x86-64 systems. It can be run either as a daemon, or by cron.

%prep
%setup -q -n %{name}-%{last_tar_git_commit}
%patch0 -p1 -b .fix-triggers-and-cacheing
%patch1 -p1 -b .mcelog-update-2577aeb
%patch2 -p1 -b .mcelog-update-f30da3d
%patch3 -p1 -b .mcelog-haswell-support
%patch4 -p1 -b .mcelog-update-9de4924
%patch5 -p1 -b .mcelog-update-e7e0ac1
%patch6 -p1 -b .mcelog-patch-1bd2984
%patch7 -p1 -b .mcelog-patch-e4aca63

%build
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}

make CFLAGS="$RPM_OPT_FLAGS  -Wl,-z,relro,-z,now -fpie" LDFLAGS="-Wl,-z,relro,-z,now -fpie -pie"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{1,5,8}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.hourly
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
install -p -m755 mcelog $RPM_BUILD_ROOT/%{_sbindir}/mcelog
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/mcelog.conf
install -p -m755 %{SOURCE10} $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/mcelog.setup
install -p -m755 triggers/cache-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/cache-error-trigger
install -p -m755 triggers/dimm-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/dimm-error-trigger
install -p -m755 triggers/page-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/page-error-trigger
install -p -m755 triggers/socket-memory-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/socket-memory-error-trigger
install -p -m755 mcelog.cron $RPM_BUILD_ROOT/%{_sysconfdir}/cron.hourly/mcelog.cron
install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/mcelog.service
install -p -m644 mcelog.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m644 mcelog.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5
install -p -m644 mcelog.triggers.5 $RPM_BUILD_ROOT/%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%post
systemctl enable mcelog.service &> /dev/null ||
systemctl daemon-reload &> /dev/null

%preun
# Handle removing mcelog
if [ "$1" -eq 0 ]; then
	systemctl disable mcelog.service &> /dev/null
	systemctl stop mcelog.service &> /dev/null
fi

%postun
# Handle upgrading mcelog
if [ "$1" -ge 1 ]; then
	systemctl try-restart mcelog.service &> /dev/null
fi

%files
%defattr(-,root,root,-)
%doc README CHANGES
%{_sbindir}/mcelog
%dir %{_sysconfdir}/mcelog
%{_sysconfdir}/mcelog/triggers
%config(noreplace) %{_sysconfdir}/mcelog/mcelog.conf
%{_sysconfdir}/mcelog/mcelog.setup
%{_sysconfdir}/cron.hourly/mcelog.cron
%{_unitdir}/mcelog.service
%attr(0644,root,root) %{_mandir}/*/*

%changelog
* Mon Oct 31 2016 Prarit Bhargava <prarit@redhat.com> - 3:136.2.e4aca63
- fix post-uninstall script warning during upgrade [1388427]
* Fri May 13 2016 Prarit Bhargava <prarit@redhat.com> - 3:136-1.e4aca63
- update NVR to 136 to match upstream [1336431]
- additional general fixes [1336431]
- Skylake Client support (6,94) (6,78) [1255571]
- Broadwell SoC/DE, EP & EX support (6,79) [1255572]
* Mon Sep 21 2015 Prarit Bhargava <prarit@redhat.com> - 3:120-3.e7e0ac1
- Fix server restart when /var/run/mcelog-client socket exists [1256714]
* Fri Jun 12 2015 Prarit Bhargava <prarit@redhat.com> - 3:120-2.e7e0ac1
- add RELRO and PIE [1092567]
* Fri Jun 12 2015 Prarit Bhargava <prarit@redhat.com> - 3:120-1.e7e0ac1
- Add Broadwell-U, Broadwell-DE, and Knights Landing/Xeon Phi Support
- additional general fixes
- add mcelog.conf and mcelog.triggers man pages
- update NVR to 120 to match upstream
* Mon Oct 27 2014 Prarit Bhargava <prarit@redhat.com> - 3:101-3.9de4924
- Update with latest minor fixes, no new support [1157683]

* Mon Sep  8 2014 Prarit Bhargava <prarit@redhat.com> - 3:101-2.f30da3d
- Additional Haswell Support [1138319]

* Thu Sep  4 2014 Prarit Bhargava <prarit@redhat.com> - 3:101-1.f30da3d
- Update to upstream NVR (101) [1136989]

* Wed Sep  3 2014 Prarit Bhargava <prarit@redhat.com> - 2:1.0-0.13.f30da3d
- Update to upstream commit f30da3d, minor fixes, no features [1085134]
- Add /var/log/mcelog file [1098864]
- remove .src.rpm file [1038755]

* Wed Jan 22 2014 Prarit Bhargava <prarit@redhat.com> - 2:1.0-0.12.2577aeb
- Add Haswell client cpuids, identify Ivy Bridge properly, and fix issues
  on Ivy Bridge

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2:1.0-0.11.d2e13bf0
- Mass rebuild 2013-12-27

* Tue Dec  3 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.10.d2e13bf0
- Fix prebuilt binaries issue in tarball [1037730]

* Thu Nov 21 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.9.d2e13bf0
- disable extended logging suppport [1028645]

* Wed May 15 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.8.d2e13bf0
- update to commit d2e13bf0 [963287]

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.7.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.6.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Jon Ciesla <limburgher@gmail.com> - 2:1.0-0.5.6e4e2a00
- Merge review fixes, BZ 226132.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.4.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.3.6e4e2a00
- Updated sources to deal with various warning issues [701083] [704302]
- Update URL for new location of Andi's mcelog tree
- Update n-v-r to include latest git hash

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.3.pre3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Jon Masters <jcm@redhat.com> 2:1.0-0.2.pre3
- Rework mcelog to use daemon mode and systemd.

* Tue Nov 09 2010 Jon Masters <jcm@redhat.com> 2:1.0-0.1.pre3
- Bump epoch and use standard Fedora Packaging Guidelines for NVR.
- Switch to using signed bz2 source and remove dead patch.

* Fri Sep 17 2010 Dave Jones <davej@redhat.com> 1:1.0pre3-0.1
- Update to upstream mcelog-1.0pre3

* Mon Oct 05 2009 Orion Poplawski <orion@cora.nwra.com> - 1:0.9pre1-0.1
- Update to 0.9pre1
- Update URL
- Add patch to update mcelog kernel record length (bug #507026)

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 0.7-5
- Fix %%install for new buildroot cleanout.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.7-2
- fix license tag
- clean this package up

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.7-1.22
- Autorebuild for GCC 4.3

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- Rebuild.

* Fri Jun 30 2006 Dave Jones <davej@redhat.com>
- Rebuild. (#197385)

* Wed May 17 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.7
- Change frequency to hourly instead of daily.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Wed Feb  8 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.6

* Mon Dec 19 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.5

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Wed Feb  9 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.4

* Thu Jan 27 2005 Dave Jones <davej@redhat.com>
- Initial packaging.

