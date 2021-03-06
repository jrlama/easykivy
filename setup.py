from distutils.core import setup

version = "0.96"
release = "0.96"

desc = list()
desc.append('EasyKivy provides an easy-to-use interface for simple GUI interaction with a user based on EasyGUI.  ')
desc.append('EasyKivy, like EasyGUI, is different from other GUI generators in that EasyKivy is NOT event-driven.  ')
desc.append('Instead, all GUI interactions are invoked by simple function calls.')

long_description = """
ABOUT EASYKIVY (EasyGUI based GUI)
==================================

EasyKivy provides an easy-to-use interface for simple GUI interaction
with a user, full compatible with de EasyGUI v.0.96 implementation.  
It does not require the programmer to know anything about Kivy.  
All GUI interactions are invoked by simple function calls that return results.

Example Usage
-------------

    >>> import easykivy
    >>> easykivy.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
    1
    >>> easykivy.msgbox('This is a basic message box.', 'Title Goes Here')
    'OK'
    >>> easykivy.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
    'Chocolate'

Full documentation for EasyGUI is available (thanks EasyGUI developers).

For the most-recent production version:
<http://easygui.readthedocs.org/en/master/>.


LICENSE INFORMATION
===================
LICENSE INFORMATION

EasyKivy version 0.96

Copyright (c) 2016, Juan R. Lama


All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer. 
    
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution. 
    
    3. The name of the author may not be used to endorse or promote products derived
       from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@note:
ABOUT THE EASYKIVY LICENSE

This license is what is generally known as the "modified BSD license",
aka "revised BSD", "new BSD", "3-clause BSD".
See http://www.opensource.org/licenses/bsd-license.php

This license is GPL-compatible.
See http://en.wikipedia.org/wiki/License_compatibility
See http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses

The BSD License is less restrictive than GPL.
It allows software released under the license to be incorporated into proprietary products. 
Works based on the software may be released under a proprietary license or as closed source software.
http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29

"""


setup(
    name='easykivy',
    version=version,
    url='https://github.com/jrlama/easykivy',
    description=''.join(desc),
    long_description=long_description,
    author='Juan R. Lama',
    author_email='jrlmaruiz@gmail.com',
    license='BSD',
    keywords='gui linux windows android graphical user interface',
    packages = ['easykivy'],
    package_data={
        'easykivy': ['python_and_check_logo.*', 'zzzzz.gif']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: User Interfaces',
        ]
    )

