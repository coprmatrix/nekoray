ver=$(cat '_service:set_version:nekoray.spec' | sed -n 's~Version: ~~p;')
tar -xzf ./*nekoray-$ver.tar.gz --directory "${outdir}"
pushd "${outdir}"
pushd "nekoray-${ver}/core/server"
go mod vendor
curl https://api.github.com/repos/sagernet/sing-box/releases/latest | jq -r '.name' > ../../../Sagernet.SingBox.Version
mv vendor ../../../
rm -rfv ../updater
popd
tar -czf "vendor-${ver}.tar.gz" vendor
popd
