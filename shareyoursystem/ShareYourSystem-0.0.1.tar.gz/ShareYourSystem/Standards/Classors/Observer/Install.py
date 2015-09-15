#ImportModules
import os
from ShareYourSystem.Standards.Objects import Installer

#Install
Installer.InstallerClass().install(**{
			'InstallingPathStr':os.getcwd()+"/"
			}
		)

