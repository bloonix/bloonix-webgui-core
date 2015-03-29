Summary: Bloonix core package for the WebGUI
Name: bloonix-webgui-core
Version: 0.10
Release: 1%{dist}
License: Commercial
Group: Utilities/System
Distribution: RHEL and CentOS

Packager: Jonny Schulz <js@bloonix.de>
Vendor: Bloonix

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: http://download.bloonix.de/sources/%{name}-%{version}.tar.gz
Requires: bloonix-agent
Requires: bloonix-core
Requires: bloonix-dbi
Requires: bloonix-fcgi
Requires: bloonix-heaven
Requires: perl-JSON-XS
Requires: perl-Time-modules
Requires: perl(Digest::SHA)
Requires: perl(JSON)
Requires: perl(MIME::Base64)
Requires: perl(MIME::Lite)
Requires: perl(Log::Handler)
Requires: perl(Params::Validate)
Requires: perl(Time::HiRes)
AutoReqProv: no

%description
bloonix-webgui-core provides core packages for the Bloonix-WebGUI.

%define with_systemd 0
%define initdir %{_sysconfdir}/init.d
%define docdir %{_docdir}/%{name}-%{version}
%define blxdir /usr/lib/bloonix

%prep
%setup -q -n %{name}-%{version}

%build
%{__perl} Configure.PL --prefix /usr --build-package
%{__make}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
mkdir -p ${RPM_BUILD_ROOT}%{docdir}
install -c -m 0444 LICENSE ${RPM_BUILD_ROOT}%{docdir}/
install -c -m 0444 ChangeLog ${RPM_BUILD_ROOT}%{docdir}/

%if %{?with_systemd}
install -p -D -m 0644 %{buildroot}%{blxdir}/etc/systemd/bloonix-webgui.service %{buildroot}%{_unitdir}/bloonix-webgui.service
%else
install -p -D -m 0755 %{buildroot}%{blxdir}/etc/init.d/bloonix-webgui %{buildroot}%{initdir}/bloonix-webgui
%endif

%pre
getent group bloonix >/dev/null || /usr/sbin/groupadd bloonix
getent passwd bloonix >/dev/null || /usr/sbin/useradd \
    bloonix -g bloonix -s /sbin/nologin -d /var/run/bloonix -r

%post
if [ -x "/srv/bloonix/webgui/scripts/bloonix-webgui" ] ; then
%if %{?with_systemd}
systemctl preset bloonix-webgui.service
systemctl condrestart bloonix-webgui.service
%else
/sbin/chkconfig --add bloonix-webgui
/sbin/service bloonix-webgui condrestart &>/dev/null
%endif
fi

if [ ! -e "/etc/bloonix/webgui/main.conf" ] ; then
    mkdir -p /etc/bloonix/webgui
    chown root:root /etc/bloonix /etc/bloonix/webgui
    chmod 755 /etc/bloonix /etc/bloonix/webgui
    cp -a /usr/lib/bloonix/etc/webgui/main.conf /etc/bloonix/webgui/main.conf
    chown -R root:bloonix /etc/bloonix/webgui/main.conf
    chmod 640 /etc/bloonix/webgui/main.conf
fi

if [ ! -e "/etc/bloonix/database/main.conf" ] ; then
    mkdir -p /etc/bloonix/database
    chown root:root /etc/bloonix /etc/bloonix/database
    chmod 755 /etc/bloonix /etc/bloonix/database
    cp -a /usr/lib/bloonix/etc/database/webgui-main.conf /etc/bloonix/database/main.conf
    chown root:bloonix /etc/bloonix/database/main.conf
    chmod 640 /etc/bloonix/database/main.conf
fi

if [ -e "/etc/nginx" ] && [ ! -e "/etc/nginx/conf.d/bloonix-webgui.conf" ] ; then
    if [ ! -e "/etc/nginx/conf.d" ] ; then
        mkdir /etc/nginx/conf.d
    fi
    install -c -m 0644 /usr/lib/bloonix/etc/webgui/nginx.conf /etc/nginx/conf.d/bloonix-webgui.conf
fi

%preun
if [ $1 -eq 0 ]; then
%if %{?with_systemd}
systemctl --no-reload disable bloonix-webgui.service
systemctl stop bloonix-webgui.service
systemctl daemon-reload
%else
    /sbin/service bloonix-webgui stop &>/dev/null || :
    /sbin/chkconfig --del bloonix-webgui
%endif
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%if %{?with_systemd} == 1
%{_unitdir}/bloonix-webgui.service
%else
%{initdir}/bloonix-webgui
%endif

%dir %attr(0755, root, root) %{blxdir}
%dir %attr(0755, root, root) %{blxdir}/etc
%dir %attr(0755, root, root) %{blxdir}/etc/webgui
%{blxdir}/etc/webgui/main.conf
%{blxdir}/etc/webgui/nginx.conf
%dir %attr(0755, root, root) %{blxdir}/etc/database
%{blxdir}/etc/database/webgui-main.conf
%dir %attr(0755, root, root) %{blxdir}/etc/systemd
%{blxdir}/etc/systemd/bloonix-webgui.service
%dir %attr(0755, root, root) %{blxdir}/etc/init.d
%{blxdir}/etc/init.d/bloonix-webgui
%dir %attr(0755, root, root) %{docdir}
%doc %attr(0444, root, root) %{docdir}/ChangeLog
%doc %attr(0444, root, root) %{docdir}/LICENSE

%changelog
* Sat Mar 21 2015 Jonny Schulz <js@bloonix.de> - 0.10-1
- Splitted configuration for fcgi and proc manager.
* Mon Feb 16 2015 Jonny Schulz <js@bloonix.de> - 0.9-1
- Kicked sth_cache_enabled from database config.
* Mon Feb 16 2015 Jonny Schulz <js@bloonix.de> - 0.8-1
- Add parameter sth_cache_enabled to the database config.
* Sat Feb 14 2015 Jonny Schulz <js@bloonix.de> - 0.7-1
- Transfer the database configuration to /etc/bloonix/database/main.conf.
* Thu Jan 29 2015 Jonny Schulz <js@bloonix.de> - 0.6-2
- Fixed %preun.
* Mon Jan 26 2015 Jonny Schulz <js@bloonix.de> - 0.6-1
- New dependency MIME::Lite added.
* Tue Jan 13 2015 Jonny Schulz <js@bloonix.de> - 0.5-1
- Kicked dependency postfix.
* Fri Dec 05 2014 Jonny Schulz <js@bloonix.de> - 0.4-1
- Changed the boot facility.
- Fixed @@LIBDIR@@.
* Sun Nov 16 2014 Jonny Schulz <js@bloonix.de> - 0.3-1
- Fixed permissions of /etc/bloonix*.
* Mon Nov 03 2014 Jonny Schulz <js@bloonix.de> - 0.2-1
- Updated the license information.
* Mon Aug 25 2014 Jonny Schulz <js@bloonix.de> - 0.1-1
- Initial release.
