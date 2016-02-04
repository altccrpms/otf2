# Needed for el7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           otf2
Version:        1.5.1
Release:        4%{?dist}
Summary:        Open Trace Format 2 library

License:        BSD
URL:            http://www.vi-hps.org/projects/score-p/
Source0:        http://www.vi-hps.org/upload/packages/%{name}/%{name}-%{version}.tar.gz
# Remove jinja2
Patch0:         otf2-jinja2.patch
# Fix AC_CONFIG_MACRO_DIR and remove $(srcdir) from TESTS
Patch1:         otf2-autoconf.patch

BuildRequires:  python2-devel
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  autoconf >= 2.69
%else
BuildRequires:  autoconf268
%endif
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
%if 0%{?fedora} || 0%{?rhel} >= 7
%patch1 -p1 -b .autoconf
%endif
# Bundled modified jinja2 in vendor/
rm -rf vendor/python/site-packages
%if 0%{?fedora} || 0%{?rhel} >= 7
for d in . build-backend build-frontend
%else
# autoconf 2.68 chokes on build-* configs
for d in .
%endif
do
  cd $d
%if 0%{?fedora} || 0%{?rhel} >= 7
  autoreconf -f -i -v
%else
  autoreconf268 -f -i -v
%endif
  cd -
done
# Remove ldflags
sed -i -s '/deps.GetLDFlags/d' src/tools/otf2_config/otf2_config.cpp


%build
%configure --disable-static --enable-shared --disable-silent-rules \
 --docdir=%{_pkgdocdir} --enable-backend-test-runs --with-platform=linux
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
cp -p AUTHORS ChangeLog README %{buildroot}%{_pkgdocdir}/
%if 0%{?rhel} && 0%{?rhel} < 7
cp -p COPYING %{buildroot}%{_pkgdocdir}/
%endif


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%if 0%{?fedora} || 0%{?rhel} >= 7
%license COPYING
%endif
%{_bindir}/%{name}-estimator
%{_bindir}/%{name}-marker
%{_bindir}/%{name}-print
%{_bindir}/%{name}-snapshots
%{_bindir}/%{name}-template
%{_libdir}/lib%{name}.so.5*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/%{name}.summary
%{_datadir}/%{name}/python
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/ChangeLog
%if 0%{?rhel} && 0%{?rhel} < 7
%{_pkgdocdir}/COPYING
%endif
%{_pkgdocdir}/README
%exclude %{_pkgdocdir}/html
%exclude %{_pkgdocdir}/pdf
%exclude %{_pkgdocdir}/tags

%files devel
%{_bindir}/%{name}-config
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%files doc
%if 0%{?fedora} || 0%{?rhel} >= 7
%license COPYING
%endif
%dir %{_pkgdocdir}
%if 0%{?rhel} && 0%{?rhel} < 7
%{_pkgdocdir}/COPYING
%endif
%{_pkgdocdir}/examples/
%{_pkgdocdir}/html/
%{_pkgdocdir}/pdf/
%{_pkgdocdir}/tags/


%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 13 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.1-2
- BR autoconf268 on el6 and use it
- Do not apply autoconf patch and only autoreconf top level on el6
- Fixup doc install

* Wed Feb 11 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.1-1
- Update to 1.5.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Orion Poplawski <orion@cora.nwra.com> - 1.4-2
- Remove ldflags output from otf2-config

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
