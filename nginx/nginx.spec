#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define buildnumber %(date +%Y%m%d%H%M)

Summary: high performance web server
Name: nginx
Version: 1.4.6
Release: %{buildnumber}%{?dist}.ngx
Epoch: 2
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


License: 2-clause BSD-like license
%if 0%{?suse_version}
Group: Productivity/Networking/Web/Servers
%else
Group: System Environment/Daemons
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: perl
BuildRequires: GeoIP-devel
BuildRequires: expat-devel
%if 0%{?suse_version}
BuildRequires: libopenssl-devel
Requires(pre): pwdutils
%else
BuildRequires: openssl-devel
Requires: initscripts >= 8.36
Requires(pre): shadow-utils
Requires(post): chkconfig
%endif
Requires: GeoIP
Provides: webserver

%description
nginx [engine x] is a HTTP and reverse proxy server, as well as
a mail proxy server

%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: nginx
%description debug
not stripped version of nginx build with the debugging log support

%prep
%setup -q

git clone -b master https://github.com/simpl/ngx_devel_kit.git extra/ngx_devel_kit
git clone -b master https://github.com/agentzh/srcache-nginx-module.git extra/srcache-nginx-module
git clone -b master https://github.com/agentzh/memc-nginx-module.git extra/memc-nginx-module
git clone -b master https://github.com/agentzh/set-misc-nginx-module.git extra/set-misc-nginx-module
git clone -b master https://github.com/yaoweibin/ngx_http_substitutions_filter_module.git extra/ngx_http_substitutions_filter_module
git clone -b master https://github.com/arut/nginx-dav-ext-module.git extra/nginx-dav-ext-module

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
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        --add-module=extra/ngx_devel_kit \
        --add-module=extra/srcache-nginx-module \
        --add-module=extra/memc-nginx-module \
        --add-module=extra/set-misc-nginx-module \
        --add-module=extra/ngx_http_substitutions_filter_module \
	    --add-module=extra/nginx-dav-ext-module \
        --with-http_geoip_module \
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
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        --add-module=extra/srcache-nginx-module \
        --add-module=extra/memc-nginx-module \
        --add-module=extra/ngx_devel_kit \
        --add-module=extra/set-misc-nginx-module \
        --add-module=extra/ngx_http_substitutions_filter_module \
	    --add-module=extra/nginx-dav-ext-module \
        --with-http_geoip_module \
        $*
make %{?_smp_mflags}

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
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx

%endif
# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/%{name}-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%{_initrddir}/nginx

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

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
    /sbin/chkconfig --add nginx
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using NGINX!

Check out our community web site:
* http://nginx.org/en/support.html

If you have questions about commercial support for NGINX please visit:
* http://www.nginx.com/support.html

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service nginx upgrade &>/dev/null || :
fi

