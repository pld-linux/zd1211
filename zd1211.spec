#
#TODO
# -  udev rules
# - spec vs name
#
#INFO
# - Development zd112 is dormant. Please use zd1211rw instead,
#   see http://zd1211.ath.cx/wiki/DriverRewrite
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_zd1211_ver	0.0.2
%define		_zd1211_name	zd1211-driver-r85
%define		_rel		3
Summary:	Linux driver for USB WLAN cards based on zd1211
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych USB opartych na układzie zd1211
Name:		zd1211
Version:	%{_zd1211_ver}
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://zd1211.ath.cx/download/%{_zd1211_name}.tgz
# Source0-md5:	51691a15137fbc35515a630d45d03352
Patch0:		kernel-net-%{name}-build.patch
URL:		http://zd1211.ath.cx/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.330
Requires(post,postun):	/sbin/depmod
Requires:	zd1211-firmware
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on zd1211.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
zd1211.

%description -l de.UTF-8
Linux Kernel Treiber für WLAN Netzwerkkarten zd1211.

%package -n kernel%{_alt_kernel}-net-%{name}
Summary:	Linux kernel module for WLAN cards based on zd1211 
Summary(de.UTF-8):	Linux Kernel Modul für WLAN Netzwerkkarten zd1211
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart WLAN na zd1211
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-net-%{name}
This package contains Linux kernel drivers for the WLAN cards based on zd1211.

%description -n kernel%{_alt_kernel}-net-%{name} -l de.UTF-8
Dieses Paket enthält Linux Kernel Treiber für WLAN Netzwerkkarten zd1211.

%description -n kernel%{_alt_kernel}-net-%{name} -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa dla kart WLAN na zd1211.

%prep
%setup -q -n %{_zd1211_name}
%patch0 -p1

%build
%build_kernel_modules -m zd1211

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m zd1211 -d /kernel/drivers/usb/net

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{name}
%depmod	%{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{name}
%depmod	%{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*
