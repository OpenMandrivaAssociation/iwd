Summary:	Wireless daemon for Linux
Name:		iwd
Version:	0.22
Release:	1
License:	LGPLv2+
URL:		https://lists.01.org/mailman/listinfo/iwd
Source0:	https://www.kernel.org/pub/linux/network/wireless/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	readline-devel
BuildRequires:	asciidoc
BuildRequires:	a2x
BuildRequires:	python-docutils
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(ell) >= 0.24
Requires:	dbus
Requires:	systemd

%description
The daemon and utilities for controlling and configuring the Wi-Fi network
hardware.

%prep
%autosetup -p1

%build
%configure \
  --with-systemd-unitdir=%{_unitdir} \
  --enable-external-ell \
  --enable-docs \
  --enable-sim-hardcoded \
  --enable-ofono \
  --enable-wired \
  --enable-hwsim \
  --enable-tools

%make_build

%install
%make_install

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-iwd.preset << EOF
enable iwd.service
EOF

%post
%systemd_post iwd.service

%files
%doc AUTHORS README TODO ChangeLog
%license COPYING
%{_prefix}/lib/modules-load.d/*.conf
%{_bindir}/iwctl
%{_bindir}/iwmon
%{_bindir}/hwsim
%{_libexecdir}/iwd
%{_libexecdir}/ead
%{_presetdir}/86-iwd.preset
%{_unitdir}/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/system-services/*.service
%{_mandir}/man1/iwmon.1*
%{_mandir}/man1/hwsim.1.*
%{_mandir}/man1/iwctl.1.*
%{_mandir}/man5/iwd.conf.5.*
%{_mandir}/man8/ead.8.*
%{_mandir}/man8/iwd.8.*
