import os
import shutil
import shlex
import subprocess

def latexfig(textstr,filename,environment='align*',env_curly=None):
	# ======================================
	# Validate Extension
	# ======================================
	split = os.path.splitext(filename)
	if split[1] != '.pdf':
		raise IOError('Final filename must have extension ''pdf'', requested: {}'.format(filename))

	# ======================================
	# Get final destination
	# ======================================
	final_path = os.path.abspath(filename)
	try:
		os.mkdir(os.path.dirname(final_path))
	except OSError as e:
		if e.errno != 17:
			raise
	
	# ======================================
	# Get current directory
	# ======================================
	cwd = os.getcwdu()

	# ======================================
	# Create info to write
	# ======================================
	template=r'''
\documentclass[10pt]{{article}}
\usepackage{{amssymb,amsmath,booktabs,multirow}}

\pagestyle{{empty}}

\begin{{document}}
\begin{{{environment}}}{env_curly}
{textstr}
\end{{{environment}}}
\end{{document}}
'''
	if env_curly!=None:
		env_curly = '{{{}}}'.format(env_curly)
	else:
		env_curly = ''

	fullwrite=template.format(textstr=textstr,environment=environment,env_curly=env_curly)

	# ======================================
	# Get file names for intermediate files
	# ======================================
	tempdir  = 'temp_latex'
	tempfile = 'temp.tex'
	split = os.path.splitext(tempfile)
	pdffile  = '{}.{}'.format(split[0],'pdf')
	cropfile = '{}-crop.{}'.format(split[0],'pdf')

	# ======================================
	# Delete and remake temp directory
	# ======================================
	try:
		shutil.rmtree(tempdir)
	except OSError as e:
		if e.errno!=2:
			raise
	os.mkdir(tempdir)

	# ======================================
	# Create temporary file
	# ======================================
	f=open(os.path.join(tempdir,tempfile),'w+')
	f.write(fullwrite)
	f.close()

	# ======================================
	# Compile figure
	# ======================================
	os.chdir(tempdir)

	command = 'latexmk {} -pdf'.format(tempfile)
	args = shlex.split(command)
	subprocess.call(args)

	command = 'pdfcrop {} {}'.format(pdffile,cropfile)
	args = shlex.split(command)
	subprocess.call(args)

	# ======================================
	# Move figure to correct location
	# ======================================
	shutil.move(cropfile,final_path)

	# ======================================
	# Clean up
	# ======================================
	os.chdir(cwd)
	shutil.rmtree(tempdir)
