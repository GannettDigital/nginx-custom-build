#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 5
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl
BuildRequires: openssl-devel
%endif

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
Epoch: 1
%define with_spdy 1
%endif

%if 0%{?suse_version}
Group: Productivity/Networking/Web/Servers
BuildRequires: libopenssl-devel
Requires(pre): pwdutils
%endif

# end of distribution specific definitions

Summary: High performance web server (Built with LDAP, XSLT, XSLT HTML Parser, and Shibboleth module)
Name: nginx
Version: @@VERSION@@
Release: @@RELEASE@@%{?dist}.gd.ngx
Vendor: nginx inc.
URL: http://nginx.org/

Source0: http://nginx.org/download/%{name}-%{version}.tar.gz
Source1: logrotate
Source2: nginx.init
Source3: nginx.sysconf
Source4: nginx.conf
Source5: nginx.vh.default.conf
Source6: nginx.vh.example_ssl.conf
Source7: nginx.suse.init
Source8: nginx.service
Source9: nginx.upgrade.sh
Source10: headers-more-nginx-module
Source11: ngx-fancyindex
Source12: nginx_ajp_module
Source13: nginx-xslt-html-parser.patch
Source14: nginx-auth-ldap
Source15: nginx-http-shibboleth
Source16: ngx_http_auth_pam_module
Source17: echo-nginx-module
Source18: memc-nginx-module
Source19: srcache-nginx-module
Source20: redis2-nginx-module
Source21: ngx_http_enhanced_memcached_module
Source22: ngx_devel_kit
Source23: set-misc-nginx-module
Source24: ngx_http_consistent_hash
Source25: nginx.te
Source26: nginx.pp


License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: openldap-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: pam-devel

BuildRequires: selinux-policy-targeted
Requires: policycoreutils


Provides: webserver

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: nginx
%description debug
Not stripped version of nginx built with the debugging log support.

%package policy
Summary: nginx selinux policy
Group: System Environment/Daemons
BuildRequires: selinux-policy-targeted
Requires: policycoreutils
%description policy
Selinux policy for nginx when set to enforcing

%prep
%setup -q
cp -R -p %SOURCE10 .
cp -R -p %SOURCE11 .
cp -R -p %SOURCE12 .
patch -p1 < %SOURCE13
cp -R -p %SOURCE14 .
cp -R -p %SOURCE15 .
cp -R -p %SOURCE16 .
cp -R -p %SOURCE17 .
cp -R -p %SOURCE18 .
cp -R -p %SOURCE19 .
cp -R -p %SOURCE20 .
cp -R -p %SOURCE21 .
cp -R -p %SOURCE22 .
cp -R -p %SOURCE23 .
cp -R -p %SOURCE24 .
cp -R -p %SOURCE25 .

