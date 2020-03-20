Summary:	Wireless daemon for Linux
Name:		iwd
Version:	1.5
Release:	2
License:	LGPLv2+
URL:		https://lists.01.org/mailman/listinfo/iwd
Source0:	https://www.kernel.org/pub/linux/network/wireless/%{name}-%{version}.tar.xz
# (tpg) 2019-11-18
# ld: error: undefined symbol: floor
# >>> referenced by rrm.c:261 (src/rrm.c:261)
Patch0:		iwd-1.1-add-missing-lm.patch
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	readline-devel
BuildRequires:	asciidoc
BuildRequires:	a2x
BuildRequires:	python-docutils
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(ell) >= 0.26
Requires:	dbus
Requires:	systemd

%description
The daemon and utilities for controlling and configuring the Wi-Fi network
hardware.

%prep
%autosetup -p1
autoreconf -fiv

%build
%configure \
  --with-systemd-unitdir=%{_unitdir} \
  --enable-external-ell \
  --enable-sim-hardcoded \
  --enable-ofono \
  --enable-wired \
  --enable-hwsim \
  --enable-tools

%make_build

%install
%make_install

# (tpg) do not install it as it break existing user's network configuration
rm -rf %{buildroot}/lib/systemd/network/80-iwd.link

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-iwd.preset << EOF
enable iwd.service
EOF

# (tpg) make sure that wpa_supplicant is stop and disabled on update
%triggerin -- wpa_supplicant
systemctl disable --now wpa_supplicant.service

# (tpg) make sure that IWD is default backend and restart NM
# this may be removed or changed after wpa_supplicant go away
%triggerin -- NetworkManager
sed -i -e 's/^#wifi.backend=iwd/wifi.backend=iwd/g' /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf
sed -i -e 's/^wifi.backend=wpa_supplicant/#wifi.backend=wpa_supplicant/g' /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf
systemctl restart --quiet NetworkManager.service

%post
%systemd_post iwd.service
# (tpg) this may be removed or adapted when wpa_supplicant will go away
if [ $1 = 1 ]; then
    if [ -e /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf ]; then
	systemctl disable --now wpa_supplicant.service
	sed -i -e 's/^#wifi.backend=iwd/wifi.backend=iwd/g' /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf
	sed -i -e 's/^wifi.backend=wpa_supplicant/#wifi.backend=wpa_supplicant/g' /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf
	systemctl restart --quiet NetworkManager.service
    fi
fi

%preun
# (tpg) this may be removed or adapted when wpa_supplicant will go away
if [ $1 = 0 ]; then
    if [ $(command -v wpa_supplicant) ];
	sed -i -e 's/^#wifi.backend=iwd/wifi.backend=iwd/g' /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf
	sed -i -e 's/^wifi.backend=wpa_supplicant/#wifi.backend=wpa_supplicant/g' /usr/lib/NetworkManager/conf.d/00-wifi-backend.conf
	systemctl restart --quiet NetworkManager.service
    fi
fi

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
%{_mandir}/man5/iwd.config.5.*
%{_mandir}/man5/iwd.network.5.*
%{_mandir}/man7/iwd.debug.7.*
%{_mandir}/man8/ead.8.*
%{_mandir}/man8/iwd.8.*
