#-*-encoding:utf-8-*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyTextUtil',  # pip에 등록될 이름
    version='0.0.6',  # 버전 정보. pip에 올릴 때마다 버전을 갱신해 주어야 한다.

    packages=['pyTextUtil'],  # src/excelpy 폴더, src/excelpy/templates 폴더
    package_dir={'pyTextUtil': 'src'},
    # packages에서 선언한 패키지 이름이 있는 경로

    # package_data={'excelpy': ['templates/xl/worksheets/*']},
    # python 파일이 아닌 파일들을 함께 첨부하고 싶은 경우. excelpy 패키지에 templates/xl/worksheets 밑에 있는
    # 모든 파일을 등록한다.

    install_requires=[],  # excelpy 패키지가 필요로 하는 패키지
    license='Apache License 2.0',  # 라이센스
    author='papower',  # 개발자
    author_email='papower2@gmail.com',  # 개발자 이메일
    url='https://github.com/papower1/pyTextUtil',  # 관련 홈페이지
    description='simple text utils for python',  #설명
    # long_description='Excelpy can add new sheets, copy sheets, delete sheets, and edit string and number type datas.',  # 자세한 설명
    keywords=['textutil', 'textUtil', 'pytextutil', 'pyTextUtil'],  # 키워드
    classifiers=[  # 분류. 설명 안해도 충분하다고 생각하여 생략
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent'
    ],
    entry_points = {
    	'console_scripts' : ['pyTextUtil=pyTextUtil.command_line:main']
    }
)
