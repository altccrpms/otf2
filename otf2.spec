# Needed for el7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           otf2
Version:        1.4
Release:        1%{?dist}
Summary:        Open Trace Format 2 library

License:        BSD
URL:            http://www.vi-hps.org/projects/score-p/
Source0:        http://www.vi-hps.org/upload/packages/%{name}/%{name}-%{version}.tar.gz
# Remove jinja2
Patch0:         otf2-jinja2.patch
# Fix AC_CONFIG_MACRO_DIR and remove $(srcdir) from TESTS
Patch1:         otf2-autoconf.patch

BuildRequires:  python2-devel
# For autoreconf, etc.
BuildRequires:  libtool
Requires:       python-jinja2


%description
The Open Trace Format 2 (OTF2) is a highly scalable, memory efficient
event trace data format plus support library.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Development files for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation files for %{name}.


%prep
%setup -q
%patch0 -p1 -b .jinja2
%patch1 -p1 -b .autoconf
#sed -i -e '/front-and-backend.am/d' ./build-frontend/Makefile.am
# Bundled modified jinja2 in vendor/
rm -rf vendor/python/site-packages
for d in . build-backend build-frontend
do
  cd $d
  autoreconf -f -i -v
  cd -
done


%build
%configure --disable-static --enable-shared --disable-silent-rules \
 --docdir=%{_pkgdocdir} --enable-backend-test-runs --with-platform=linux
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/%{name}-estimator
%{_bindir}/%{name}-marker
%{_bindir}/%{name}-print
%{_bindir}/%{name}-snapshots
%{_bindir}/%{name}-template
%{_libdir}/lib%{name}.so.5*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/%{name}.summary
%{_datadir}/%{name}/python
%exclude %{_pkgdocdir}/html
%exclude %{_pkgdocdir}/pdf
%exclude %{_pkgdocdir}/tags

%files devel
%{_bindir}/%{name}-config
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%files doc
%doc COPYING
%dir %{_pkgdocdir}
%{_pkgdocdir}/html/
%{_pkgdocdir}/pdf/
%{_pkgdocdir}/tags/


%changelog
* Tue Jul 15 2014 Orion Poplawski <orion@cora.nwra.com> - 1.4-1
- Update to 1.4
- Add patch to allow running autoreconf to remove rpaths

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Orion Poplawski <orion@cora.nwra.com> - 1.2.1-4
- Move otf2-config back to -devel

* Mon Oct 21 2013 Orion Poplawski <orion@cora.nwra.com> - 1.2.1-3
- Add BR python2-devel
- Add Requires jinja2
- Exclude docs from main package
- Rebase jinja2 patch

* Wed Oct 2 2013 Orion Poplawski <orion@cora.nwra.com> - 1.2.1-2
- Fix rpath with configure change

* Wed Sep 25 2013 Orion Poplawski <orion@cora.nwra.com> - 1.2.1-1
- Initial package
