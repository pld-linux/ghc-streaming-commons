#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	streaming-commons
Summary:	Common lower-level functions needed by various streaming data libraries
Summary(pl.UTF-8):	Wspólnie niskopoziomowe funkcje wymagane przez różne biblioteki obsługujące strumienie danych
Name:		ghc-%{pkgname}
Version:	0.2.1.2
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/streaming-commons
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	ce7f307504236140535e61408c000e63
URL:		http://hackage.haskell.org/package/streaming-commons
BuildRequires:	ghc >= 7.10.1
BuildRequires:	ghc-array
BuildRequires:	ghc-async
BuildRequires:	ghc-base >= 4.8
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10.2.0
BuildRequires:	ghc-network >= 2.4.0.0
BuildRequires:	ghc-process
BuildRequires:	ghc-random
BuildRequires:	ghc-stm
BuildRequires:	ghc-text
BuildRequires:	ghc-transformers
BuildRequires:	ghc-unix
BuildRequires:	ghc-zlib
%if %{with prof}
BuildRequires:	ghc-prof >= 7.10.1
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-async-prof
BuildRequires:	ghc-base-prof >= 4.8
BuildRequires:	ghc-bytestring-prof >= 0.10.2.0
BuildRequires:	ghc-network-prof >= 2.4.0.0
BuildRequires:	ghc-process-prof
BuildRequires:	ghc-random-prof
BuildRequires:	ghc-stm-prof
BuildRequires:	ghc-text-prof
BuildRequires:	ghc-transformers-prof
BuildRequires:	ghc-unix-prof
BuildRequires:	ghc-zlib-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-array
Requires:	ghc-async
Requires:	ghc-base >= 4.8
Requires:	ghc-bytestring >= 0.10.2.0
Requires:	ghc-network >= 2.4.0.0
Requires:	ghc-process
Requires:	ghc-random
Requires:	ghc-stm
Requires:	ghc-text
Requires:	ghc-transformers
Requires:	ghc-unix
Requires:	ghc-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Provides low-dependency functionality commonly needed by various
streaming data libraries, such as conduit and pipes.

%description -l pl.UTF-8
Ta biblioteka zapewnia niskopoziomową funkcjonalność wymaganą przez
różne biblioteki obsługujące strumienie danych, jak przewody i potoki.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-async-prof
Requires:	ghc-base-prof >= 4.8
Requires:	ghc-bytestring-prof >= 0.10.2.0
Requires:	ghc-network-prof >= 2.4.0.0
Requires:	ghc-process-prof
Requires:	ghc-random-prof
Requires:	ghc-stm-prof
Requires:	ghc-text-prof
Requires:	ghc-transformers-prof
Requires:	ghc-unix-prof
Requires:	ghc-zlib-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/Builder
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/Builder/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/Builder/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Network/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Network/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Process
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Process/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Process/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Zlib
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Zlib/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Zlib/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Encoding
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Encoding/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Encoding/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Unsafe
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Unsafe/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Unsafe/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/ByteString/Builder/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Network/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Process/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/Zlib/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Encoding/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Internal/Unsafe/*.p_hi
%endif
