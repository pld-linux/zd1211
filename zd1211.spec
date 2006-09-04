#
#TODO
#- udev rules

# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_zd1211_ver	0.0.2
%define		_zd1211_name	zd1211-driver-r83
%define		_rel		2
Summary:	Linux driver for WLAN cards based on zd1211
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie zd1211
Name:		kernel-net-zd1211
Version:	%{_zd1211_ver}
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://zd1211.ath.cx/download/%{_zd1211_name}.tgz
# Source0-md5:	a5751f0e6f1f368689077fa7758a4932
Patch0:		%{name}-build.patch
URL:		http://zd1211.ath.cx/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
%{?with_dist_kernel:%requires_releq_kernel_up}
BuildRequires:	rpmbuild(macros) >= 1.153
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on zd1211.

This package contains Linux UP module.

%description -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie
zd1211.

Ten pakiet zawiera modu³ j±dra Linuksa UP.

%package -n kernel-smp-net-zd1211
Summary:	Linux SMP driver for WLAN cards based on zd1211
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych opartych na uk³adzie zd1211
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel-smp}

%description -n kernel-smp-net-zd1211
This is a Linux driver for WLAN cards based on zd1211.

This package contains Linux SMP module.

%description -n kernel-smp-net-zd1211 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie
zd1211.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{_zd1211_name}
#%patch0 -p1

%build
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
    fi
    for t in zd1211 zd1211b; do
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		`[ "$t" = "zd1211" ] && echo ZD1211REV_B=0 || echo ZD1211REV_B=1` \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

		for i in $t; do
			mv $i{,-$cfg}.ko
		done
    done
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/usb/net
for i in zd1211 zd1211b; do
	install $i-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/$i.ko
done
%if %{with smp} && %{with dist_kernel}
for i in zd1211 zd1211b; do
	install $i-smp.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/$i.ko
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post -n kernel-smp-net-zd1211
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-zd1211
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-zd1211
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/*.ko*
%endif
