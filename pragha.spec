Summary:	Lightweight GTK+ music manager
Name:		pragha
Version:	1.0.2
Release:	1
License:	GPL v3+
Group:		Applications/Multimedia
URL:		http://pragha.wikispaces.com/
# VCS: git:https://github.com/matiasdelellis/pragha.git
Source0:	https://github.com/downloads/matiasdelellis/pragha/%{name}-%{version}.tar.bz2
# Source0-md5:	f6ac43773a88d16c51201cedce812b4a
Patch0:		libcdio-paranoia.patch
BuildRequires:	curl-devel >= 7.18
BuildRequires:	dbus-devel >= 1.1
BuildRequires:	dbus-glib-devel >= 0.84
BuildRequires:	desktop-file-utils
BuildRequires:	flac-devel >= 1.2.1
BuildRequires:	gettext
BuildRequires:	glyr-devel >= 0.9.4
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	gtk+2-devel >= 2.20.0
BuildRequires:	keybinder-devel >= 0.2.0
BuildRequires:	libcddb-devel >= 1.3.0
BuildRequires:	libcdio-devel >= 0.80
BuildRequires:	libcdio-paranoia-devel
BuildRequires:	libclastfm-devel >= 0.5
BuildRequires:	libnotify-devel >= 0.4.4
BuildRequires:	libxfce4ui-devel >= 4.8.0
BuildRequires:	sqlite3-devel >= 3.4
BuildRequires:	taglib-devel >= 1.7
BuildRequires:	totem-pl-parser-devel >= 2.26
Requires:	gstreamer-plugins-base
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pragha is is a lightweight GTK+ music manager that aims to be fast,
bloat-free, and light on memory consumption. It is written completely
in C and GTK+.

Pragha is a fork of Consonance Music Manager, discontinued by the
original author.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make} V=1

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

mv $RPM_BUILD_ROOT%{_localedir}/{no,nb}

%find_lang %{name}

# remove duplicate docs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

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
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/%{name}.png
%{_pixmapsdir}/%{name}/
%{_mandir}/man1/pragha.1.*
