Name: nekoray
Version: 4.3.2
Release: 0%{?autorelease}
Summary: Qt based cross-platform GUI proxy configuration manager (backend: sing-box)
URL: https://github.com/Mahdi-zarei/nekoray
License: GPLv3

Source0: https://github.com/Mahdi-zarei/nekoray/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# cd nekoray-%{version}/core/server; go mod vendor; mv vendor ../../../; cd ../../../; tar -czf vendor-%{version}.tar.gz vendor;
Source1: vendor-%{version}.tar.gz
# curl https://api.github.com/repos/sagernet/sing-box/releases/latest | jq -r '.name' > Sagernet.SingBox.Version
Source2: Sagernet.SingBox.Version
Source3: %{name}.desktop
Source4: %{name}.sh
Source100: run.sh
Source101: _service

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
BuildRequires: golang
BuildRequires: rpm_macro(gobuildflags)
Requires: %{name}-core
%define core nekobox_core

%package core
Summary: %{summary}

%description
%{summary}

%description core
%{summary}

%prep
%autosetup -p1 -n %{name}-%{version}
sed -i 's~find_package(Protobuf CONFIG REQUIRED)~find_package(Protobuf REQUIRED)~' cmake/myproto.cmake
sed -i 's~ImageFormat::BGRA~ImageFormat::BGR~' 3rdparty/ZxingQtReader.hpp

%build
%cmake
%cmake_build
DEST=$PWD/%{__cmake_builddir}/%{core}
pushd core/server
%{_rpmconfigdir}/rpmuncompress -xv %{SOURCE1}
VERSION_SINGBOX=$(cat %{SOURCE2})
go build %{gobuildflags} -o $DEST -trimpath -ldflags "-w -s -X 'github.com/sagernet/sing-box/constant.Version=${VERSION_SINGBOX}'" -tags "with_clash_api,with_gvisor,with_quic,with_wireguard,with_utls,with_ech,with_dhcp"
popd

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons

cp %{SOURCE4} %{buildroot}%{_bindir}/%{name}
cp %{SOURCE3} %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i 's~/bin~%{_bindir}~g;s~/usr/share~%{_datadir}~g;s~nekoray~%{name}~g' %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i 's~/bin~%{_bindir}~g;s~/lib64~%{_libdir}~g;s~nekoray~%{name}~g' %{buildroot}%{_bindir}/%{name}
cp %{__cmake_builddir}/lib*.so.* %{buildroot}%{_libdir}/
cp %{__cmake_builddir}/%{name} %{buildroot}%{_libdir}/%{name}/%{name}
cp %{__cmake_builddir}/%{core} %{buildroot}%{_libdir}/%{name}/%{core}
cp res/nekoray.ico %{buildroot}%{_datadir}/icons/%{name}.ico
patchelf --remove-rpath %{buildroot}%{_libdir}/%{name}/%{name}
patchelf --remove-rpath %{buildroot}%{_libdir}/%{name}/%{core}

%files
%attr(0755, -, -) %{_bindir}/%{name}
%attr(0755, -, -) %{_libdir}/lib*.so.*
%attr(0755, -, -) %{_libdir}/%{name}/%{name}
%attr(0644, -, -) %{_datadir}/icons/%{name}.ico
%attr(0644, -, -) %{_datadir}/applications/%{name}.desktop

%files core
%dir %{_libdir}/%{name}
%attr(0755, -, -) %{_libdir}/%{name}/%{core}

