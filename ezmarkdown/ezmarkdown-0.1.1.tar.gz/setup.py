# necessary to push to PyPI
# cf. http://peterdowns.com/posts/first-time-with-pypi.html
# cf. https://tom-christie.github.io/articles/pypi/


from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
  name = 'ezmarkdown',
  packages = ['ezmarkdown'],
  version = '0.1.1',
  description = 'easy markdown: Write markdown in IPython notebook and generate standalone HTML file from it, picking the cells to output',
  long_description = long_description,
  author = 'oscar6echo',
  author_email = 'olivier.borderies@gmail.com',
  url = 'https://github.com/oscar6echo/ezmarkdown', # use the URL to the github repo
  download_url = 'https://github.com/oscar6echo/ezmarkdown/tarball/0.1.1', # tag number at the end
  keywords = ['markdown', 'export', 'notebook', 'HTML'], # arbitrary keywords
  license='MIT',
  classifiers = [ 'Development Status :: 4 - Beta',
                  'License :: OSI Approved :: MIT License',
                  'Programming Language :: Python :: 2.7'
  ],
  include_package_data=True,
  package_data={
    'template':
        ['template/html_input_output.tpl',
         'template/html_input_toggle_output.tpl',
         'template/html_input.tpl',
         'template/html_output_toggle_input.tpl',
         'template/html_output.tpl',
        ]
    },
)