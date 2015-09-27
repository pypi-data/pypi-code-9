from djangoUtils.styles.generator.units import Px,Pt,Em


def messageBoxCss(ss,textColour,backgroundColour,borderColour,errorTextColour,successTextColour):
    s=ss.addStyle('.messages_messageBox')
    s.padding='0.5em'
    s.margin='0.75em 0em 0.1em 0em'
    s.border='1px solid '+borderColour
    s.background=backgroundColour
    s.color=textColour

    s=ss.addStyle('.messages_messageBox .error')
    s.color=errorTextColour

    s=ss.addStyle('.messages_messageBox .success')
    s.color=successTextColour
