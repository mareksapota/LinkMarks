EAPI=5

PYTHON_COMPAT=( python{3_3,3_4} pypy3 )

inherit distutils-r1

DESCRIPTION="LinkMarks"
HOMEPAGE="https://github.com/maarons/LinkMarks"

EGIT_REPO_URI="https://github.com/maarons/LinkMarks.git"
EGIT_HAS_SUBMODULES=1
EGIT_COMMIT="${PV}"
SRC_URI=""
inherit git-2

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

DEPEND="dev-python/cherrypy[${PYTHON_USEDEP}]
	dev-ruby/sass
	net-libs/nodejs
	net-misc/curl
	sys-devel/make"
RDEPEND="${DEPEND}"

src_compile() {
	make || die "Make failed"
}

src_install() {
	dodir "/usr/share/LinkMarks"
	rsync -a --exclude '.git' --exclude 'packaging' \
		"${S}/" "${D}/usr/share/LinkMarks" || die "Install failed"
}
