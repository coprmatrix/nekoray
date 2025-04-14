ver=$(cat '_service:set_version:nekoray.spec' | sed -n 's~Version: ~~p;')
curl "https://github.com/bunzuhbu/nekoray/releases/download/${ver}/nekoray-${ver}.tar.gz" -o "${outdir}/nekoray-${ver}.tar.gz"
tar -xzf "${outdir}/nekoray-${ver}.tar.gz" --directory "${outdir}"
pushd "${outdir}"
pushd "nekoray-${ver}/core/server"
go mod vendor
curl https://api.github.com/repos/sagernet/sing-box/releases/latest | jq -r '.name' > "../../../NekoRay-${ver}.Sagernet.SingBox.Version.txt"
mv vendor ../../../
rm -rfv ../updater
popd
tar -czf "vendor-${ver}.tar.gz" vendor
popd
