import os, glob, fnmatch

## Added 10 Jan 2008
from distutils.core import setup
import distutils.command.install_data

## Code borrowed from wxPython's setup and config files
## Thanks to Robin Dunn for the suggestion.
## I am not 100% sure what's going on, but it works!
def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)

## Added 10 Jan 2008
# Specializations of some distutils command classes
class wx_smart_install_data(distutils.command.install_data.install_data):
    """need to change self.install_dir to the actual library dir"""
    def run(self):
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return distutils.command.install_data.install_data.run(self)

def find_data_files(srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    ## A list of partials within a filename that would disqualify it
## from appearing in the tarball.
    badnames = [".pyc", "~", "no_"]
    def walk_helper(arg, dirname, files):
        if 'CVS' in dirname: ## ADD/CHANGE as you need here too.
            return
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)
                #if ".pyc" not in filename:
                ## This hairy looking line excludes the filename
                ## if any part of one of  badnames is in it:
                if not any(bad in filename for bad in badnames):
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
        if names:
            lst.append((dirname, names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list

## This is a list of files to install, and where:
## Make sure the MANIFEST.in file points to all the right 
## directories too.
files = find_data_files('jankflixmodules/', '*.*')


setup(name = "jankflix",
    version = "1.1.2",
    description = "Jankflix: A jankier way to watch things",
    author = "fimbrethil",
    author_email = "fimbrethil.wandlimb@gmail.com",
    url = "https://github.com/fimbrethil/jankflix-python",
    packages = ['jankflixmodules'],
    requires = ['BeautifulSoup'],
    data_files = files,

    ## Borrowed from wxPython too:
    ## Causes the data_files to be installed into the modules directory.
    ## Override some of the default distutils command classes with my own.
    cmdclass = { 'install_data':    wx_smart_install_data },

    #'jankflix' is in the root.
    scripts = ["jankflix", "cjankflix"],

)
