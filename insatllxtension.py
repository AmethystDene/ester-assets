#!/usr/bin/python3

########################################################################
#                                                                      #
# install-gnome-shell-extension.py                                     #
#                                                                      #
# In order to prevent the customized default schema files in           #
# /usr/share/glib-2.0/schemas from being overridden, remove all        #
# distribution specific schema override files in this directory by     #
# moving them to a backup directory in /tmp.                           #
#                                                                      #
# Copyright (C) 2019 PJ Singh <psingh.cubic@gmail.com>                 #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program. If not, see <https://www.gnu.org/licenses>. #
#                                                                      #
########################################################################
"""
Install the specified gnome shell extension.

Run this program as root or using sudo.

Usage:

$ sudo ./install-gnome-shell-extension extension_id [shell_version]

Examples:

# Install Dash to Dock
$ sudo ./install-gnome-shell-extension 307

# Install Dash to Dock for Gnome Shell version 3.38
$ sudo ./install-gnome-shell-extension 307 3.38

Arguments:

extension_id (int)
    The extension number
shell_version (str)
    The Gnome shell version

Returns:
    None
"""

import json
import shutil
import subprocess
import sys
import tempfile
import traceback
import urllib
import urllib.request
import xml.etree.ElementTree as ElementTree
import zipfile

########################################################################
# References
########################################################################

# https://docs.python.org/3/howto/urllib2.html

########################################################################
# Globals & Constants
########################################################################

EXTENSION_INFORMATION_URL_TEMPLATE = 'https://extensions.gnome.org/extension-info/?pk=%i&shell_version=%s'
EXTENSION_DOWNLOAD_URL_TEMPLATE = 'https://extensions.gnome.org%s'
EXTENSION_DIRECTORY_TEMPLATE = '/usr/share/gnome-shell/extensions/%s'
# EXTENSION_DIRECTORY_TEMPLATE = '/home/psingh/Temp/test/%s'

########################################################################
# Functions
########################################################################

#-----------------------------------------------------------------------
# Arguments
#-----------------------------------------------------------------------


def get_arguments():

    extension_id = None
    try:
        extension_id = int(sys.argv[1])
    except IndexError:
        pass
    except ValueError:
        pass

    shell_version = None
    try:
        shell_version = str(sys.argv[2])
    except IndexError:
        pass
    except ValueError:
        pass

    return extension_id, shell_version


#-----------------------------------------------------------------------
# Gnome Shell Version
#-----------------------------------------------------------------------


def get_shell_version():

    # Try to get the Gnome shell version from
    # '/usr/share/gnome/gnome-version.xml'.
    try:
        filepath = '/usr/share/gnome/gnome-version.xml'
        tree = ElementTree.parse(filepath)
        root = tree.getroot()
        platform = root.find('platform').text
        shell_version = platform
        minor = root.find('minor').text
        shell_version = shell_version + '.' + minor
        try:
            micro = root.find('micro').text
            shell_version = shell_version + '.' + micro
        except AttributeError:
            print('• Ignoring. Unable to get Gnome micro version from.')
        print('• The Gnome Shell version is %s.' % shell_version)
        return shell_version
    except Exception as exception:
        print('• Warning. Unable to get the Gnome shell version.')
        print('• The exception is %s.' % exception)
        # print('• The tracekback is %s.' % traceback.format_exc())

    # Try to get the Gnome shell version using 'gnome-shell --version'.
    try:
        output = subprocess.check_output(['gnome-shell', '--version'])
        output = output.strip()
        output = output.decode("utf-8")
        output = output.split()
        shell_version = output[-1]
        print('• The Gnome Shell version is %s.' % shell_version)
        return shell_version
    except Exception as exception:
        print('• Warning. Unable to get the Gnome shell version.')
        print('• The exception is %s.' % exception)
        # print('• The tracekback is %s.' % traceback.format_exc())

    return ''


#-----------------------------------------------------------------------
# Download the Extension
#-----------------------------------------------------------------------


