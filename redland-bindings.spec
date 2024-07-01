#
# Conditional build:
%bcond_without	lua	# don't build Lua bindings
%bcond_with	php	# don't build (any) PHP bindings
%bcond_without	ruby	# don't build Ruby bindings

%define		php_name	php%{?php_suffix}
Summary:	Redland RDF Application Framework Bindings
Summary(pl.UTF-8):	Wiązania szkieletu aplikacji Redland RDF
Name:		redland-bindings
Version:	1.0.17.1
Release:	19
License:	LGPL v2.1+ or GPL v2+ or Apache v2.0+
Group:		Libraries
Source0:	http://download.librdf.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	b13c3d0e1bf291b071aae73603e70e65
Patch0:		%{name}-py_sitescriptdir.patch
Patch1:		%{name}-php.patch
Patch2:		%{name}-sh.patch
Patch3:		%{name}-ruby.patch
URL:		http://librdf.org/bindings/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	redland-devel >= 1.0.15
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.344
%if %{with php}
BuildRequires:	%{php_name}-devel
BuildRequires:	%{php_name}-program
BuildRequires:	swig-php >= 2.0.0
%endif
%if %{with ruby}
BuildRequires:	ruby-devel
%endif
Obsoletes:	dotnet-redland
Obsoletes:	java-redland
Obsoletes:	tcl-redland
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Redland is a library that provides a high-level interface for the
Resource Description Framework (RDF) allowing the RDF graph to be
parsed from XML, stored, queried and manipulated. Redland implements
each of the RDF concepts in its own class via an object based API,
reflected into the language APIs, currently Lua, Perl, PHP, Python and
Ruby. Several classes providing functionality such as for parsers,
storage are built as modules that can be loaded at compile or run-time
as required.

%description -l pl.UTF-8
Redland to biblioteka dostarczająca wysokopoziomowy interfejs dla
szkieletu opisu zasobów (RDF - Resource Description Framework),
umożliwiająca na przetwarzanie grafów XML z RDF, przechowywanie,
odpytywanie i obrabianie ich. Redland implementuje wszystkie idee RDF
we własnych klasach poprzez API oparte na obiektach, mających
odzwierciedlenie w API dla poszczególnych języków - aktualnie Lua,
Perla, PHP, Pythona i Ruby'ego. Kilka klas dostarczających
funkcjonalność dla analizatorów i przechowywania danych jest budowana
jako moduły, które mogą być wczytywane w czasie kompilacji lub
działania programu w razie potrzeby.

%package -n lua-redland
Summary:	Lua bindings for Redland RDF library
Summary(pl.UTF-8):	Interfejs języka Lua do biblioteki Redland RDF
Group:		Development/Languages/Perl
Requires:	redland >= 1.0.15

%description -n lua-redland
Lua bindings for Redland RDF library.

%description -n lua-redland -l pl.UTF-8
Interfejs języka Lua do biblioteki Redland RDF.

%package -n perl-RDF-Redland
Summary:	Perl bindings for Redland RDF library
Summary(pl.UTF-8):	Perlowy interfejs do biblioteki Redland RDF
Group:		Development/Languages/Perl
Requires:	redland >= 1.0.15

%description -n perl-RDF-Redland
Perl bindings for Redland RDF library.

%description -n perl-RDF-Redland -l pl.UTF-8
Perlowy interfejs do biblioteki Redland RDF.

%package -n %{php_name}-redland
Summary:	PHP 5.x bindings for Redland RDF library
Summary(pl.UTF-8):	Interfejs PHP 5.x do biblioteki Redland RDF
Group:		Libraries
%{?requires_php_extension}
Requires:	redland >= 1.0.15

%description -n %{php_name}-redland
PHP 5.x bindings for Redland RDF library.

%description -n %{php_name}-redland -l pl.UTF-8
Interfejs PHP 5.x do biblioteki Redland RDF.

%package -n python-redland
Summary:	Python bindings for Redland RDF library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki Redland RDF
Group:		Libraries/Python
Requires:	python
Requires:	redland >= 1.0.15

%description -n python-redland
Python bindings for Redland RDF library.

%description -n python-redland -l pl.UTF-8
Pythonowy interfejs do biblioteki Redland RDF.

%package -n ruby-redland
Summary:	Ruby bindings for Redland RDF library
Summary(pl.UTF-8):	Interfejs języka Ruby do biblioteki Redland RDF
Group:		Libraries
Requires:	redland >= 1.0.15
%{?ruby_mod_ver_requires_eq}

%description -n ruby-redland
Ruby bindings for Redland RDF library.

%description -n ruby-redland -l pl.UTF-8
Interfejs języka Ruby do biblioteki Redland RDF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# force regeneration
%{__rm} php/{php_redland.h,redland_wrap.c}
%{__rm} perl/CORE_wrap.c

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	PYTHON="%{__python}" \
	--disable-static \
	%{?with_lua:--with-lua=lua51} \
	--with-perl \
	--with-perl-makemaker-args='INSTALLDIRS=vendor OPTIMIZE="%{rpmcflags}"' \
%if %{with php}
	PHP_CONFIG=%{_bindir}/php-config \
	--with-php=%{__php} \
%endif
	--with-python \
	%{?with_ruby:--with-ruby}

%{__make} \
	pythondir=%{py_sitedir}

%if %{with ruby}
cd ruby
rdoc --op ../rdoc
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitedir} \
	luadir=%{_libdir}/lua/5.1

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/*.py

%if %{with lua}
chmod +x $RPM_BUILD_ROOT%{_libdir}/lua/5.1/*.so
%endif
%if %{with php}
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/redland.ini
; Enable redland bindings module
extension=redland.so
EOF
# make .so executable so that rpm would add autodeps on .so files
chmod +x $RPM_BUILD_ROOT%{php_extensiondir}/*.so
%endif

rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/RDF/Redland/CORE/.packlist

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{php_name}-redland
%php_webserver_restart

%postun -n %{php_name}-redland
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog* LICENSE.html NEWS.html README.html RELEASE.html TODO.html

%if %{with lua}
%files -n lua-redland
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lua/5.1/redland.so
%endif

%files -n perl-RDF-Redland
%defattr(644,root,root,755)
%doc docs/perl.html
%dir %{perl_vendorarch}/RDF
%{perl_vendorarch}/RDF/Redland.pm
%{perl_vendorarch}/RDF/Redland
%dir %{perl_vendorarch}/auto/RDF
%dir %{perl_vendorarch}/auto/RDF/Redland
%dir %{perl_vendorarch}/auto/RDF/Redland/CORE
%attr(755,root,root) %{perl_vendorarch}/auto/RDF/Redland/CORE/CORE.so
%{_mandir}/man3/RDF::Redland*.3pm*

%if %{with php}
%files -n %{php_name}-redland
%defattr(644,root,root,755)
%doc docs/php.html
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/redland.ini
%attr(755,root,root) %{php_extensiondir}/redland.so
%endif

%files -n python-redland
%defattr(644,root,root,755)
%doc docs/python.html docs/pydoc
%{py_sitescriptdir}/RDF.py[co]
%{py_sitescriptdir}/Redland.py[co]
%attr(755,root,root) %{py_sitedir}/_Redland.so

%if %{with ruby}
%files -n ruby-redland
%defattr(644,root,root,755)
%doc docs/ruby.html rdoc
%attr(755,root,root) %{ruby_archdir}/redland.so
%dir %{ruby_rubylibdir}/rdf
%{ruby_rubylibdir}/rdf/redland.rb
%{ruby_rubylibdir}/rdf/redland
%endif
