# -*- coding: utf-8 -*-
"""
Created on Sun Jun 02 19:07:43 2013

Latex code templates for typesetting a spexdown script.

@author: Koos Zevenhoven
"""
from __future__ import unicode_literals, print_function, division

latex_preamble1 = """
\documentclass[a4paper,11pt,twocolumn]{article}
"""
#TODO can I get rid of color or wasysym (used for \twonotes and \eighthnote)

# Had to convert from byte string, as \u in \usepackage would be interpreted
# as a unicode code point escape. This problem will be gone in Py3k (PEP414)
latex_preamble2 = br"""

\makeatletter
\newcommand{\needspace}[1]{%
 { \begingroup
    \setlength{\dimen@}{#1}%
    \vskip\z@\@plus\dimen@
    \penalty -100\vskip\z@\@plus -\dimen@
    \vskip\dimen@
    \penalty 9999%
    \vskip -\dimen@
    \vskip\z@skip % hide the previous |\vskip| from |\addvspace|
  \endgroup}
}
\makeatother

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\usepackage[usenames]{color}
\usepackage{wasysym}

\addtolength\columnsep{0.5cm}
\usepackage[landscape, left=1.4cm, top=1.5cm, right=1.4cm, nohead]{geometry}

\newcommand{\scripttitle}[1]{
    \twocolumn
    {{\noindent { \texttt{\Huge #1}}}\vspace{3.5cm}\phantom{joo} \\ }
    \newpage
}

\newcommand{\hugetitle}[1]{\newpage
    \noindent \texttt{\Huge #1} \vspace{1.2cm}\phantom{joo} \\
}

\newcommand{\character}[2]{

    \noindent \texttt{#1}
    
    \setlength{\leftskip}{8mm}\nopagebreak
    \noindent #2
    
    \setlength{\leftskip}{0mm}

    \vspace{1mm}
    
}

\newcommand{\intermission}[1]{\vspace{\fill}\vspace{5mm}\begin{center}\texttt{\LARGE #1}
\end{center}\vspace{4mm}\vspace{\fill}}


\newcommand{\actlisting}[1]{
    \vspace{1.5mm}
    \noindent
    \begin{tabular}{@{}l@{}}%\hline\hline
    \begin{minipage}{\columnwidth}\vspace{1mm}
    \LARGE \bf \texttt{#1}\hfill
    \end{minipage}\\\hline\nopagebreak %\\hline
    \end{tabular}}

\newcommand{\acttitle}[1]{

    \newpage\noindent
    \begin{tabular}{@{}l@{}}\hline\hline
    \begin{minipage}{\columnwidth}\vspace{1mm}
    \LARGE \bf \texttt{#1}\hfill
    \end{minipage}\\\hline\hline
    \end{tabular}\nopagebreak}


\newcommand{\scenetitle}[3]{

    \vspace{0.4cm}
    \pagebreak[3]\begin{center}\needspace{3cm}\pagebreak[3]\framebox{\begin{minipage}{.87\columnwidth}
    {\Large \bf \texttt{#1}}
    #2
    
    \begingroup {\raggedleft\texttt{\small (#3)}\\*}\endgroup
    \end{minipage}}\nopagebreak\end{center}\nopagebreak}

\newcommand{\scenelisting}[3]{%
    \begin{center}\begin{minipage}{\columnwidth}
    {\Large \bf \texttt{#1}}
    #2
    
    \begingroup{\raggedleft\texttt{\small (#3)}\par}\endgroup
    \end{minipage}\end{center}
    
}


\newcommand{\anonymousblock}[1]{%
    \noindent
    \begin{minipage}[t]{1\columnwidth}\it
    #1
    %if(bufi >= bufsize)
    %\qed
    \end{minipage}\vspace{1.6mm}\par

}

\newcommand{\namedblock}[2]{%
    \noindent
    \begin{minipage}[t]{.22\columnwidth}\flushleft\noindent\textbf{#1\vfill}\end{minipage}
    \begin{minipage}[t]{.78\columnwidth} #2
    %if(bufi >= bufsize)
    %\qed
    \end{minipage}\vspace{1.3mm}\par
    
}

\newcommand{\musicblock}[2]{%
    \noindent
    \begin{minipage}[t]{.22\columnwidth}\flushright\noindent\textbf{#1\vfill}\end{minipage}
    \begin{minipage}[t]{.78\columnwidth} #2
    %if(bufi >= bufsize)
    %\qed
    \end{minipage}\vspace{1.3mm}\par

}

\flushbottom
\widowpenalty=1000
\clubpenalty=1000

\begin{document}
""".decode('ascii')

latex_end = r"""
\end{document}

"""

par_delimiter = "\n\n" r"\noindent\hspace{5mm}"
song_symbol = r"\twonotes "
music_symbol = r"\eighthnote "

VERSION = r"$spex\tau\epsilon\chi\,2\,beta$"

