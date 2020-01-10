%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}

%global specversion 13
%global upstream_version 0.4.4

%define _default_patch_fuzz 2

# Keep around for when/if required
#global alphatag #{upstream_version}.git

%global mh_release %{?alphatag:0.}%{specversion}%{?alphatag:.%{alphatag}}%{?dist}

Name:		mingw32-matahari
Version:	0.4.4
Release:	%{mh_release}
Summary:	Matahari QMF Agents for Windows guests

Group:		Applications/System
License:	GPLv2
URL:		https://github.com/matahari/matahari/wiki

Source0:	http://github.com/matahari/matahari/downloads/matahari-%{upstream_version}.tar.gz
Patch1:		674578-remove-kstart.diff
Patch2:		bz737088-1-add-man-pages.diff
Patch3:		bz737137-1-fix-sysconfig-issues.diff
Patch4:		bz737618-1-kill-old-processes-on-upgrade.diff
Patch5:		bz739666-1-fix-NULL-UUID.diff
Patch6:		bz737137-2-fix-sysconfig-issues.diff
Patch7:		bz740038-1-fix-sysconfig-no-response.diff
Patch8:		bz735426-1-check-malloc-return-for-coverity.diff
Patch9:		bz740090-1-sysconfig-validate-key-names.diff
Patch10:	bz740090-2-add-mh_string_copy.diff
Patch11:	bz740091-1-store-sysconfig-keys-in-subdir.diff
Patch12:	bz741965-1-check-sysconfig-keys-sooner.diff
Patch13:	bz735426-2-fix-warning.diff
Patch14:	bz737088-2-dont-use-help2man.diff
Patch15:	bz806948-1-dont-link-qpid-unstable.diff

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	redhat-rpm-config cmake make qpid-qmf-devel
BuildRequires:	mingw32-filesystem >= 57
BuildRequires:	mingw32-gcc-c++ mingw32-nsis genisoimage
BuildRequires:	mingw32-pcre mingw32-qpid-cpp mingw32-srvany mingw32-glib2 mingw32-sigar

%description

Matahari provides a QMF Agent that can be used to control and manage
various pieces of functionality for an ovirt node, using the AMQP protocol.

The Advanced Message Queuing Protocol (AMQP) is an open standard application
layer protocol providing reliable transport of messages.

QMF provides a modeling framework layer on top of qpid (which implements
AMQP).  This interface allows you to manage a host and its various components
as a set of objects with properties and methods.

MinGW cross-compiled Windows application.

%prep
%setup -q -n matahari-%{upstream_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p0

%build
PATH=%{_mingw32_bindir}:$PATH

%{_mingw32_cmake} --debug-output -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_VERBOSE_MAKEFILE=on
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make VERBOSE=1 %{?_smp_mflags} package
genisoimage -o matahari-%{version}-win32.iso matahari-%{version}-win32.exe src/windows/autorun.inf

%{__install} -d $RPM_BUILD_ROOT/%{_mingw32_datadir}/matahari
%{__install} matahari-%{version}-win32.iso $RPM_BUILD_ROOT/%{_mingw32_datadir}/matahari

%clean
test "x%{buildroot}" != "x" && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mingw32_datadir}/matahari

%doc AUTHORS COPYING

%changelog
* Tue May 08 2012 Zane Bitter <zbitter@redhat.com> - 0.4.4-13
- Rebuild against latest Qpid to remove extraneous dependencies
  Resolves: rhbz#785192

* Wed Mar 28 2012 Jeff Peeler <jpeeler@redhat.com> - 0.4.4-12
- Remove dependence on unstable ABI of Qpid
  Resolves: rhbz#806948

* Mon Nov 07 2011 Adam Stokes <astokes@fedoraproject.org> - 0.4.4-11
- fix qpid-qmf-devel buildrequire
- Related: rhbz#751799

* Wed Oct 05 2011 Russell Bryant <rbryant@redhat.com> 0.4.4-10
- sync with linux package
- Resolves: rhbz#741965, rhbz#737088, rhbz#737541

* Mon Sep 26 2011 Russell Bryant <rbryant@redhat.com> 0.4.4-6
- sync with linux package
- Resolves: rhbz#740090, rhbz#740091
- Related: rhbz#735426

* Mon Sep 19 2011 Russell Bryant <rbryant@redhat.com> 0.4.4-5
- sync with linux package
- Resolves: rhbz#740038

* Mon Sep 19 2011 Russell Bryant <rbryant@redhat.com> 0.4.4-4
- Import all patches from matahari package
- rebuild to include latest mingw32-sigar
- Resolves: rhbz#737088, rhbz#737137, rhbz#737618, rhbz#739666
- Resolves: rhbz#739952, rhbz#737541

* Thu Sep 08 2011 Russell Bryant <rbryant@redhat.com> 0.4.4-2
- Rebase to upstream release 0.4.4
- Resolves: rhbz#735419, rhbz#735429, rhbz#733483. rhbz#734981
- Resolves: rhbz#735426, rhbz#734536, rhbz#733468, rhbz#734522
- Resolves: rhbz#733393, rhbz#736468
- Resolves: rhbz#733384, rhbz#733393, rhbz#733451, rhbz#731858
- Resolves: rhbz#733150, rhbz#714249 

* Wed Aug 24 2011 Russell Bryant <rbryant@redhat.com> 0.4.2-9
- Sync the windows package with the linux version
  - Update patch level to: 468fc0b
- Related: rhbz#732498, rhbz#730087, rhbz#731914. rhbz#731858, rhbz#731233
- Related: rhbz#729332, rhbz#730044, rhbz#730066, rhbz#731534, rhbz#714249
- Related: rhbz#728360, rhbz#733013

* Tue Aug 16 2011 Andrew Beekhof <abeekhof@fedoraproject.org> 0.4.2-6
- Sync the windows package with the linux version:
  - Rebase on new upstream release: 325f740
  - Update patch level to: 6b5df25
- Related: rhbz#730066, rhbz#727194, rhbz#728360, rhbz#730087,
	rhbz#729516, rhbz#729331, rhbz#728977, rhbz#728988,
	rhbz#728631, rhbz#729063, rhbz#727192, rhbz#714249,
	rhbz#688191, rhbz#727961, rhbz#688193

* Tue Jul 26 2011 Adam Stokes <astokes@fedoraproject.org> 0.4.2-2
- Rebase to latest upstream
- Related: rhbz#709649

* Wed Apr 20 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.4.0-5
- Bump the version to sync with Linux package
- Related: rhbz#698370

* Wed Apr 20 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.4.0-4
- Bump the version to sync with Linux package
- Related: rhbz#698370

* Fri Apr 15 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.4.0-3
- Bump the version to sync with Linux package
- Related: rhbz#696810

* Fri Apr  1 2011 Andrew Beekhof <abeekhof@redhat,com> - 0.4.0-1
- Convert agents to the QMFv2 API
- Removed empty debug package
  Related: rhbz#658840

* Wed Mar 30 2011 Lon Hohberger <lhh@redhat.com> 0.4.0-0.3.0b41287.git
- Rebuilt against latest version of QPid and QMF libraries
  Related: rhbz#658840

* Fri Feb  4 2011 Andrew Beekhof <andrew@beekhof.net> - 0.4.0-0.2.0b41287.git
- Update to upstream version 2798d52.git
  + Support password authentication to qpid
  + Prevent errors when matahari is started at boot
  Related: rhbz#658840

* Thu Jan 13 2011 Andrew Beekhof <andrew@beekhof.net> - 0.4.0-0.1.0b41287.git
- Initial import

