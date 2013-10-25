Name:           otf2
Version:        1.2.1
Release:        4%{?dist}
Summary:        Open Trace Format 2 library

License:        BSD
URL:            http://www.vi-hps.org/projects/score-p/
Source0:        http://www.vi-hps.org/upload/packages/%{name}/%{name}-%{version}.tar.gz
# Remove jinja2
Patch0:         otf2-jinja2.patch

BuildRequires:  python2-devel
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
find . -name configure -exec sed -i 's|sys_lib_dlsearch_path_spec=\"/lib /usr/lib $lt_ld_extra\"|sys_lib_dlsearch_path_spec=\"/lib64 /usr/lib64 /lib /usr/lib $lt_ld_extra\"|g' '{}' \; 

# Bundled modified jinja2 in vendor/
rm -rf vendor/python/site-packages
# Remove setting -rpath in otf2-config
sed -i -e '/^HARDCODE_INTO_LIBS/s/=.*/=0/' \
       -e '/^HARDCODE_LIBDIR_FLAG_C/s/=.*/=/' */configure


%build
%configure --disable-static --enable-shared --disable-silent-rules \
 --enable-backend-test-runs \
 --with-platform=linux
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
%{_bindir}/%{name}-marker
%{_bindir}/%{name}-print
%{_bindir}/%{name}-snapshots
%{_bindir}/%{name}-template
%{_libdir}/lib%{name}.so.3*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/python
%exclude %{_defaultdocdir}/%{name}/html
%exclude %{_defaultdocdir}/%{name}/pdf
%exclude %{_defaultdocdir}/%{name}/tags

%files devel
%{_bindir}/%{name}-config
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%files doc
%doc COPYING
%dir %{_defaultdocdir}/%{name}
%{_defaultdocdir}/%{name}/html/
%{_defaultdocdir}/%{name}/pdf/
%{_defaultdocdir}/%{name}/tags/


%changelog
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
