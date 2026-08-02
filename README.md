# [conan-auth-source-plugin](https://github.com/conan-py/conan-auth-source-plugin)

A Conan authentication source plugin, implemented as a python module. Conan supports both a *remote*
and a *source* authentication, where the remotes are used for interacting with a remote for
packages, whereas the *source* is used for getting source using the `get()` or `download()`
method in a `conanfile.py`.

# Installation

Install the conan authentication source Python module, then install the plugin in that module
into the conan installation.

```shell
python -m pip install conan-auth-source-plugin
conan-auth-source-plugin-install
```

# Configuration

This plugin uses the
[`source_creditials.json`](https://docs.conan.io/2/reference/config_files/source_credentials.html)
file for configuration. This file is marked as experimental at this stage. This module further
experiments and extends its usage.

**Note**: The conan source configuration code uses a first match (begins with) strategy with URLs.
Thus, it is important to order the credentials in longest url first if there is any overlap in
matching the URL being fetched with the configuration.

## Sample

```json
{
  "credentials": [
    {
      "url": "https://github.com/...",
      "type": "github.app",
      "app_id": "4459267",
      "app_installation_id": "150620648",
      "app_private_key" : "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
    }
  ]
}
```

# Create App

The following procedure can be used to create an application in github. This procedure requires an
organisation owner, or a team member with app management permissions.

This procedure is documented as a GitHub app that act on their 
[own behalf](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps#github-apps-that-act-on-their-own-behalf).
This requires an installation access token for authentication.

1. Go to the organisation (or user) settings
   
   https://github.com/organizations/conan-py/settings/apps
   https://github.com/<org name>/conan-py/settings/apps

2. App settings
   
  - provide a github app name
  - write a description
  - add a homepage URL (e.g. to the organisation landing page), even though it isn't explicitly used
  - disable web hook
  - add repository permission 'Contents', set to 'Read-Only' 

3. Once the app is created, the 'App ID' and the 'Client ID' (not used for this workflow) are known

4. Go to the bottom of the application and generate a private key. This will
   generate a 2048bit RSA key pair without a pass phrase. 

5. On the side bar of the application, select the "Install App" menu item. Once installed
   the installation id can be taken from the installation URL. For example if the installation
   URL is 'https://github.com/organizations/conan-py/settings/installations/150620648', then the
   installation id is 150620648. The installation id is not displayed in the web UI of github.

# Why use this plugin module

This module is a shift-left style strategy for authentication. Instead of using this pluing
a build pipeline (or any Conan build) can pre-authenticate with all github organisation/repositores
that *may* be needed during a build.

This module goes half-way towards "authentication on demand". This is a concept where http
authentication is only attempted by a client if a 
[401 (Not authenticated)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401)
response is received, and the
[`WWW-Authenticate` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/WWW-Authenticate)
provides
[authentication schemes](https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml)
that are semantically understood by the client. Once authenticated the client should reissue the
http request with the new credentials.

*Residual*: This plugin does not defer authentication until after it is needed. This is not
supported by the Conan client.

# Known issues

- this implementation stores private keys by value in memory. e.g. if using AWS it
  would be better to use a HSM or AWS KMS, but this would require an implementation
  of the `github.Auth.Auth` class. Using AWS Secrets Manager at least stores the
  key more securely at rest, even though it will be stored in memory non-securely.

- when using the `get()` method in a `conanfile.py`, provide a filename parameter
  with a representative name (e.g. 'archive.tgz') so that conan can write the download
  to disk.  The filename should be expressed in the `conandat.yml`.

# Development

To install the plugin in a local Conan environment, the whole of the plugin repository
can be installed, as the `.conanignore` will exclude everything except the plugin
python file that thunks to the module.

```shell
conan config install .
```

Install the plugin Python for development as an editable module. From the root of the
repository/project:

```shell
pip install --editable .
```

# Links

 - https://pypi.org/project/conan-auth-source-plugin 
 - https://github.com/conan-io/conan-extensions/tree/main
 - https://docs.conan.io/2/reference/extensions/authorization_plugins.html
 - https://docs.conan.io/2/reference/config_files/source_credentials.html
 - https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app
 - https://docs.github.com/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps

## pygithub

 - https://github.com/PyGithub/PyGithub/tree/main
 - https://pygithub.readthedocs.io/en/stable/introduction.html

# Appendices

## github tarball URLs

For getting source from a private github repo, use a URL/http request of the form: 

```
GET https://api.github.com/repos/{owner}/{repo}/tarball/{ref}
Authorization: Bearer <installation_token>
```