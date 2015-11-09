#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Perceptual hashing library
Name:		pHash
Version:	0.9.6
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	http://www.phash.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	0572f3cfe2219a5537b78d3c5b78f84c
Patch0:		%{name}-optflags.patch
Patch1:		%{name}-link.patch
URL:		http://www.phash.org/
BuildRequires:	CImg >= 1.6.7
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw3-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmpg123-devel
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pHash is an open source software library that implements several
perceptual hashing algorithms, and provides a C-like API to use those
functions in your own programs. pHash itself is written in C++.

%package devel
Summary:	Header files for pHash library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pHash
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for pHash library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pHash.

%package static
Summary:	Static pHash library
Summary(pl.UTF-8):	Statyczna biblioteka pHash
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static pHash library.

%description static -l pl.UTF-8
Statyczna biblioteka pHash.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CPPFLAGS="-I/usr/include/CImg" \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp examples/*.cpp $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_libdir}/libpHash.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpHash.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpHash.so
%{_libdir}/libpHash.la
%{_includedir}/*.h
%{_pkgconfigdir}/pHash.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpHash.a
%endif
