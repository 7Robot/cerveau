mkdir -p pkg
rm -rf pkg/*
cd pkg
cp ../PKGBUILD .
makepkg
