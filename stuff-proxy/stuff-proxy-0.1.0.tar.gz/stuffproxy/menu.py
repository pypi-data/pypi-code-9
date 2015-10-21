import npyscreen as npyscreen


class ProjectSettingsForm(npyscreen.Form):
    def create(self):
        # box = self.add(npyscreen.BoxTitle)
        self.nginxHostname = self.add(npyscreen.TitleText, name='Nginx hostname', use_two_lines=False)
        self.nginxPort = self.add(npyscreen.TitleText, name='Nginx port', use_two_lines=False)
