from conan import ConanFile
from conan.tools.files import get


class DownloadRecipe(ConanFile):
    """
        A test sample, see the README.md
    """
    name = "download-only"
    version = "1.0"

    def source(self):
        get(self,
            url="https://api.github.com/repos/conan-py/sample-private-repository/tarball/v1.0.0",
            filename = "archive.tgz",
            strip_root=True, )
