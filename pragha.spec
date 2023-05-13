#
# Conditional build:
%bcond_without	grilo	# playing on DLNA servers using grilo
%bcond_with	rygel	# sharing on DLNA using rygel [API 2.6, i.e. 0.20.x-0.40.x]
%bcond_without	xfce	# session management support using libxfce4ui
#
Summary:	Lightweight GTK+ music manager
Summary(pl.UTF-8):	Lekki zarządca muzyki oparty na GTK+
Name:		pragha
Version:	1.3.4
Release:	2
License:	GPL v3+
Group:		Applications/Multimedia
#Source0Download: https://github.com/pragha-music-player/pragha/releases
Source0:	https://github.com/pragha-music-player/pragha/releases/download/v%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	a50b655e6f4a4a78ce9c08d54cf0a296
URL:		https://github.com/pragha-music-player/pragha
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.8
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	gtk+3-devel >= 3.8.0
BuildRequires:	intltool
BuildRequires:	libpeas-devel >= 1.0.0
BuildRequires:	libpeas-gtk-devel >= 1.0.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel >= 3.4
BuildRequires:	taglib-devel >= 1.8
# optional, for plugins
BuildRequires:	glyr-devel >= 1.0.1
%if %{with grilo}
BuildRequires:	grilo-devel >= 0.3.0
%endif
BuildRequires:	keybinder3-devel >= 0.2.0
BuildRequires:	libcddb-devel >= 1.3.0
BuildRequires:	libcdio-devel >= 0.80
BuildRequires:	libcdio-paranoia-devel >= 0.90
BuildRequires:	libclastfm-devel >= 0.5
BuildRequires:	libmtp-devel >= 1.1.0
BuildRequires:	libnotify-devel >= 0.7.5
BuildRequires:	libsoup-devel >= 2.38
%{?with_xfce:BuildRequires:	libxfce4ui-devel >= 4.10.0}
%if %{with rygel}
# rygel-server-2.6
BuildRequires:	rygel-devel >= 0.26
%endif
BuildRequires:	totem-pl-parser-devel >= 2.26
BuildRequires:	udev-glib-devel >= 1:145
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.36
Requires:	glyr >= 1.0.1
Requires:	gtk+3 >= 3.8.0
Requires:	hicolor-icon-theme
Requires:	keybinder3 >= 0.2.0
Requires:	libcddb >= 1.3.0
Requires:	libcdio >= 0.80
Requires:	libcdio-paranoia >= 0.90
Requires:	libclastfm >= 0.5
Requires:	libmtp >= 1.1.0
Requires:	libnotify >= 0.7.5
Requires:	libpeas >= 1.0.0
Requires:	libpeas-gtk >= 1.0.0
Requires:	libsoup >= 2.38
%{?with_xfce:Requires:	libxfce4ui >= 4.10.0}
Requires:	sqlite3 >= 3.4
Requires:	taglib >= 1.8
Requires:	totem-pl-parser >= 2.26
Requires:	udev-glib >= 1:145
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pragha is a lightweight GTK+ music manager that aims to be fast,
bloat-free, and light on memory consumption. It is written completely
in C and GTK+.

Pragha is a fork of Consonance Music Manager, discontinued by the
original author.

%description -l pl.UTF-8
Pragha to lekki zarządca muzyki oparty na GTK+, stworzony z myślą o
szybkości, braku nadmiarowych opcji i niewielkim zużyciu pamięci. Jest
napisany w całości w C, z użyciem biblioteki GTK+.

Pragha to odgałęzienie projektu Consonance Music Manager, który
przestał być rozwijany przez pierwotnego autora.

%package devel
Summary:	Header file for Pragha plugins development
Summary(pl.UTF-8):	Plik nagłówkowy do tworzenia wtyczek dla zarządcy muzyki Pragha
Group:		Development/Libraries
Requires:	libpeas-devel >= 1.0.0
Requires:	libpeas-gtk-devel >= 1.0.0
# doesn't require base

%description devel
Header file for Pragha plugins development.

