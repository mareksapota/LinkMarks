EAPI=5

PYTHON_COMPAT=( python{3_3,3_4} )

inherit vcs-snapshot

DESCRIPTION="LinkMarks"
HOMEPAGE="https://github.com/maarons/LinkMarks"
SRC_URI="https://github.com/maarons/LinkMarks/archive/${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

DEPEND="dev-python/cherrypy[${PYTHON_USEDEP}]
	dev-ruby/sass
	app-misc/python_apis_maarons
	sys-devel/make"
RDEPEND="${DEPEND}"

src_compile() {
	make
}
