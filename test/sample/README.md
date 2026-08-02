# Manual test

This is a sample test conanfile.py used to check the source auth plugin works. The
url referred to is valid, but private and should require authentication.

## Without authentication:

```shell
 conan create test/sample/
```

This generates the following output, where the download can not be fetched:
```text
    ... output skipped ...
======== Installing packages ========
download-only/1.0: Calling source() in ~/.conan2/p/downlb88fd09d3fb01/s
ERROR: download-only/1.0: Error in source() method, line 14
    get(self, url="https://api.github.com/repos/conan-py/sample-private-repository/tarball/v1.0.0",
    NotFoundException: Not found: https://api.github.com/repos/conan-py/sample-private-repository/tarball/v1.0.0
```

## With authentication:

If the github application key is installed, and the plugin is installed, then the package can
download its source (or at least a proxy for that imaginary package source).

```shell
conan config install .
pip install --editable .
export GITHUB_AUTH_KEY="$(< test/sample/auth-key.pem)"
conan config install test/sample/
conan create test/sample/
```

```text
======== Installing packages ========                                                                                                                                                                                       
download-only/1.0: Calling source() in C:\Users\gregb\.conan2\p\downlf6cffc938c61a\s
download-only/1.0: Sources correctly downloaded from https://api.github.com/repos/conan-py/sample-private-repository/tarball/v1.0.0
download-only/1.0: Uncompressing archive.tgz to .

-------- Installing package download-only/1.0 (1 of 1) --------                                                                                                                                                             
download-only/1.0: Building from source
download-only/1.0: Package download-only/1.0:da39a3ee5e6b4b0d3255bfef95601890afd80709
>>> Source step
download-only/1.0: Copying sources to build folder
download-only/1.0: Building your package in C:\Users\gregb\.conan2\p\b\downl8d4ad18498fba\b
>>> Generate step
Generating files for download-only/1.0
Generators folder: C:\Users\gregb\.conan2\p\b\downl8d4ad18498fba\b
Generating aggregated env files
Generated aggregated env files: ['conanbuild.bat', 'conanrun.sh']
>>> Build step
Building download-only/1.0
download-only/1.0: Package 'da39a3ee5e6b4b0d3255bfef95601890afd80709' built
download-only/1.0: Build folder C:\Users\gregb\.conan2\p\b\downl8d4ad18498fba\b
>>> Package step
Generating the package download-only/1.0:da39a3ee5e6b4b0d3255bfef95601890afd80709
Packaging in folder C:\Users\gregb\.conan2\p\b\downl8d4ad18498fba\p
package(): WARN: No files in this package!
Created package revision 0ba8627bd47edc3a501e8f0eb9a79e5e
Package 'da39a3ee5e6b4b0d3255bfef95601890afd80709' created
Full package reference: download-only/1.0#e97dc1c00da4cd1c6c495fe3f0a6a006:da39a3ee5e6b4b0d3255bfef95601890afd80709#0ba8627bd47edc3a501e8f0eb9a79e5e
Package folder C:\Users\gregb\.conan2\p\b\downl8d4ad18498fba\p
```