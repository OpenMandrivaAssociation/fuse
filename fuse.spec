%define major 3
%define minor 4
%define libname %mklibname %{name}3
%define devname %mklibname %{name}3 -d
%define static %mklibname %{name}3 -d -s
# https://github.com/libfuse/libfuse/issues/198
# gcc lto not supported yet, but doesn't seem to affect clang
#define _disable_lto 1

Summary:	Interface for userspace programs to export a virtual filesystem to the kernel
Name:		fuse
Version:	3.17.3
Release:	1
License:	GPLv2+
Group:		System/Base
Url:		https://github.com/libfuse/libfuse
Source0:	https://github.com/libfuse/libfuse/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	meson
BuildRequires:	pkgconfig(libudev)

%description
FUSE (Filesystem in USErspace) is a simple interface for userspace
programs to export a virtual filesystem to the linux kernel.  FUSE
also aims to provide a secure method for non privileged users to
create and mount their own filesystem implementations.

%package -n %{libname}
Summary:	Libraries for fuse
Group:		System/Libraries
License:	LGPLv2+
Obsoletes:	%{mklibname %{name}3 %{major}} < %{EVRD}

%description -n %{libname}
Libraries for fuse.

%package -n %{devname}
Summary:	Header files and development libraries for libfuse2
Group:		Development/C
License:	LGPLv2+
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Header files and development libraries for fuse.

%package -n %{static}
Summary:	Static libraries for fuse
Group:		Development/C
License:	LGPLv2+
Provides:	%{name}-static-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{static}
Static libraries for fuse.

%prep
%autosetup -p1
# udevrulesdir is specified because it's misdetected when
# crosscompiling.
%meson -Duseroot=false \
	-Db_lto=true \
%if %{cross_compiling}
	-Dudevrulesdir=%{_udevrulesdir}
%endif

%build
%meson_build

%install
%meson_install

rm -rf %{buildroot}%{_sysconfdir}/rc.d/init.d %{buildroot}%{_sysconfdir}/udev/rules.d
rm -rf %{buildroot}%{_sysconfdir}/init.d

%files
%config(noreplace) %{_sysconfdir}/fuse.conf
%{_udevrulesdir}/99-fuse3.rules
%attr(4755,root,root) %{_bindir}/fusermount3
%{_sbindir}/mount.fuse3
%doc %{_mandir}/man1/fusermount3.1*
%doc %{_mandir}/man8/mount.fuse3.8*

%files -n %{libname}
%{_libdir}/libfuse3.so.%{major}*
%{_libdir}/libfuse3.so.%{minor}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