def download_extension(extension_id, shell_version):

    # Drop all trailing decimal zero(s) from the shell version.
    if int(float(shell_version)) == float(shell_version):
        shell_version = str(int(float(shell_version)))
    else:
        shell_version = str(float(shell_version))

    url = EXTENSION_INFORMATION_URL_TEMPLATE % (extension_id, shell_version)
    print('• The extension information url is %s.' % url)
    try:
        with urllib.request.urlopen(url) as response:
            try:
                # Get extension information.
                data = response.read()
                info = json.loads(data)
                name = info.get('name')
                print('• The extension name is %s.' % name)
                uuid = info.get('uuid')
                print('• The extension uuid is %s.' % uuid)
                shell_versions = info.get('shell_version_map')
                print('• Supported shell versions are %s.' % ', '.join(list(shell_versions.keys())))
                if shell_version in shell_versions:
                    # Ex: url = 'https://extensions.gnome.org/download-extension/dash-to-dock@micxgx.gmail.com.shell-extension.zip?version_tag=15925'
                    url = EXTENSION_DOWNLOAD_URL_TEMPLATE % info.get('download_url')
                    print('• The extension download url is %s.' % url)
                    # Download the extension.
                    try:
                        with urllib.request.urlopen(url) as response:
                            try:
                                # Extract the extension
                                # extension_directory = EXTENSION_DIRECTORY_TEMPLATE % uuid
                                # extension_filepath = '%s/test.zip' % extension_directory
                                # with open(extension_filepath, 'wb') as target:
                                #     shutil.copyfileobj(response, target)
                                #     print('• Saved the extension as %s.' % extension_filepath)
                                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                                    shutil.copyfileobj(response, temp_file)
                                    extension_directory = EXTENSION_DIRECTORY_TEMPLATE % uuid
                                    print('• The extension directory is %s.' % extension_directory)
                                    try:
                                        # Unzip the temporary file to the target directory.
                                        with zipfile.ZipFile(temp_file, 'r') as zip_file:
                                            # The extension directory path will be created.
                                            zip_file.extractall(extension_directory)
                                        print(
                                            '• Successfully extracted %s extension %d for Gnome %s to %s.' %
                                            (uuid,
                                             extension_id,
                                             shell_version,
                                             extension_directory))
                                    except Exception as exception:
                                        print('• Error. Unable to extract extension to %s.' % extension_directory)
                                        print('• The exception is %s.' % exception)
                                        # print('• The tracekback is %s.' % traceback.format_exc())
                            except Exception as exception:
                                print('• Error. Unable to save extension as a temporary file from %s.' % url)
                                print('• The exception is %s.' % exception)
                                # print('• The tracekback is %s.' % traceback.format_exc())
                    except urllib.error.URLError as exception:
                        print('• Error. Unable to access %s.' % url)
                        print('• The exception is %s.' % exception)
                        # print('• The tracekback is %s.' % traceback.format_exc())
                else:
                    print('• Error. Shell version %s is not supported by this extension.' % shell_version)
            except Exception as exception:
                print('• Error. Unable to get extension information from %s.' % url)
                print('• The exception is %s.' % exception)
                print('• The tracekback is %s.' % traceback.format_exc())
    except urllib.error.URLError as exception:
        print('• Error. Unable to access %s.' % url)
        print('• The exception is %s.' % exception)
        # print('• The tracekback is %s.' % traceback.format_exc())


#-----------------------------------------------------------------------
# Execute
#-----------------------------------------------------------------------

extension_id, shell_version = get_arguments()

if extension_id:
    print('Install extension %d...' % extension_id)
else:
    print('• Error. An extension id number is required.')
    exit()

system_shell_version = get_shell_version()

shell_version = shell_version or system_shell_version
if shell_version:
    print('• Install extension for Gnome Shell version %s.' % shell_version)
else:
    print('• Error. The Gnome Shell version is required.')
    exit()

# Install the extension.
download_extension(extension_id, shell_version)
