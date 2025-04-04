Name: nekoray
Version: 4.2.12
Release: 1%{?autorelease}
Summary: Qt based cross-platform GUI proxy configuration manager (backend: sing-box)
URL: https://github.com/Mahdi-zarei/nekoray
License: GPLv3

Source0: https://github.com/Mahdi-zarei/nekoray/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: rpm_macro(cmake)
BuildRequires: rpm_macro(cmake_build)
BuildRequires: rpm_macro(cmake_install)
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(libcurl)
BuildRequires: cmake(yaml-cpp)
BuildRequires: cmake(ZXing)
BuildRequires: cmake(absl)
BuildRequires: cmake(cpr)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Linguist)
BuildRequires: cmake(Qt6Charts)
BuildRequires: patchelf
BuildRequires: sed

%description
%{summary}

%prep
%autosetup -p1 -n %{name}-%{version}
sed -i 's~find_package(Protobuf CONFIG REQUIRED)~find_package(Protobuf REQUIRED)~' cmake/myproto.cmake

%build
%cmake
%cmake_build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons

cat << EOF > %{buildroot}%{_bindir}/%{name}
#!/bin/sh
%{_libdir}/%{name}/%{name} -appdata "${@}"
EOF

cat << EOF > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Version=1.0
Terminal=false
Type=Application
Name=NekoRay
Categories=Network;
Comment=Qt based cross-platform GUI proxy configuration manager (backend: sing-box)
Comment[zh_CN]=基于 Qt 的跨平台代理配置管理器 (后端 sing-box)
Keywords=Internet;VPN;Proxy;sing-box;
Exec=%{_bindir}/%{name}
Icon=%{_datadir}/icons/%{name}.ico
EOF

cp %{__cmake_builddir}/lib*.so.* %{buildroot}%{_libdir}/
cp %{__cmake_builddir}/%{name} %{buildroot}%{_libdir}/%{name}/%{name}
cp res/nekoray.ico %{buildroot}%{_datadir}/icons/%{name}.ico
patchelf --remove-rpath %{buildroot}%{_libdir}/%{name}/%{name}

%files
%attr(0755, -, -) %{_bindir}/%{name}
%attr(0755, -, -) %{_libdir}/lib*.so.*
%attr(0755, -, -) %{_libdir}/%{name}/%{name}
%attr(0644, -, -) %{_datadir}/icons/%{name}.ico
%attr(0644, -, -) %{_datadir}/applications/%{name}.desktop
%dir %{_libdir}/%{name}