%description devel -l pl.UTF-8
Plik nagłówkowy do tworzenia wtyczek dla zarządcy muzyki Pragha.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_grilo:--disable-grilo-0.3} \
	%{!?with_xfce:--disable-libxfce4ui} \
	%{!?with_rygel:--disable-rygel-server-2.6} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL='install -p' \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
	--delete-original \
	--add-category=Audio \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%{__rm} $RPM_BUILD_ROOT%{_libdir}/pragha/plugins/*/*.la

# remove duplicate docs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

# unify locale names
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{ca_ES,ca}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{ko_KR,ko}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{no,nb}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database

%postun
%update_icon_cache hicolor
%update_desktop_database

%files -f %{name}.lang
%defattr(644,root,root,755)
# FIXME add AUTHORS if not empty
%doc ChangeLog COPYING FAQ NEWS README
%attr(755,root,root) %{_bindir}/pragha
%dir %{_libdir}/pragha
%dir %{_libdir}/pragha/plugins
# R: libsoup
%dir %{_libdir}/pragha/plugins/acoustid
%{_libdir}/pragha/plugins/acoustid/acoustid.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/acoustid/libacoustid.so
# R: libcddb libcdio libcdio-paranoia
%dir %{_libdir}/pragha/plugins/cdrom
%{_libdir}/pragha/plugins/cdrom/cdrom.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/cdrom/libcdrom.so
%if %{with rygel}
# R: rygel
%dir %{_libdir}/pragha/plugins/dlna
%{_libdir}/pragha/plugins/dlna/dlna.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/dlna/libdlna.so
%endif
%if %{with grilo}
# R: grilo
%dir %{_libdir}/pragha/plugins/dlna-renderer
%{_libdir}/pragha/plugins/dlna-renderer/dlna-renderer.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/dlna-renderer/libpdlnarenderer.so
%endif
# R: udev-glib
%dir %{_libdir}/pragha/plugins/devices
%{_libdir}/pragha/plugins/devices/devices.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/devices/libdevices.so
%attr(755,root,root) %{_libdir}/pragha/plugins/devices/libdeviceclient.so*
# R: libpeas
%dir %{_libdir}/pragha/plugins/gnome-media-keys
%{_libdir}/pragha/plugins/gnome-media-keys/gnome-media-keys.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/gnome-media-keys/libgnome-media-keys.so
# R: keybinder
%dir %{_libdir}/pragha/plugins/keybinder
%{_libdir}/pragha/plugins/keybinder/keybinder.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/keybinder/libkeybinder.so
# R: libclastfm
%dir %{_libdir}/pragha/plugins/lastfm
%{_libdir}/pragha/plugins/lastfm/lastfm.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/lastfm/libplastfm.so
# R: libpeas
%dir %{_libdir}/pragha/plugins/mpris2
%{_libdir}/pragha/plugins/mpris2/mpris2.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/mpris2/libmpris2.so
# R: libmtp udev-glib
%dir %{_libdir}/pragha/plugins/mtp
%{_libdir}/pragha/plugins/mtp/mtp.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/mtp/libpmtp.so
# R: libnotify
%dir %{_libdir}/pragha/plugins/notify
%{_libdir}/pragha/plugins/notify/notify.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/notify/libnotify.so
# R: udev-glib
%dir %{_libdir}/pragha/plugins/removable
%{_libdir}/pragha/plugins/removable/removable.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/removable/libremovable.so
# R: glyr
%dir %{_libdir}/pragha/plugins/song-info
%{_libdir}/pragha/plugins/song-info/song-info.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/song-info/libsong-info.so
# R: libsoup
%dir %{_libdir}/pragha/plugins/tunein
%{_libdir}/pragha/plugins/tunein/tunein.plugin
%attr(755,root,root) %{_libdir}/pragha/plugins/tunein/libtunein.so
%{_datadir}/appdata/pragha.appdata.xml
%{_desktopdir}/pragha.desktop
%{_iconsdir}/hicolor/*x*/apps/pragha.png
%{_pixmapsdir}/pragha
%{_mandir}/man1/pragha.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/pragha
