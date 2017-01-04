%define last_git_commit 2e5b915
%define last_git_version 146

Summary:	Tool to translate x86-64 CPU Machine Check Exception data.
Name:		mcelog
Version:	146
Release:	1.%{last_git_commit}%{?dist}
Epoch:		2
Group:		System Environment/Base
License:	GPLv2
Source0:	https://github.com/andikleen/mcelog/archive/v%{last_git_version}.tar.gz
# single unified patch relative to upstream
Patch0:		mcelog-alti6.patch
URL:		https://github.com/andikleen/mcelog.git
Buildroot:	%{_tmppath}/%{name}-%{version}-root
ExclusiveArch:	x86_64

%description
mcelog is a daemon that collects and decodes Machine Check Exception data
on x86-64 machines.

%prep
%setup -q -n %{name}-%{last_git_version}
%patch0 -p1

# This can be removed at the next update.
chmod a+x triggers/*

%build
make CFLAGS="$RPM_OPT_FLAGS -fpie -pie"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,8}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mcelog
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install mcelog $RPM_BUILD_ROOT%{_sbindir}/mcelog
install mcelog.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/mcelog.cron
cp mcelog.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -m 755 mcelog.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mcelogd
cp mcelog.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mcelogd
cp mcelog.conf $RPM_BUILD_ROOT%{_sysconfdir}/mcelog/mcelog.conf
cp mcelog.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mcelog
cp triggers/* $RPM_BUILD_ROOT%{_sysconfdir}/mcelog/

cd ..
chmod -R a-s $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add mcelogd

%files
%defattr(-,root,root,-)
%doc README.md CHANGES
%{_sbindir}/mcelog
%{_sysconfdir}/cron.hourly/mcelog.cron
%attr(0644,root,root) %{_mandir}/*/*
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/mcelogd
%{_sysconfdir}/sysconfig/mcelogd
%{_sysconfdir}/mcelog/
%{_sysconfdir}/logrotate.d/mcelog

%changelog
* Tue Jan 01 2017 Tucker <junk@altiscale.com> 2:146.1
- updated to upstream 146
- updated patch file and renamed to alti6

* Mon Oct 26 2015  Prarit Bhargava <prarit@redhat.com> 2:128.1
- updated to upstream 128
- a little better documentation to /etc/mcelog/mcelog.conf [1136920]
- Atom cpuids [1206320]
- Broadwell-DE cpuid [1206320]
- Skylake (0x4e and 0x5e) cpuids [1255561]
- fix cpu buffer overflow warning [1136920]

* Fri Feb 13 2015  Prarit Bhargava <prarit@redhat.com> 2:109.4
- move triggers to /etc/mcelog

* Tue Feb 10 2015  Prarit Bhargava <prarit@redhat.com> 2:109.3
- rename source tarball to 109

* Fri Feb  6 2015  Prarit Bhargava <prarit@redhat.com> 2:109.2
- unify all rhel patches into single patch for simplicity

* Fri Feb  6 2015  Prarit Bhargava <prarit@redhat.com> 2:109.1
- updated to upstream 109, brought in previous Haswell and additional fixes
- add Broadwell support, currently unsupported in kernel

* Wed Mar 26 2014  Prarit Bhargava <prarit@redhat.com> 2:101.0
- Decode MISC register when IO MCA occurs
- add and fix leaky bucket logging
- exit with EXIT_SUCCESS (aka 0) when stopped by signal
- Fix missing handling for flag MCE_GETCLEAR_FLAGS
- Decode new simple error code number 6
- introduce new NVR scheme to sync with upstream

* Fri Mar 21 2014  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.14
- add /etc/logrotate.d/mcelog file [849252]
- add chkconfig levels to mcelogd initscript [1006293]
- fix IvyBridge detection (commits b29cc4d and 2577aeb) [1079360]
- cleanup .orig and .rej patch files [1059227]
- add Haswell CPUID 0x3f [1079501]
- Modify --daemon logic to allow syslog-only output [872387]

* Tue Aug 20 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.13
- update fix for mcelog.cron not running if mcelogd service is running [875824]

* Wed Aug 14 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.12
- Disable extended logging support [BZ 996634]

* Wed Aug 14 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.11
- Add support for Haswell [BZ 991079]

* Mon Jun  3 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.10
- do not run mcelog.cron if mcelogd service is running [875824]

* Fri Mar 22 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.9
- update fix for AMD family 15 is supported in mcelog

* Tue Mar 19 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.8
- Add support for IvyBridge [BZ 881555]

* Mon Mar 18 2013  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.7
- Add support for SandyBridge EP [BZ 922873]

* Wed Oct 31 2012  Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.6
- AMD family 15 is supported in mcelog [BZ 871249]

* Wed Sep  5 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.5
- Fix typo with --supported flag in manpage [BZ 851406]

* Tue Aug 14 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.4
- Fix source file damage associated with fix for BZ 740915

* Tue Aug 14 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.2
- Fix spec file damage associated with fix for BZ 740915

* Tue Aug 14 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814_2-0.1
- Do not run on newer AMD processors [BZ 795931]

* Tue Aug 14 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20120814-0.1
- Add IvyBridge client CPUID [BZ 740915]

* Tue Feb 21 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.14
- Add --supported option to mcelog; include misc fixes [BZ 795508] - v2
- added missing man page documentation for --supported option

* Tue Feb 21 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.13
- Add --supported option to mcelog; include misc fixes [BZ 795508]

* Thu Feb  9 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.12
- cron mcelog: mcelog read: No such device at first boot [BZ 784091]

* Wed Feb  1 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.11
- Do not support AMD family > 15 in mcelog, patch updated [BZ 746785]

* Tue Jan 31 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.10
- Do not print unsupported CPU message in mcelog [BZ 769363]

* Mon Jan 30 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.9
- Do not support AMD family > 15 in mcelog [BZ 746785]

* Tue Jan 26 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.8
- RHEL6 mcelog: Update README RPM package [BZ 728265]

* Mon Jul 18 2011 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.7
- Updated to 1.0pre3 as of Jul 18 2011/cbd4da48 [BZ 699592]
- chkconfig mcelogd on by default [BZ 699592]

* Mon Mar 07 2011 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.6
- comment out default error handling in /etc/mcelog/mcelog.conf [BZ 682753]

* Tue Feb 22 2011 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.5
- fix type in LOCKFILE location [BZ 614874]

* Tue Nov 16 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.4
- add /etc/mcelog/mcelog.conf file [BZ 647066]

* Mon Nov 15 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.3
- add /var/lock/subsys/mcelogd lockfile [BZ 614874]

* Mon Nov 15 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.2
- updated to 1.0pre3 as of Nov 12 2010 [BZ 646568]
- pulled from %{URL}

* Thu Apr 08 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3-0.2
- fixed initscript and added /etc/sysconfig/mcelog (BZ 576284)

* Wed Jan 27 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3-0.1
- updated to 1.0pre3
- added initscript for Predictive Failure Analysis (PFA) which does not
  run by default.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:0.9pre1-0.2
- Rebuilt for RHEL 6

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

