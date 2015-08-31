from distutils.core import setup

setup(
    name='pynct',
    version='0.1.0',
    author='Delphine Draelants',
    author_email='Delphine.Draelants@uantwerpen.be',
    packages=['pynct', 'pynct.condition', 'pynct.solver', 'pynct.demo_biology', 'pynct.demo_biology.system'],
    description='Python toolbox for continuation'
)

