import kubetemplate.compile
import argh

def main():
    p = argh.ArghParser(description='Kubetemplate: kubernetes specific helpers and jinja templating', epilog='TODO:put-teh-gihub')

    argh.set_default_command(p, kubetemplate.compile.compile)

    p.dispatch()
