# TODO: C#/mono
#
# Conditional build:
%bcond_with	java	# build Java bindings
%bcond_with	ruby	# build Ruby bindings


%include	/usr/lib/rpm/macros.perl
Summary:	Redland RDF Application Framework Bindings
Summary(pl):	Wi±zania szkieletu aplikacji Redland RDF
Name:		redland-bindings
Version:	0.9.18.1
Release:	1
License:	LGPL v2.1 or GPL v2 or MPL 1.1
Group:		Libraries
Source0:	http://www.redland.opensource.ac.uk/dist/source/%{name}-%{version}.tar.gz
# Source0-md5:	19f99c04da51705e8b1db5c969151af3
Patch0:		%{name}-install.patch
URL:		http://www.redland.opensource.ac.uk/bindings/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.7
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libtool
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	php-devel
BuildRequires:	python-devel
BuildRequires:	redland-devel >= 0.9.17
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	ruby
BuildRequires:	swig >= 1.3.10
BuildRequires:	tcl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')

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
Requires:	%{name} = %{version}-%{release}
Requires:	jre

%description -n java-redland
Java bindings for Redland RDF library.

%description -n java-redland -l pl
Interfejs Javy do biblioteki Redland RDF.

%package -n perl-RDF-Redland
Summary:	Perl bindings for Redland RDF library
Summary(pl):	Perlowy interfejs do biblioteki Redland RDF
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-RDF-Redland
Perl bindings for Redland RDF library.

%description -n perl-RDF-Redland -l pl
Perlowy interfejs do biblioteki Redland RDF.

%package -n php-redland
Summary:	PHP bindings for Redland RDF library
Summary(pl):	Interfejs PHP do biblioteki Redland RDF
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php-common

%description -n php-redland
PHP bindings for Redland RDF library.

%description -n php-redland -l pl
Interfejs PHP do biblioteki Redland RDF.

%package -n python-redland
Summary:	Python bindings for Redland RDF library
Summary(pl):	Pythonowy interfejs do biblioteki Redland RDF
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python

%description -n python-redland
Python bindings for Redland RDF library.

%description -n python-redland -l pl
Pythonowy interfejs do biblioteki Redland RDF.

%if %{with ruby}
%package -n ruby-redland
Summary:	Ruby bindings for Redland RDF library
Summary(pl):	Interfejs jêzyka Ruby do biblioteki Redland RDF
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ruby

%description -n ruby-redland
Ruby bindings for Redland RDF library.

%description -n ruby-redland -l pl
Interfejs jêzyka Ruby do biblioteki Redland RDF.
%endif

%package -n tcl-redland
Summary:	Tcl bindings for Redland RDF library
Summary(pl):	Interfejs Tcl do biblioteki Redland RDF
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	tcl

%description -n tcl-redland
Tcl bindings for Redland RDF library.

%description -n tcl-redland -l pl
Interfejs Tcl do biblioteki Redland RDF.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	%{?with_java:--with-java --with-jdk=%{_libdir}/java jdkdir=%{_libdir}/java} \
	--with-perl \
	--with-php \
	--with-python \
	%{?with_ruby:--with-ruby} \
	--with-tcl

#	--with-ecma-cli=mono  -- TODO

%{__make} \
	MAKE_PL_OPTS='INSTALLDIRS=vendor OPTIMIZE="%{rpmcflags}"' \
	javalibdir=%{_libdir}/java

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	javalibdir=%{_libdir}/java

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc docs/perl.html perl/README.txt
%dir %{perl_vendorarch}/RDF
%{perl_vendorarch}/RDF/Redland.pm
%{perl_vendorarch}/RDF/Redland
%dir %{perl_vendorarch}/auto/RDF
%dir %{perl_vendorarch}/auto/RDF/Redland
%dir %{perl_vendorarch}/auto/RDF/Redland/CORE
%{perl_vendorarch}/auto/RDF/Redland/CORE/CORE.bs
%attr(755,root,root) %{perl_vendorarch}/auto/RDF/Redland/CORE/CORE.so
%{_mandir}/man3/RDF::Redland*.3pm*

%files -n php-redland
%defattr(644,root,root,755)
%doc docs/php.html
%attr(755,root,root) %{_libdir}/php/redland.so

%files -n python-redland
%defattr(644,root,root,755)
%doc docs/python.html docs/pydoc
%{py_sitedir}/RDF.py
%attr(755,root,root) %{py_sitedir}/Redland.so

%if %{with ruby}
%files -n ruby-redland
%defattr(644,root,root,755)
%doc docs/ruby.html
%attr(755,root,root) %{ruby_archdir}/redland.so
%endif

%files -n tcl-redland
%defattr(644,root,root,755)
%doc docs/tcl.html
%attr(755,root,root) %{_libdir}/tcl*/Redland.so
