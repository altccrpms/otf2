%global shortname otf2
%global ver 2.0
%{?altcc_init}

# Needed for el7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{shortname}-%{version}}

Name:           %{shortname}%{?altcc_pkg_suffix}
Version:        %{ver}
Release:        1%{?dist}
Summary:        Open Trace Format 2 library

License:        BSD
URL:            http://www.vi-hps.org/projects/score-p/
Source0:        http://www.vi-hps.org/upload/packages/%{shortname}/%{shortname}-%{version}.tar.gz
Source1:        %{shortname}.module.in
# Remove jinja2
Patch0:         otf2-jinja2.patch

BuildRequires:  python2-devel
BuildRequires:  libtool
Requires:       python-jinja2
%?altcc_reqmodules
%?altcc_provide


%description
The Open Trace Format 2 (OTF2) is a highly scalable, memory efficient
event trace data format plus support library.


%package        devel
Summary:        Development files for %{shortname}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?altcc:%altcc_provide devel}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{shortname}.


%package        doc
Summary:        Development files for %{shortname}
BuildArch:      noarch
%{?altcc:%altcc_provide doc}

%description    doc
The %{name}-doc package contains documentation files for %{shortname}.


%prep
%setup -q -n %{shortname}-%{version}
%patch0 -p1 -b .jinja2
# Bundled modified jinja2 in vendor/
rm -r vendor/python/site-packages
# Remove ldflags
sed -i -s '/deps.GetLDFlags/d' src/tools/otf2_config/otf2_config.cpp


%build
%configure --disable-static --enable-shared --disable-silent-rules \
 --docdir=%{_pkgdocdir} --enable-backend-test-runs --with-platform=linux \
  %{?altcc:--with-nocross-compiler-suite=%{altcc_cc_name}}
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -name '*.la' -delete
cp -p AUTHORS ChangeLog README %{buildroot}%{_pkgdocdir}/

%{?altcc:%altcc_license}
%{?altcc:%altcc_writemodule %SOURCE1}


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{?altcc:%altcc_files -dlm %{_bindir} %{_libdir}}
%license COPYING
%{_bindir}/%{shortname}-estimator
%{_bindir}/%{shortname}-marker
%{_bindir}/%{shortname}-print
%{_bindir}/%{shortname}-snapshots
%{_bindir}/%{shortname}-template
%{_libdir}/lib%{shortname}.so.7*
%dir %{_datadir}/%{shortname}/
%{_datadir}/%{shortname}/%{shortname}.summary
%{_datadir}/%{shortname}/python
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/ChangeLog
%{_pkgdocdir}/OPEN_ISSUES
%{_pkgdocdir}/README
%exclude %{_pkgdocdir}/html
%exclude %{_pkgdocdir}/pdf
%exclude %{_pkgdocdir}/tags

%files devel
%{?altcc:%altcc_files %{_includedir}}
%{_bindir}/%{shortname}-config
%{_includedir}/%{shortname}/
%{_libdir}/lib%{shortname}.so

%files doc
%{?altcc:%altcc_files -dl}
%license COPYING
%dir %{_pkgdocdir}
%{_pkgdocdir}/examples/
%{_pkgdocdir}/html/
%{_pkgdocdir}/pdf/
%{_pkgdocdir}/tags/


%changelog
* Thu Apr 14 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0-1
- Update to 2.0

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
