# Maintainer: Tom Meyers tom@odex.be
pkgname=installer-backend
pkgver=r62.2092668
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
        install -Dm755 readme-gen "$pkgdir"/usr/bin/readme-gen
        install -Dm644 visual "$pkgdir"/var/cache/readme/demo
        install -Dm644 generic "$pkgdir"/var/cache/readme/demo
}
