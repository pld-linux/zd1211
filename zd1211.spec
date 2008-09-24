#
#TODO
# -  udev rules
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

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		zd1211_name	zd1211-driver-r85
%define		rel		65
%define		pname	zd1211
Summary:	Linux driver for USB WLAN cards based on zd1211
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych USB opartych na układzie zd1211
Name:		%{pname}%{_alt_kernel}
Version:	0.0.2
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://zd1211.ath.cx/download/%{zd1211_name}.tgz
# Source0-md5:	51691a15137fbc35515a630d45d03352
Patch0:		kernel-net-%{pname}-build.patch
Patch1:		%{pname}-3410.patch
URL:		http://zd1211.ath.cx/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
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
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}(vermagic) = %{_kernel_ver}}
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

%package -n kernel%{_alt_kernel}-smp-net-%{pname}
Summary:	Linux SMP kernel module for the WLAN cards based on zd1211
Summary(de.UTF-8):	Linux SMP Kernel Modul für WLAN Netzwerkkarten zd1211
Summary(pl.UTF-8):	Moduł jądra Linuksa SMP dla kart WLAN na zd1211
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-smp(vermagic) = %{_kernel_ver}}
Requires:	module-init-tools >= 3.2.2-2
Requires:	zd1211-firmware

%description -n kernel%{_alt_kernel}-smp-net-%{pname}
This package contains Linux SMP kernel drivers for the WLAN cards
based on zd1211.

%description -n kernel%{_alt_kernel}-smp-net-%{pname} -l de.UTF-8
Dieses Paket enthält Linux SMP Kernel Treiber für WLAN Netzwerkkarten
zd1211.

%description -n kernel%{_alt_kernel}-smp-net-%{pname} -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa SMP dla kart WLAN opartych
na układzie zd1211.

%prep
%setup -q -n %{zd1211_name}
%patch0 -p1
%patch1 -p1

%build
%build_kernel_modules -m zd1211

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m zd1211 -d kernel/drivers/usb/net

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{pname}
%depmod	%{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{pname}
%depmod	%{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-%{pname}
%depmod	%{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-%{pname}
%depmod	%{_kernel_ver}smp

%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{pname}.conf
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/*.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}smp/%{pname}.conf
%endif
