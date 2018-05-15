Summary:		Wireless daemon for Linux
Name:			iwd
Version:		0.2
Release:		1
License:		LGPLv2+
URL:			https://lists.01.org/mailman/listinfo/iwd
Source0:		https://www.kernel.org/pub/linux/network/wireless/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	readline-devel
BuildRequires:	asciidoc
BuildRequires:	pkgconfig(libsystemd)
Requires:		dbus
Requires:		systemd

%description
The daemon and utilities for controlling and configuring the Wi-Fi network
hardware.

%prep
%setup -q

%build
%configure --enable-docs
%make_build

%install
%make_install
install tools/hwsim %{buildroot}%{_bindir}

%files
%doc AUTHORS README TODO ChangeLog
%license COPYING
%{_bindir}/iwctl
%{_bindir}/iwmon
%{_bindir}/hwsim
%{_libexecdir}/iwd
%{_unitdir}/iwd.service
%{_datadir}/dbus-1/system.d/iwd-dbus.conf
%{_mandir}/man1/iwmon.1*
