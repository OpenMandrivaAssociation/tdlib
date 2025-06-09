%global debug_package %{nil} 

# set to nil when packaging a release, 
# or the long commit tag for the specific git branch

# use the commit tag when they update the version in README.md because
# there doesn't appear to be anyone creating tags anymore
%define commit_tag e894536b2f46caad93f997448d2daff9431b19dd

# When using a commit_tag (i.e. not nil) add a commit date 
# decoration ~0.yyyyMMdd. to Version number 
%define commit_date ~0.20250527

Name:           tdlib
Version:        1.8.50%{?commit_date}
Release:        1
Summary:        Cross-platform library for building Telegram clients
Group:          Development
License:        BSL-1.0
URL:            https://core.telegram.org/tdlib

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Source0:        https://github.com/%name/td/archive/%{commit_tag}.tar.gz#/%name-%version.tar.gz
%else
Source0:        https://github.com/%name/td/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE=Release -DTD_ENABLE_JNI:BOOL=OFF -DTD_ENABLE_DOTNET:BOOL=OFF

# mitigate the incorrect property set here (probably a conditional for the IPO check is more ideal):
# https://github.com/tdlib/td/blob/e894536b2f46caad93f997448d2daff9431b19dd/CMakeLists.txt#L45
BuildOption:    -DCMAKE_INTERPROCEDURAL_OPTIMIZATION:BOOL=ON

BuildRequires:  gperf
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)

%description
TDLib (Telegram Database library) is a cross-platform library for building Telegram clients. 
It can be easily used from almost any programming language.

%package devel
Summary:        Development files for %name
Requires:       %name = %version

%description devel
Development files for TDLib

%package static
Summary:        Static libraries for %name
Requires:       %name = %version
Requires:       %name-devel = %version

%description static
Static libraries for %name

%files
%license LICENSE_1_0.txt
%doc  README.md
%{_libdir}/libtd*.so.*

%files static
%{_libdir}/*.a

%files devel
%{_includedir}/td
%{_libdir}/*.so
%{_libdir}/cmake/Td
%{_libdir}/pkgconfig/td*.pc

