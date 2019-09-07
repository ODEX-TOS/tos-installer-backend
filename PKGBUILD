# Maintainer: Tom Meyers tom@odex.be
pkgname=installer-backend
pkgver=r81.105ed28
pkgrel=1
pkgdesc="API for installing Operating Systems"
arch=(any)
url="https://github.com/ODEX-TOS/tos-installer-backend"
_reponame="tos-installer-backend"
license=('GPL')

source=(
"git+https://github.com/ODEX-TOS/tos-installer-backend.git")
md5sums=('SKIP')
depends=('python' 'python-yaml')
makedepends=('git')

pkgver() {
  cd "$srcdir/$_reponame"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}


build() {
    return 0;
}

package() {
        cd "$srcdir/$_reponame"
        python setup.py  install --root="${pkgdir}"
}
