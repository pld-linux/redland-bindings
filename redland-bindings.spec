# TODO:
# - C#/mono
#
# Conditional build:
%bcond_with	java	# build Java bindings
%bcond_without	ruby	# don't build Ruby bindings
%bcond_with	php4	# build PHP4 bindings (default: PHP5)
%bcond_with	tcl85	# use tcl8.5 dirs
#
%include	/usr/lib/rpm/macros.perl
Summary:	Redland RDF Application Framework Bindings
Summary(pl):	Wi±zania szkieletu aplikacji Redland RDF
Name:		redland-bindings
Version:	1.0.2.1
Release:	2
License:	LGPL v2.1+ or GPL v2+ or Apache v2
Group:		Libraries
Source0:	http://librdf.org/dist/source/%{name}-%{version}.tar.gz
# Source0-md5:	16fdb1f862ac08136d786aca7f75c80a
Patch0:		%{name}-install.patch
Patch1:		%{name}-py_sitescriptdir.patch
URL:		http://librdf.org/bindings/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.7
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libtool
BuildRequires:	perl-devel >= 1:5.8.0
%if %{with php4}
BuildRequires:	php4-devel
BuildRequires:	php4-cli
%else
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	php-cli >= 3:5.0.0
%endif
BuildRequires:	python-devel
BuildRequires:	redland-devel >= 1.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with ruby}
BuildRequires:	ruby
BuildRequires:	ruby-devel
%endif
BuildRequires:	swig >= 1.3.10
%if %{with tcl85}
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tcl-devel < 8.6
%else
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	tcl-devel < 8.5
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define		ruby_libdir	%(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
%if %{with tcl85}
%define		tcldir	%{_libdir}/tcl8.5
%else
%define		tcldir	%{_libdir}/tcl8.4
%endif
%define		phpdir	%(php-config --extension-dir 2>/dev/null)

%description
Redland is a library that provides a high-level interface for the
Resource Description Framework (RDF) allowing the RDF graph to be
parsed from XML, stored, queried and manipulated. Redland implements
each of the RDF concepts in its own class via an object based API,
reflected into the language APIs, currently C#, Java, Perl, PHP,
Python, Ruby and Tcl. Several classes providing functionality such as
for parsers, storage are built as modules that can be loaded at
compile or run-time as required.

%description -l pl
Redland to biblioteka dostarczaj±ca wysokopoziomowy interfejs dla
szkieletu opisu zasobów (RDF - Resource Description Framework),
umo¿liwiaj±ca na przetwarzanie grafów XML z RDF, przechowywanie,
odpytywanie i obrabianie ich. Redland implementuje wszystkie idee RDF
we w³asnych klasach poprzez API oparte na obiektach, maj±cych
odzwierciedlenie w API dla poszczególnych jêzyków - aktualnie C#, Java
Perl, PHP, Python, Ruby i Tcl. Kilka klas dostarczaj±cych
funkcjonalno¶æ dla parserów i przechowywania danych jest budowana jako
modu³y, które mog± byæ wczytywane w czasie kompilacji lub dzia³ania
programu w razie potrzeby.

%package -n java-redland
Summary:	Java bindings for Redland RDF library
Summary(pl):	Interfejs Javy do biblioteki Redland RDF
Group:		Libraries
Requires:	jre

%description -n java-redland
Java bindings for Redland RDF library.

%description -n java-redland -l pl
Interfejs Javy do biblioteki Redland RDF.

%package -n perl-RDF-Redland
Summary:	Perl bindings for Redland RDF library
Summary(pl):	Perlowy interfejs do biblioteki Redland RDF
Group:		Development/Languages/Perl

%description -n perl-RDF-Redland
Perl bindings for Redland RDF library.

%description -n perl-RDF-Redland -l pl
Perlowy interfejs do biblioteki Redland RDF.

%package -n php4-redland
Summary:	PHP bindings for Redland RDF library
Summary(pl):	Interfejs PHP do biblioteki Redland RDF
Group:		Libraries
Requires:	php4-common

%description -n php4-redland
PHP bindings for Redland RDF library.

%description -n php4-redland -l pl
Interfejs PHP do biblioteki Redland RDF.

%package -n php-redland
Summary:	PHP bindings for Redland RDF library
Summary(pl):	Interfejs PHP do biblioteki Redland RDF
Group:		Libraries
%{?requires_php_extension}

%description -n php-redland
PHP bindings for Redland RDF library.

%description -n php-redland -l pl
Interfejs PHP do biblioteki Redland RDF.

%package -n python-redland
Summary:	Python bindings for Redland RDF library
Summary(pl):	Pythonowy interfejs do biblioteki Redland RDF
Group:		Libraries/Python
%pyrequires_eq	python

%description -n python-redland
Python bindings for Redland RDF library.

%description -n python-redland -l pl
Pythonowy interfejs do biblioteki Redland RDF.

%package -n ruby-redland
Summary:	Ruby bindings for Redland RDF library
Summary(pl):	Interfejs jêzyka Ruby do biblioteki Redland RDF
Group:		Libraries
Requires:	ruby

%description -n ruby-redland
Ruby bindings for Redland RDF library.

%description -n ruby-redland -l pl
Interfejs jêzyka Ruby do biblioteki Redland RDF.

%package -n tcl-redland
Summary:	Tcl bindings for Redland RDF library
Summary(pl):	Interfejs Tcl do biblioteki Redland RDF
Group:		Libraries
%if %{with tcl85}
Requires:	tcl >= 8.5
Requires:	tcl < 8.6
%else
Requires:	tcl >= 8.4
Requires:	tcl < 8.5
%endif

%description -n tcl-redland
Tcl bindings for Redland RDF library.

%description -n tcl-redland -l pl
Interfejs Tcl do biblioteki Redland RDF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	%{?with_java:--with-java --with-jdk=%{_libdir}/java jdkdir=%{_libdir}/java} \
	--with-perl \
	--with-php=%{_bindir}/php%{?with_php4:4}.cli \
	--with-python \
	%{?with_ruby:--with-ruby} \
	--with-tcl

#	--with-ecma-cli=mono  -- TODO

%{__make} \
	MAKE_PL_OPTS='INSTALLDIRS=vendor OPTIMIZE="%{rpmcflags}"' \
	javalibdir=%{_libdir}/java \
	pythondir=%{py_sitedir} \
	tcldir=%{tcldir}

%if %{with ruby}
cd ruby
rdoc --op ../rdoc
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	javalibdir=%{_libdir}/java \
	pythondir=%{py_sitedir} \
	tcldir=%{tcldir}

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/*.py

%{?with_java:rm -f $RPM_BUILD_ROOT%{_libdir}/java/librdf-java.la}

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/php%{?with_php4:4}/conf.d,%{phpdir}}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/php%{?with_php4:4}/conf.d/redland.ini
; Enable redland bindings module
extension=redland.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post -n php%{?with_php4:4}-redland
[ ! -f /etc/apache/conf.d/??_mod_php.%{?with_php4:4}conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php%{?with_php4:4}.conf ] || %service -q httpd restart

%postun -n php%{?with_php4:4}-redland
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php%{?with_php4:4}.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php%{?with_php4:4}.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE.html NEWS.html README.html RELEASE.html TODO.html

%if %{with java}
%files -n java-redland
%defattr(644,root,root,755)
%doc docs/java.html
%{_libdir}/java/librdf-java.so*
%{_javadir}/librdf-java.jar
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
%{perl_vendorarch}/auto/RDF/Redland/CORE/CORE.bs
%attr(755,root,root) %{perl_vendorarch}/auto/RDF/Redland/CORE/CORE.so
%{_mandir}/man3/RDF::Redland*.3pm*

%files -n php%{?with_php4:4}-redland
%defattr(644,root,root,755)
%doc docs/php.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php%{?with_php4:4}/conf.d/redland.ini
%attr(755,root,root) %{phpdir}/redland.so

%files -n python-redland
%defattr(644,root,root,755)
%doc docs/python.html docs/pydoc
%{py_sitescriptdir}/RDF.py[co]
%attr(755,root,root) %{py_sitedir}/Redland.so

%if %{with ruby}
%files -n ruby-redland
%defattr(644,root,root,755)
%doc docs/ruby.html rdoc
%attr(755,root,root) %{ruby_archdir}/redland.so
%dir %{ruby_libdir}/rdf
%{ruby_libdir}/rdf/redland.rb
%{ruby_libdir}/rdf/redland
%endif

%files -n tcl-redland
%defattr(644,root,root,755)
%doc docs/tcl.html
%attr(755,root,root) %{_libdir}/tcl*/Redland.so
