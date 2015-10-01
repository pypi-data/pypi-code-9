import tinycss
import rules


def lint_css(css):
    violations = []
    css_rules = tinycss.make_parser().parse_stylesheet(css).rules
    for rule in css_rules:
        for declaration in rule.declarations:
            css_selector = rule.selector.as_css()
            prop = declaration.name
            value = " ".join([v.as_css() for v in declaration.value])
            clients_without_support = get_clients_without_support(declaration)
            if clients_without_support:
                clients = " | ".join(clients_without_support)
                warning = "Invalid Rule: {} {{ {}: {}; }} -- {}".format(css_selector, prop, value, clients)

                violations.append(warning)

    return violations

# uses https://www.campaignmonitor.com/css/
def get_clients_without_support(declaration):
    return rules.INVALID_PROPERTIES.get(declaration.name)
