Name:           flite
Version:        1.3
Release:        9%{?dist}
Summary:        Small, fast speech synthesis engine (text-to-speech)

Group:          Applications/Multimedia
License:        BSD-style
URL:            http://fife.speech.cs.cmu.edu/flite/
Source0:        http://fife.speech.cs.cmu.edu/flite/packed/%{name}-%{version}/%{name}-%{version}-release.tar.gz
Source1:        README-ALSA.txt
Patch0:         flite-1.3-sharedlibs.patch
Patch1:         flite-1.3-doc_texinfo.patch
Patch2:         flite-1.3-alsa_support.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  texi2html ed alsa-lib-devel autoconf


%description
Flite (festival-lite) is a small, fast run-time speech synthesis engine
developed at CMU and primarily designed for small embedded machines and/or
large servers. Flite is designed as an alternative synthesis engine to
Festival for voices built using the FestVox suite of voice building tools.


%package devel
Summary: Development files for flite
Group: Development/Libraries
Requires: flite = %{version}-%{release}


%description devel
Development files for Flite, a small, fast speech synthesis engine.


%prep
%setup -q -n %{name}-%{version}-release
%patch0 -p1 -b .flite-1.3-sharedlibs
%patch1 -p1 -b .flite-1.3-doc_texinfo
%patch2 -p1 -b .flite-1.3-alsa_support
cp -p %{SOURCE1} .


%build
autoconf
%configure --enable-shared --with-audio=alsa
# This package fails parallel make (thus cannot be built using "_smp_flags")
make
# Build documentation
cd doc
make flite.html


%install
rm -rf %{buildroot}
make install INSTALLBINDIR=%{buildroot}%{_bindir} INSTALLLIBDIR=%{buildroot}%{_libdir}  INSTALLINCDIR=%{buildroot}%{_includedir}/flite


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ACKNOWLEDGEMENTS README COPYING doc/html README-ALSA.txt
%{_libdir}/*.so.*
%{_bindir}/*


%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/flite


%changelog
* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-9
- Autorebuild for GCC 4.3

* Tue Nov 14 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-8
- Added comment to %%build stating why "_smp_flags" isn't used with make

* Mon Nov 13 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-7
- Modified alsa support patch file to patch "configure.in" instead of "configure"
- Added "autoconf" step to %%build
- Added BuildRequires: autoconf
- Fixed patch backup file suffixes
- Renamed patch files to a more standard format
- Moved header files from /usr/include to /usr/include/flite
- Added -p option to all cp operations (to preserve timestamps)

* Sun Nov 12 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-6
- Recreated patch to allow shared libraries to build correctly (sharedlibs.patch)
- "flite" and "flite_time" binaries now link to flite shared libraries (sharedlibs.patch)
- Simplified the documentation patch filename
- Modified patch steps in %%prep to create backup files with different suffixes
- Removed "_smp_flags" macro from %%build for all archs

* Fri Oct 20 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-5
- Modified "build" so that "_smp_flags" is only used for i386 arch

* Mon Oct 10 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-4
- Removed "_smp_flags" macro from "build" for x86_64 arch

* Tue Sep 26 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-3
- Added README-ALSA.txt (Source1)
- Removed subpackage: flite-devel-static
- Modified shared libraries patch (Patch0) to prevent building static libraries
- Renamed patch files: Patch0, Patch1

* Tue Sep 26 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-2
- Added flite 1.3 ALSA patch (Patch2) by Lukas Loehrer - thanks Anthony Green for pointing it out
- Added configure option: --with-audio=alsa
- Added BuildRequires: alsa-lib-devel

* Fri Sep 22 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-1
- Initial RPM build
