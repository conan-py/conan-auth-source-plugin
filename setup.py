"""
    Trivial setup.py to package for publishing the module to pypi.
"""
from setuptools import setup, find_packages

setup(
    name="conan-auth-source-plugin",
    use_scm_version=True,
    package_dir={
        "": "src",
        "auth_source_extensions": "extensions",
    },
    packages=find_packages(where="src") + [
        "auth_source_extensions",
        "auth_source_extensions.plugins",
    ],
    python_requires=">=3.13",
    install_requires=[
        "conan>=2.25,<3.0",
        "packaging>=26.2",
        "PyGithub>=2.9.1"
    ],
    package_data={
        "auth_source_extensions.plugins": ["plugin_auth_source.py"],
    },
    entry_points={
        "console_scripts": [
            # An entry point to install this plugin into conan
            "conan-auth-source-plugin-install = auth_source.installer:main",
        ],
    },
)
