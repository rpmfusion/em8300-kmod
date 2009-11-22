# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

#define prever  rc1

Name:           em8300-kmod
Summary:        Kernel modules for DXR3/Hollywood Plus MPEG decoder cards
Version:        0.17.4
Release:        1%{?dist}.2

Group:          System Environment/Kernel
License:        GPLv2+
URL:            http://dxr3.sourceforge.net/
#Source0: http://dxr3.sourceforge.net/download/em8300-%{version}%{?prever:-%{prever}}.tar.gz with modules/em8300.uc removed
#Source0:        em8300-nofirmware-%{version}%{?prever:-%{prever}}.tar.lzma
Source0:        http://downloads.sourceforge.net/dxr3/em8300-nofirmware-%{version}%{?prever:-%{prever}}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
%{summary}.


%prep
%{?kmodtool_check}
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c
for kernel_version  in %{?kernel_versions} ; do
    cp -a em8300-%{version}%{?prever:-%{prever}} \
        _kmod_build_${kernel_version%%___*}
done


%build
for kv in %{?kernel_versions} ; do
    d=$PWD/_kmod_build_${kv%%___*}
    make -C "${kv##*___}" SUBDIRS=$d/modules EM8300_DIR=$d V=1
done


%install
rm -rf $RPM_BUILD_ROOT
for kv in %{?kernel_versions} ; do
    d=$RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kv%%___*}/%{kmodinstdir_postfix}
    install -dm 755 $d
    install -pm 755 _kmod_build_${kv%%___*}/modules/*.ko $d
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.4-1.2
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.4-1.1
- rebuild for F12 release kernel

* Mon Nov 09 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.17.4-1
- new upstream release
- now builds on F12, too

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.3-1.5
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.3-1.4
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.3-1.3
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.3-1.2
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.3-1.1
- rebuild for new kernels

* Sat Jul 04 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.17.3-1
- update to 0.17.3

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.23
- rebuild for new kernels

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.22
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.21
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.20
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.19
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.18
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.17
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.16
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-3.15
- rebuild for new kernels

* Tue Mar 31 2009 Felix Kaechele <felix at fetzig dot org> - 0.17.2-3.14
- fixes for 2.6.29

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-2.14
- rebuild for new F11 features

* Sun Mar 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.14
- rebuild for new kernels

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.13
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.12
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.11
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.10
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.9
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.8
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.7
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.6
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.5
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.4
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.3
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.2
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-1.1
- rebuild for latest Fedora kernel;

* Tue Nov 11 2008 Felix Kaechele <felix at fetzig dot org> - 0.17.2-1
- 0.17.2

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-0.1.rc1.4
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-0.1.rc1.3
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-0.1.rc1.2
- rebuild for latest rawhide kernel

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.17.2-0.1.rc1.1
- rebuild for latest rawhide kernel

* Wed Oct 15 2008 Felix Kaechele <felix at fetzig dot org> - 0.17.2-0.1.rc1
- update to new upstream prerelease due to kernel incompatibilities

* Fri Oct 10 2008 Felix Kaechele <felix at fetzig dot org> - 0.17.1-4.2
- patch for changed include path of newer kernels added

* Fri Oct 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.17.1-3.2
- rebuild for rpm fusion

* Wed Oct 01 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.17.1-2.2
- rebuild for new kernels

* Sun Sep 27 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.17.1-1.2
- temporary disable ppc due to http://bugzilla.kernel.org/show_bug.cgi?id=11143

* Sun Sep 07 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.17.1-1.1
- 0.17.1.

* Sat Aug 16 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.17.0-0.9.rc1
- rebuild for new kernels

* Thu Jul 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.17.0-8
- rebuild for new Fedora kernels

* Tue Jul 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.17.0-7
- rebuild for new Fedora kernels

* Wed Jul 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.17.0-6
- rebuild for new Fedora kernels

* Fri Jun 13 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.17.0-5
- rebuild for new Fedora kernels

* Fri Jun 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.17.0-4
- rebuild for new Fedora kernels

* Thu May 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.17.0-3
- rebuild for new Fedora kernels

* Sun May  4 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.17.0-0.2.rc1
- 0.17.0-rc1.

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.16.4-30
- build for f9

* Sun Feb 10 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.16.4-2
- adjustments for akmods

* Tue Feb  5 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.16.4-1
- 0.16.4, 2.6.23+ patch applied upstream.
- Drop WSS patch, it no longer applies.
- Prune pre-0.16.0 changelog entries.

* Sun Dec  9 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.3-10
- Convert to use new RPMFusion kmod setup.

* Mon Dec  3 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23.8-63.fc8.

* Sat Nov 10 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23.1-49.fc8.

* Wed Oct 31 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.3-6
- Don't run depmod during build even if System.map is available.
- Run "make install" in verbose mode.
- Build for kernel 2.6.23.1-42.fc8.

* Thu Oct 18 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23.1-23.fc8.

* Sat Oct  6 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23-0.220.rc9.git2.fc8.

* Tue Sep 25 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23-0.202.rc8.fc8.

* Wed Sep 19 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23-0.187.rc6.git7.fc8.

* Tue Sep 18 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23-0.186.rc6.git7.fc8.

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.3-5
- 0.16.3, build for kernel 2.6.23-0.124.rc3.git2.fc8.
- Fix build with recent 2.6.23 rc kernels.
- Use ExcludeArch instead of ExclusiveArch.
- License: GPLv2+

* Wed Jul 25 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.23-0.45.rc0.git16.fc8.

* Sat Jul 21 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.3-0.6.rc2
- Restore ExclusiveArch, build for kernel 2.6.23-0.41.rc0.git14.fc8.

* Sat Jul 21 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.3-0.5.rc2
- 0.16.3-rc2.
- Test build without ExclusiveArch for kernel 2.6.23-0.35.rc0.git6.fc8.

* Wed Jul 11 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.3-0.1.rc1
- 0.16.3-rc1, build for kernel 2.6.22-8.fc8.
- Bring up to date with current Rawhide kernel archs and variants.

* Sat May 12 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.21-1.3149.fc7.

* Mon May  7 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.2-5
- 0.16.2, build for kernel 2.6.21-1.3141.fc7.

* Thu Apr 26 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.2-0.1.rc2
- 0.16.2-rc2, build for kernel 2.6.20-1.3104.fc7.

* Fri Apr 20 2007 Ville Skyttä <ville.skytta at iki.fi>
- Rebuild for kernel 2.6.20-1.3094.fc7.

* Wed Apr  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.2-0.1.rc1
- 0.16.2-rc1, build for kernel 2.6.20-1.3040.fc7.
- Update kmodtool to 0.10.13.

* Mon Mar 19 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.1-7
- Drop OSS default patch, making ALSA the default now; users who need
  OSS should use the audio_driver=oss option of the em8300 module.
- Use upstream 2.6.21/ALSA patch.
- Build for kernel 2.6.20-1.2997.fc7, including ppc64.

* Sun Mar  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.1-6
- Re-enable i586 and i686.
- Build for kernel 2.6.20-1.2962.fc7.

* Thu Mar  1 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.1-5
- 0.16.1, build for kernel 2.6.20-1.2953.fc7.
- Exclude i*86 until #229489 is fixed.

* Sat Feb 24 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.1-0.5.rc2
- 0.16.1-rc2 + patch for post-2.6.20 ALSA changes.
- Update kmodtool to 0.10.12.
- Build for kernel 2.6.20-1.2942.fc7.

* Tue Feb  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.0-10
- Adjust to current Rawhide arch-variant combos (kdump, xen, debug).

* Tue Feb  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.16.0-6
- Patch for kernel 2.6.20 (David van Vyfeyken), build for 2.6.20-1.2922.fc7.

* Mon Dec 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.16.0-5
- 0.16.0, build for kernel 2.6.18-1.2868.fc6.
