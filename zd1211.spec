#
#TODO
# -  udev rules
#
#INFO
# - Development zd112 is dormant. Please use zd1211rw instead,
#   see http://zd1211.ath.cx/wiki/DriverRewrite, but now zd1211rw
#   have not master mode (AP mode).
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		zd1211_name	zd1211-driver-r85
%define		rel		7
%define		pname	zd1211
Summary:	Linux driver for USB WLAN cards based on zd1211
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych USB opartych na układzie zd1211
Name:		%{pname}%{_alt_kernel}
Version:	0.0.2
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	%{zd1211_name}.tar.bz2
# Source0-md5:	20569b84770f011c78b47dc4030548a5
Patch0:		%{pname}-build.patch
Patch1:		%{pname}-3410.patch
Patch2:		%{pname}-2.6.22.patch
Patch3:		%{pname}-2.6.27.patch
Patch4:		%{pname}-2.6.29.patch
Patch5:		%{pname}-2.6.30.patch
URL:		http://zd1211.ath.cx/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.27}
BuildRequires:	rpmbuild(macros) >= 1.330
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on zd1211.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
zd1211.

%description -l de.UTF-8
Linux Kernel Treiber für WLAN Netzwerkkarten zd1211.

%package -n kernel%{_alt_kernel}-net-%{pname}
Summary:	Linux kernel module for WLAN cards based on zd1211
Summary(de.UTF-8):	Linux Kernel Modul für WLAN Netzwerkkarten zd1211
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart WLAN na zd1211
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Requires:	zd1211-firmware

%description -n kernel%{_alt_kernel}-net-%{pname}
This package contains Linux kernel drivers for the WLAN cards based on
zd1211.

%description -n kernel%{_alt_kernel}-net-%{pname} -l de.UTF-8
Dieses Paket enthält Linux Kernel Treiber für WLAN Netzwerkkarten
zd1211.

%description -n kernel%{_alt_kernel}-net-%{pname} -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa dla kart WLAN na zd1211.

%prep
%setup -q -n %{zd1211_name}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%build_kernel_modules -m zd1211

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m zd1211 -d /kernel/drivers/net/usb

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{pname}
%depmod	%{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{pname}
%depmod	%{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/usb/zd1211.ko*
