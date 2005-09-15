#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_zd1211_ver	0.0.1
%define		_zd1211_name	zd1211
%define		_rel		2
Summary:	Linux driver for WLAN cards based on zd1211
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie zd1211
Name:		kernel-net-zd1211
Version:	%{_zd1211_ver}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
License:	GPL v2
Source0:	%{_zd1211_name}.tar.gz
# Source0-md5:	23f9e42f7930ae1189016f5081e7c76b
URL:		http://zd1211.sourceforge.net/
%if %{with kernel}
BuildRequires:	gawk
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel}
BuildRequires:	rpmbuild(macros) >= 1.153
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

%build
# kernel module(s)
cat src/zddevlist | gawk -f src/zddevlist.awk > src/zddevlist.h
cd src
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/include/linux/version.h include/linux/version.h
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		M=$PWD O=$PWD \
		CC="%{__cc}" CPP="%{__cpp}" \
		%{?with_verbose:V=1}
	for i in zd1211_mod; do
		mv $i{,-$cfg}.ko
	done
done

%install
rm -rf $RPM_BUILD_ROOT

cd src

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/usb/net
for i in zd1211_mod; do
	install $i-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/$i.ko
done
%if %{with smp} && %{with dist_kernel}
for i in zd1211_mod; do
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
