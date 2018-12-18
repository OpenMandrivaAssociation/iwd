Summary:	Wireless daemon for Linux
Name:		iwd
Version:	0.13
Release:	1
License:	LGPLv2+
URL:		https://lists.01.org/mailman/listinfo/iwd
Source0:	https://www.kernel.org/pub/linux/network/wireless/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	readline-devel
BuildRequires:	asciidoc
BuildRequires:	a2x
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
Requires:	dbus
Requires:	systemd

%description
The daemon and utilities for controlling and configuring the Wi-Fi network
hardware.

%prep
%autosetup -p1

%build
%configure \
  --enable-docs \
  --enable-sim-hardcoded \
  --enable-ofono \
  --enable-wired \
  --enable-hwsim \
  --enable-tools

%make_build

%install
%make_install

%files
%doc AUTHORS README TODO ChangeLog
%license COPYING
%{_bindir}/iwctl
%{_bindir}/iwmon
%{_bindir}/hwsim
%{_libexecdir}/iwd
%{_libexecdir}/ead
%{_unitdir}/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/system-services/*.service
%{_mandir}/man1/iwmon.1*
