%global upstream_version 11.0.25+9
# Only [A-Za-z0-9.] allowed in version:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Versioning/#_upstream_uses_invalid_characters_in_the_version
# also not very intuitive:
#  $ rpmdev-vercmp 11.0.13.0.1___7 11.0.13.0.0+8
#  11.0.13.0.0___8 == 11.0.13.0.0+8
%global spec_version 11.0.25.0.0.9
%global spec_release 1
%global priority 1112

%global source_url_base https://github.com/adoptium/temurin11-binaries/releases/download
%global upstream_version_url %(echo %{upstream_version} | sed 's/\+/%%2B/g')
%global upstream_version_no_plus %(echo %{upstream_version} | sed 's/\+/_/g')
%global java_provides openjre

# Map architecture to the expected value in the download URL; Allow for a
# pre-defined value of vers_arch and use that if it's defined

%ifarch x86_64
%global vers_arch x64
%global vers_arch2 ppc64le
%global vers_arch3 s390x
%global vers_arch4 aarch64
%global vers_arch5 arm
%global src_num 0
%global sha_src_num 1
%endif
%ifarch ppc64le
%global vers_arch x64
%global vers_arch2 ppc64le
%global vers_arch3 s390x
%global vers_arch4 aarch64
%global vers_arch5 arm
%global src_num 2
%global sha_src_num 3
%endif
%ifarch s390x
%global vers_arch x64
%global vers_arch2 ppc64le
%global vers_arch3 s390x
%global vers_arch4 aarch64
%global vers_arch5 arm
%global src_num 4
%global sha_src_num 5
%endif
%ifarch aarch64
%global vers_arch x64
%global vers_arch2 ppc64le
%global vers_arch3 s390x
%global vers_arch4 aarch64
%global vers_arch5 arm
%global src_num 6
%global sha_src_num 7
%endif
%ifarch %{arm}
%global vers_arch x64
%global vers_arch2 ppc64le
%global vers_arch3 s390x
%global vers_arch4 aarch64
%global vers_arch5 arm
%global src_num 8
%global sha_src_num 9
%endif
# Allow for noarch SRPM build
%ifarch noarch
%global src_num 0
%global sha_src_num 1
%endif

Name:        temurin-11-jre
Version:     %{spec_version}
Release:     %{spec_release}
Summary:     Eclipse Temurin 11 JRE

Group:       java
License:     GPLv2 with exceptions
Vendor:      Eclipse Adoptium
URL:         https://projects.eclipse.org/projects/adoptium
Packager:    Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org>

AutoReqProv: no
Prefix: /usr/lib/jvm/%{name}

ExclusiveArch: x86_64 ppc64le s390x aarch64 %{arm}

BuildRequires:  tar
BuildRequires:  wget

Requires: /bin/sh
Requires: /usr/sbin/alternatives
Requires: ca-certificates
Requires: dejavu-sans-fonts
Requires: libX11%{?_isa}
Requires: libXext%{?_isa}
Requires: libXi%{?_isa}
Requires: libXrender%{?_isa}
Requires: libXtst%{?_isa}
Requires: alsa-lib%{?_isa}
Requires: glibc%{?_isa}
Requires: zlib%{?_isa}
Requires: fontconfig%{?_isa}

Provides: jre
Provides: jre-11
Provides: jre-11-headless
Provides: jre-11-%{java_provides}
Provides: jre-11-%{java_provides}-headless
Provides: jre-headless
Provides: jre-%{java_provides}
Provides: jre-%{java_provides}-headless

# First architecture (x86_64)
Source0: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch}_linux_hotspot_%{upstream_version_no_plus}.tar.gz
Source1: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch}_linux_hotspot_%{upstream_version_no_plus}.tar.gz.sha256.txt
# Second architecture (ppc64le)
Source2: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch2}_linux_hotspot_%{upstream_version_no_plus}.tar.gz
Source3: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch2}_linux_hotspot_%{upstream_version_no_plus}.tar.gz.sha256.txt
# Third architecture (s390x)
Source4: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch3}_linux_hotspot_%{upstream_version_no_plus}.tar.gz
Source5: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch3}_linux_hotspot_%{upstream_version_no_plus}.tar.gz.sha256.txt
# Fourth architecture (aarch64)
Source6: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch4}_linux_hotspot_%{upstream_version_no_plus}.tar.gz
Source7: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch4}_linux_hotspot_%{upstream_version_no_plus}.tar.gz.sha256.txt
# Fifth architecture (arm32)
Source8: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch5}_linux_hotspot_%{upstream_version_no_plus}.tar.gz
Source9: %{source_url_base}/jdk-%{upstream_version_url}/OpenJDK11U-jre_%{vers_arch5}_linux_hotspot_%{upstream_version_no_plus}.tar.gz.sha256.txt

# Set the compression format to xz to be compatible with more Red Hat flavours. Newer versions of Fedora use zstd which
# is not available on CentOS 7, for example. https://github.com/rpm-software-management/rpm/blob/master/macros.in#L353
# lists the available options.
%define _source_payload w7.xzdio
%define _binary_payload w7.xzdio