%build
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        %{?with_spdy:--with-http_spdy_module} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        --with-http_spdy_module \
        --with-http_xslt_module \
        --add-module=%{_builddir}/%{name}-%{version}/ngx-fancyindex \
        --add-module=%{_builddir}/%{name}-%{version}/nginx_ajp_module \
        --add-module=%{_builddir}/%{name}-%{version}/headers-more-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/nginx-auth-ldap \
        --add-module=%{_builddir}/%{name}-%{version}/nginx-http-shibboleth \
	--with-md5-asm  \
	--with-sha1-asm  \
	--with-pcre  \
	--with-pcre-jit  \
	--add-module=%{_builddir}/%{name}-%{version}/echo-nginx-module \
	--add-module=%{_builddir}/%{name}-%{version}/memc-nginx-module \
	--add-module=%{_builddir}/%{name}-%{version}/srcache-nginx-module \
	--add-module=%{_builddir}/%{name}-%{version}/redis2-nginx-module \
	--add-module=%{_builddir}/%{name}-%{version}/ngx_http_enhanced_memcached_module \
	--add-module=%{_builddir}/%{name}-%{version}/ngx_devel_kit \
	--add-module=%{_builddir}/%{name}-%{version}/set-misc-nginx-module \
	--add-module=%{_builddir}/%{name}-%{version}/ngx_http_consistent_hash \
	--add-module=%{_builddir}/%{name}-%{version}/ngx_http_auth_pam_module \

        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/%{name}-%{version}/objs/nginx \
        %{_builddir}/%{name}-%{version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        %{?with_spdy:--with-http_spdy_module} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        --with-http_spdy_module \
        --with-http_xslt_module \
        --add-module=%{_builddir}/%{name}-%{version}/ngx-fancyindex \
        --add-module=%{_builddir}/%{name}-%{version}/nginx_ajp_module \
        --add-module=%{_builddir}/%{name}-%{version}/headers-more-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/nginx-auth-ldap \
        --add-module=%{_builddir}/%{name}-%{version}/nginx-http-shibboleth \
        --with-md5-asm  \
        --with-sha1-asm  \
        --with-pcre  \
        --with-pcre-jit  \
        --add-module=%{_builddir}/%{name}-%{version}/echo-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/memc-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/srcache-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/redis2-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/ngx_http_enhanced_memcached_module \
        --add-module=%{_builddir}/%{name}-%{version}/ngx_devel_kit \
        --add-module=%{_builddir}/%{name}-%{version}/set-misc-nginx-module \
        --add-module=%{_builddir}/%{name}-%{version}/ngx_http_consistent_hash \
        --add-module=%{_builddir}/%{name}-%{version}/ngx_http_auth_pam_module \

        $*
make %{?_smp_mflags}

checkmodule -M -m -o nginx.mod %SOURCE25
semodule_package -o %SOURCE26 -m nginx.mod

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf.sample
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf.sample


%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/%{name}-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

install -p -m 644 -D %{SOURCE26} \
   $RPM_BUILD_ROOT%{_datadir}/selinux/packages/nginx/nginx.pp

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf.sample
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf.sample

%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files policy
%dir %{_datadir}/selinux/packages/nginx
%{_datadir}/selinux/packages/nginx/nginx.pp

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi
%post policy
semodule -i %{_datadir}/selinux/packages/nginx/nginx.pp 2>/dev/null ||:
semanage port -a -t http_port_t -p tcp 8090

%preun
if [ $1 -eq 0 ]; then
semodule -r nginx 2>/dev/null || :
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%preun policy 
semodule -r nginx 2>/dev/null || :

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%postun policy 
semodule -i %{_datadir}/selinux/packages/nginx/nginx.pp 2>/dev/null || :
semanage port -a -t http_port_t -p tcp 8090

%changelog
* Tue Sep 16 2014 Sergey Budnevitch <sb@nginx.com>
- epoch added to the EPEL7/CentOS7 spec to override EPEL one
- 1.6.2

* Thu Aug  5 2014 Sergey Budnevitch <sb@nginx.com>
- 1.6.1

* Thu Jul 12 2014 Sergey Budnevitch <sb@nginx.com>
- incorrect sysconfig filename finding in the initscript fixed

* Thu Apr 24 2014 Konstantin Pavlov <thresh@nginx.com>
- 1.6.0
- http-auth-request module added

* Tue Mar 18 2014 Sergey Budnevitch <sb@nginx.com>
- 1.4.7
- spec cleanup
- openssl version dependence added
- upgrade() function in the init script improved
- warning added when binary upgrade returns non-zero exit code

* Tue Mar  4 2014 Sergey Budnevitch <sb@nginx.com>
- 1.4.6

* Tue Feb 11 2014 Konstantin Pavlov <thresh@nginx.com>
- 1.4.5

* Tue Nov 19 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.4

* Tue Oct  8 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.3

* Tue Jul 17 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.2

* Tue May  6 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.1

* Wed Apr 24 2013 Sergey Budnevitch <sb@nginx.com>
- gunzip module added
- 1.4.0

* Tue Apr  2 2013 Sergey Budnevitch <sb@nginx.com>
- set permissions on default log files at installation
- 1.2.8

* Tue Feb 12 2013 Sergey Budnevitch <sb@nginx.com>
- excess slash removed from --prefix
- 1.2.7

* Tue Dec 11 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.6

* Tue Nov 13 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.5

* Tue Sep 25 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.4

* Tue Aug  7 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.3
- nginx-debug package now actually contains non stripped binary

* Tue Jul  3 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.2

* Tue Jun  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.1

* Mon Apr 23 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.0

* Thu Apr 12 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.15

* Thu Mar 15 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.14
- OpenSUSE init script and SuSE specific changes to spec file added

* Mon Mar  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.13

* Mon Feb  6 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.12
- banner added to install script

* Thu Dec 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.11
- init script enhancements (thanks to Gena Makhomed)
- one second sleep during upgrade replaced with 0.1 sec usleep

* Tue Nov 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.10

* Tue Nov  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.9
- nginx-debug package added

* Tue Oct 11 2011 Sergey Budnevitch <sb@nginx.com>
- spec file cleanup (thanks to Yury V. Zaytsev)
- log dir permitions fixed
- logrotate creates new logfiles with nginx owner
- "upgrade" argument to init-script added (based on fedora one)

* Sat Oct  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.8
- built with mp4 module

* Fri Sep 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.7

* Tue Aug 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.6
- replace "conf.d/*" config include with "conf.d/*.conf" in default nginx.conf

* Tue Aug 10 2011 Sergey Budnevitch
- Initial release

