# Maintainer: Élie Bouttier <elie.bouttier@free.fr>
pkgname=7robot-eurobot-git
pkgver=20120425
pkgrel=1
pkgdesc="7Robot eurobot related sources"
arch=('i686' 'x86_64')
url="http://github.com/bouttier/eurobot/"
license=('GPL')
depends=()
makedepends=('git')

_gitroot=../..
_gitname=ARM

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [[ -d "$_gitname" ]]; then
    cd "$_gitname" && git pull origin
    msg "The local files are updated."
  else
    git clone "$_gitroot" "$_gitname"
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting build..."

  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"

  mkdir build
  cd build
  cmake .. -DCMAKE_INSTALL_PREFIX=/usr
  make
}

package() {
  cd "$srcdir/$_gitname-build/build"
  make DESTDIR="$pkgdir/" install
}
