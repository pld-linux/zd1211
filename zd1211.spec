#TODO
# -  udev rules
# - spec fs name
#
#INFO
# - Development zd112 is dormant. Please use zd1211rw instead,
#   see http://zd1211.ath.cx/wiki/DriverRewrite
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	grsec_kernel	# build for kernel-grsecurity
#
#
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
#
%define		_zd1211_ver	0.0.2
%define		_zd1211_name	zd1211-driver-r85
%define		_rel	55
Summary:	Linux driver for USB WLAN cards based on zd1211
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych USB opartych na uk³adzie zd1211
Name:		zd1211
Version:	%{_zd1211_ver}
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://zd1211.ath.cx/download/%{_zd1211_name}.tgz
# Source0-md5:	51691a15137fbc35515a630d45d03352
Patch0:		kernel-net-%{name}-build.patch
URL:		http://zd1211.ath.cx/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
Requires(post,postun):	/sbin/depmod
Requires:	zd1211-firmware
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on zd1211.

%description -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie
zd1211.

%description -l de
Linux Kernel Treiber für WLAN Netzwerkkarten zd1211.

%package -n kernel%{_alt_kernel}-net-%{name}
Summary:	Linux kernel module for WLAN cards based on zd1211 
Summary(de):	Linux Kernel Modul für WLAN Netzwerkkarten zd1211
Summary(pl):	Modu³ j±dra Linuksa dla kart WLAN na zd1211
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-net-%{name}
This package contains Linux kernel drivers for the WLAN cards based on zd1211.

%description -n kernel%{_alt_kernel}-net-%{name} -l de
Dieses Paket enthält Linux Kernel Treiber für WLAN Netzwerkkarten zd1211.

%description -n kernel%{_alt_kernel}-net-%{name} -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa dla kart WLAN na zd1211.

%package -n kernel%{_alt_kernel}-smp-net-%{name}
Summary:	Linux SMP kernel module for the WLAN cards based on zd1211.
Summary(de):	Linux SMP Kernel Modul für WLAN Netzwerkkarten zd1211
Summary(pl):	Modu³ j±dra Linuksa SMP dla kart WLAN na zd1211
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-smp-net-%{name}
This package contains Linux SMP kernel drivers for the WLAN cards based on zd1211.

%description -n kernel%{_alt_kernel}-smp-net-%{name} -l de
Dieses Paket enthält Linux SMP Kernel Treiber für WLAN Netzwerkkarten zd1211.

%description -n kernel%{_alt_kernel}-smp-net-%{name} -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa SMP dla kart WLAN opartych na uk³adzie zd1211.

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

%post	-n kernel%{_alt_kernel}-smp-net-%{name}
%depmod	%{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-%{name}
%depmod	%{_kernel_ver}smp

%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{name}.conf
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/*.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}smp/%{name}.conf
%endif