# Avoid build failures on some distros due to missing build-id in binaries.
%global debug_package %{nil}
%global __brp_strip %{nil}

%description
Eclipse Temurin JRE is an OpenJDK-based runtime environment to execute
applications and components using the programming language Java.

%prep
pushd "%{_sourcedir}"
sha256sum -c "%{expand:%{SOURCE%{sha_src_num}}}"
popd

%setup -n jdk-%{upstream_version}-jre -T -b %{src_num}

%build
# noop

%install
mkdir -p %{buildroot}%{prefix}
cd %{buildroot}%{prefix}
tar --strip-components=1 -C "%{buildroot}%{prefix}" -xf %{expand:%{SOURCE%{src_num}}}

# Use cacerts included in OS
rm -f "%{buildroot}%{prefix}/lib/security/cacerts"
pushd "%{buildroot}%{prefix}/lib/security"
ln -s /etc/pki/java/cacerts "%{buildroot}%{prefix}/lib/security/cacerts"
popd

# Ensure systemd-tmpfiles-clean does not remove pid files
# https://bugzilla.redhat.com/show_bug.cgi?id=1704608
%{__mkdir} -p %{buildroot}/usr/lib/tmpfiles.d
echo 'x /tmp/hsperfdata_*' > "%{buildroot}/usr/lib/tmpfiles.d/%{name}.conf"
echo 'x /tmp/.java_pid*' >> "%{buildroot}/usr/lib/tmpfiles.d/%{name}.conf"

%post
if [ $1 -ge 1 ] ; then
    update-alternatives --install %{_bindir}/java java %{prefix}/bin/java %{priority} \
                        --slave %{_bindir}/jaotc jaotc %{prefix}/bin/jaotc \
                        --slave %{_bindir}/jfr jfr %{prefix}/bin/jfr \
                        --slave %{_bindir}/jjs jjs %{prefix}/bin/jjs \
                        --slave %{_bindir}/jrunscript jrunscript %{prefix}/bin/jrunscript \
                        --slave %{_bindir}/keytool keytool %{prefix}/bin/keytool \
                        --slave %{_bindir}/pack200 pack200 %{prefix}/bin/pack200 \
                        --slave %{_bindir}/rmid rmid %{prefix}/bin/rmid \
                        --slave %{_bindir}/rmiregistry rmiregistry %{prefix}/bin/rmiregistry \
                        --slave %{_bindir}/unpack200 unpack200 %{prefix}/bin/unpack200 \
                        \
                        --slave  %{_mandir}/man1/java.1 java.1 %{prefix}/man/man1/java.1 \
                        --slave  %{_mandir}/man1/jjs.1 jjs.1 %{prefix}/man/man1/jjs.1 \
                        --slave  %{_mandir}/man1/keytool.1 keytool.1 %{prefix}/man/man1/keytool.1 \
                        --slave  %{_mandir}/man1/pack200.1 pack200.1 %{prefix}/man/man1/pack200.1 \
                        --slave  %{_mandir}/man1/rmid.1 rmid.1 %{prefix}/man/man1/rmid.1 \
                        --slave  %{_mandir}/man1/rmiregistry.1 rmiregistry.1 %{prefix}/man/man1/rmiregistry.1 \
                        --slave  %{_mandir}/man1/unpack200.1 unpack200.1 %{prefix}/man/man1/unpack200.1
fi

%preun
if [ $1 -eq 0 ]; then
    update-alternatives --remove java %{prefix}/bin/java
fi

%files
%defattr(-,root,root)
%{prefix}
/usr/lib/tmpfiles.d/%{name}.conf

%changelog
* Wed Oct 16 2024 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.25.0.0.9-1
- Eclipse Temurin 11.0.25.0+9 release.
* Wed Jul 17 2024 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.24.0.0.8-1
- Eclipse Temurin 11.0.24.0+8 release.
* Wed Apr 17 2024 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.23.0.0.9-1
- Eclipse Temurin 11.0.23.0+9 release.
* Tue Jan 23 2024 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.22.0.0.7-1
- Eclipse Temurin 11.0.22.0+7 release.
* Thu Oct 26 2023 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.21.0.0.1-9
- Eclipse Temurin 11.0.21.0+9 release.
* Thu Aug 31 2023 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.20.1.0.1-1
- Eclipse Temurin 11.0.20.1+1 release.
* Tue Jul 25 2023 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.20.0.0.8-1
- Eclipse Temurin 11.0.20+8 release.
* Wed Apr 26 2023 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.19.0.0.7-1
- Eclipse Temurin 11.0.19+7 release.
* Wed Feb 22 2023 Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.18.0.0.10-3
- Eclipse Temurin 11.0.18+10 release 3.
* Mon Jan 30 2023 11:35:00  Eclipse Adoptium Package Maintainers <temurin-dev@eclipse.org> 11.0.18.0.0.10-1
- Eclipse Temurin JRE 11.0.18+10 release.