class Spextex(object):
    """An object for encoding spexcript elements into a latex source."""
    
    def __init__(self, language):
        self._lang = language
        self.latex_data = [latex_preamble1, 
                           self._lang.LATEX_PREAMBLE,
                           latex_preamble2]
        
    def final_result(self):
        self.latex_data.append(latex_end)
        return "".join(self.latex_data)
    
    def _process_string(self, string):
        #TODO handle underline emphasis somehow instead of just deleting
        replacements = [("_", r"{\textunderscore}"),
                        ("&", r"{\&}"),
                        ('" ', r'{"\ }')]
        for rep in replacements:
            string = string.replace(*rep)
        return string
        
    def _process_paragraphs(self, paragraphs):
        return [self._process_string(par) for par in paragraphs]
        
    def _format_paragraphs(self, paragraphs):
        return par_delimiter.join(self._process_paragraphs(paragraphs))

    def front_page(self, title):
        (SCRIPT, 
         TITLE, title,
         DATE, 
         OWNER_OF_COPY,
         SLOGAN, EXTRA) = map(self._process_string, 
                              (self._lang.SCRIPT, 
                               self._lang.TITLE, title,
                               self._lang.DATE,
                               self._lang.OWNER_OF_COPY,
                               self._lang.SLOGAN, self._lang.EXTRA))        
        
        self.latex_data.append(r"""
        \begin{titlepage}
            \vspace*{\fill}
            \begin{center}
                \vspace*{1cm}
                {\Huge \tt {""" + SCRIPT + r"""}\hspace*{5cm}\phantom{.}}\\
                \vspace{.3cm}
                \begin{tabular}{r|l}
                \Large """ + TITLE + r""" &{\Large \tt """ + title + r"""}\\
                \vspace{0.4cm}
                """ + DATE + r""" &{\tt \today}\\
                \end{tabular}
                \vspace{1.5cm}
                
                \hspace*{5cm}""" + OWNER_OF_COPY + r""" 
                """ "\\u" r"""nderline{""" + (r"\ " * 38) + r"""}\\

            \end{center}
            \vspace*{\fill}
            \flushright
                \small """ + VERSION + r""": """ + SLOGAN + r"""\\
                \tiny """ + EXTRA + r"""
        \end{titlepage}
        """)
        
    
    def paragraphs(self, paragraphs):
        paragraphs = self._format_paragraphs(paragraphs)
        self.latex_data.append(paragraphs)
    
    def characters_title(self):
        self.latex_data.append(r"\hugetitle{%s}" % 
                               self._process_string(self._lang.CHARACTERS))
    
    def listing_title(self):
        self.latex_data.append(r"\hugetitle{%s}" % 
                               self._process_string(self._lang.LIST_OF_SCENES))
        
        
    def character(self, display_name, full_name, description):
        full_name = self._process_string(full_name)
        if full_name != "":
            full_name = " (%s)" % full_name
        self.latex_data.append(r"\character{%s%s}{%s}" %
                               (self._process_string(display_name),
                                self._process_string(full_name),
                                self._format_paragraphs(description)))
    
    def music(self, names, paragraphs, style):
        postfix = r"$\;\;$"        
        char_delimiter = postfix + r"\\"

        if style == "song":
            prefix = song_symbol + r"\hfill "
        elif style == "music":
            prefix = music_symbol + r"\hfill "

        text = self._format_paragraphs(paragraphs) + "\n"
        self.latex_data.append(r"\musicblock{%s}{%s}" %  
            (prefix + 
             self._process_string(char_delimiter.join(names)) +
             postfix, text))
        
    def block(self, names, paragraphs):
        prefix = ""
        char_delimiter = r"\hspace{0.1mm}&\hspace{0.1mm}"
        postfix = ":"
        text = self._format_paragraphs(paragraphs) + "\n"
        if len(names) == 0:
            self.latex_data.append(r"\anonymousblock{%s}" % text)
        else:
            self.latex_data.append(r"\namedblock{%s}{%s}" %  
                (prefix + 
                 self._process_string(char_delimiter.join(names)) +
                 postfix, text))

    
    def scene(self, act, scene, title, people = [],
              description_pars = [], listing = False):
        if len(description_pars) > 0:
            descr = r"\\" + self._format_paragraphs(description_pars) + "\n"
        else:
            descr = ""
            
        def make_people_list():
            for cont, name in people:
                append = ""
                if "Music" in cont:
                    append += music_symbol
                if "Song" in cont:
                    append += song_symbol


                if name == "":
                    if append != "":
                        yield append
                else:
                    if append == "":
                        yield name
                    else:
                        yield name + " " + append
                
                    
        
        data = (self._process_string(self._lang.scene_title(act, 
                                                            scene, 
                                                            title)), 
                descr,
                ", ".join(make_people_list()))
        if listing:
            self.latex_data.append(r"\scenelisting{%s}{%s}{%s}" % data)
        else:
            self.latex_data.append(r"\scenetitle{%s}{%s}{%s}" % data)
        
    def scene_end(self):
        pass
        
    def act(self, number, title, listing = False):
        cmd = r"\acttitle{%s}" if not listing else r"\actlisting{%s}"
        self.latex_data.append(cmd % 
            self._lang.act_title(number, self._process_string(title)))

    def intermission(self):
        self.latex_data.append(r"\intermission{%s}" % self._lang.INTERMISSION)
    
    def script_title(self):
        self.latex_data.append(r"\scripttitle{%s}" % self._lang.SCRIPT)
        
PDFLATEX = r"C:\Program Files (x86)\MiKTeX 2.9\miktex\bin\pdflatex.exe"
#ACROREAD = r"C:\Program Files (x86)\Adobe\Reader 10.0\Reader\AcroRd32.exe"
PDFLATEX = 'pdflatex'
#ACROREAD = 'acroread'

def pdflatex(latex_unicode):
    with open(r"tmp/spex.tex", "w", encoding = 'utf8') as f:
        f.write(latex_unicode)
    from subprocess import Popen
    Popen(["pdflatex", r"spex.tex"], cwd = "tmp").wait()
    
def show():
    import os
    import os.path
    os.startfile(os.path.join("tmp", "spex.pdf"))
    
    
    
