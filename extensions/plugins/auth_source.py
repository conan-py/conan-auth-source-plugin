"""
    A Conan plugin module.
"""


def auth_source_plugin(url: str, **kwargs):
    """
        This is a conan plugin, that conforms to the plugin definition in Conan.

        This implementation thunks the call through to the plugin entry point
        in the Conan auth source authentication plugin module.

        In the current implementation, defined here:
          - https://github.com/conan-io/conan/blob/develop2/conan/internal/rest/conan_requester.py#L66

        At the time of writing, Conan invokes this plugin with the request URL and
        no additional keyword arguments. Perhaps in the future Conan could pass:
           - a logger instance
           - the best matching section of the `source_credentials.json` file, or the whole contents
           - the `www-authenticate` headers upon a 401 request failing
    """

    # Import the python module at this point, so that module loading issues
    # are reported during authentication.
    #
    # pylint: disable=import-outside-toplevel
    from auth_source.auth_source_plugin import plugin
    return plugin(url, **kwargs)
