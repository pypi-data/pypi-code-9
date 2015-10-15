from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from binascii import hexlify
from hashlib import sha1
import os
import pkg_resources
import re

# Use gevent greenlet-local if available, otherwise use normal thread-local
try:
    from gevent.local import local
except ImportError:
    from threading import local


from immunio.logger import log
from immunio.patcher import monkeypatch


# Match Immunio placeholders like {immunio-var:0:1234}
PLACEHOLDER_REGEX = re.compile(r"\{\/?immunio-var:[0-9]+:[0-9a-fA-F]{4}\}")


# Give a name to this plugin so it can be enabled and disabled.
NAME = "xss_jinja2"


def add_hooks(run_hook, get_agent_func=None):
    """
    Add hooks to Jinja2
    """
    try:
        # TODO Verify error cases, what kind of errors are thrown?
        version = pkg_resources.get_distribution("Jinja2").version
    except:
        version = None

    meta = {
        "version": version
    }


    # Add our custom parser node
    add_immunio_var_node()
    # Hook the template parse and compile stages
    add_compiler_hooks()
    # Hook the actual rendering
    add_template_render_hook(run_hook)

    return meta


def add_immunio_var_node():
    """
    Adds a new Node type to Jinja2's parser.

    Jinja2 tries to prevent people from defining new node types by removing
    the __new__ method at the end of the nodes.py file. Unfortunately, we do
    need our own node type, so we have to work around the restriction by
    temporarily replacing the __new__ function, adding our node type, then
    putting everything back the way it was.
    """

    try:
        import jinja2.nodes
    except ImportError:
        return None

    @monkeypatch("jinja2.nodes.NodeType.__new__")
    def _copy_of_real_new(orig, cls, name, bases, d):
        """
        This is an exact copy of the `__new__()` method of
        jinja2.nodes.NodeType.
        """
        for attr in 'fields', 'attributes':
            storage = []
            storage.extend(getattr(bases[0], attr, ()))
            storage.extend(d.get(attr, ()))
            assert len(bases) == 1, 'multiple inheritance not allowed'
            assert len(storage) == len(set(storage)), 'layout conflict'
            d[attr] = tuple(storage)
        d.setdefault('abstract', False)
        return type.__new__(cls, name, bases, d)

    # Define our new Node type
    class ImmunioVarNode(jinja2.nodes.Expr):
        fields = ('node', 'var_definition_index')

    # And save our new node type into the module
    jinja2.nodes.ImmunioVarNode = ImmunioVarNode

    # Now unwrap __new__ to replace the previous 'disabled' version
    jinja2.nodes.NodeType.__new__.immunio_unwrap()


def add_compiler_hooks():
    """
    MonkeyPatch the template parser and the code generate to inject
    ImmunioVarNode wrappers around template variable expressions
    (anything wrapped in `{{ }}`) to collect data every time the
    template is rendered..

    This function handles everything from the template source up to the
    compiled template. The compiled code is handled by the
    `add_template_render_hook()` function.
    """
    try:
        import jinja2.parser
        import jinja2.nodes
    except ImportError:
        return None


    @monkeypatch("jinja2.parser.Parser.__init__")
    def _init(orig, parser_self, environment, source, name, filename,
              *args, **kwargs):
        """
        The goal here is to hash the template source and grab the
        filename. Stick the values on the instance so we can get them
        again when we parse the template.
        """
        # Calculate the SHA1 of the template source code
        source_bytes = source
        if isinstance(source_bytes, unicode):
            # Any unicode should be converted to bytes (as utf8)
            source_bytes = source_bytes.encode("utf8")
        parser_self._immunio_template_sha = sha1(source_bytes).hexdigest()

        # Prefer the `name`, but fall back to <template> if nothings better
        # is available.
        parser_self._immunio_template_name = name or filename or "<template>"

        return orig(parser_self, environment, source, name, filename,
                    *args, **kwargs)


    # Add extra fields to the template node
    jinja2.nodes.Template.fields = ('body', '_immunio_template_sha',
                                    '_immunio_template_name')


    @monkeypatch("jinja2.parser.Parser.parse")
    def _parse(orig, parser_self, *args, **kwargs):
        """
        Here we just copied the existing implementation here instead of
        calling the original. This gives us access to the `Template`
        instantiation.

        The goal here is to add our two extra parameters (source sha and
        name) to the Template node. We modified the Template node just
        above to accept the additional fields. When we compile the template
        we will inject these two extra variables into the generated source
        code.

        We also reset the `_immunio_var_counter` so we can give each
        template expression a unique id that stays constant between renders
        and doesn't change due to conditionals or loops.
        """
        # Initialize the variable definition counter to 0 for this template
        parser_self._immunio_var_counter = 0

        # Everything below is a copy of the original, except `nodes.Template`
        # has two extra immunio-specific arguments
        result = jinja2.nodes.Template(
            parser_self.subparse(),
            parser_self._immunio_template_sha,
            parser_self._immunio_template_name,
            lineno=1)
        result.set_environment(parser_self.environment)
        return result


    @monkeypatch("jinja2.parser.Parser.subparse")
    def _subparse(orig, parser_self, *args, **kwargs):
        """
        Here we loop through all the nodes in the subparse result and wrap
        all expressions (except constants) with an ImmunioVarNode.

        The ImmunioVarNode doesn't render anything, but it allows us to
        pass through additional metadata during the rendering process.
        It also provides and overall group for more complex expressions
        that are inside a single {{ }}.
        """
        # Call original function
        nodes = orig(parser_self, *args, **kwargs)
        # Loop through each node looking for expressions
        for node in nodes:
            if isinstance(node, jinja2.nodes.Output):
                for i, subnode in enumerate(node.nodes):
                    # Find all the expression nodes (except literal constants)
                    if (isinstance(subnode, jinja2.nodes.Expr) and
                            not isinstance(subnode, jinja2.nodes.Literal)):
                        # Wrap the expression node with our ImmunioVarNode
                        # Include the var counter as well.
                        node.nodes[i] = jinja2.nodes.ImmunioVarNode(
                            subnode, parser_self._immunio_var_counter)
                        parser_self._immunio_var_counter += 1
        return nodes


    @monkeypatch("jinja2.compiler.CodeGenerator.visit_Template")
    def _visit_template(orig, codegen_self, node, *args, **kwargs):
        """
        Wraps the original `visit_Template` to give us a chance to write
        two values into the global scope of the generated source code.

        This makes the template sha and the template name available
        anywhere within the generated source code.
        """
        result = orig(codegen_self, node, *args, **kwargs)
        # Add some special Immunio variables at the end
        codegen_self.writeline("# Additional metadata added by Immunio")
        codegen_self.writeline(
            "_immunio_template_sha = '%s'" % node._immunio_template_sha)
        codegen_self.writeline(
            "_immunio_template_name = '%s'" % node._immunio_template_name)
        return result


    def visit_ImmunioVarNode(self, node, frame):
        """
        Handle our completely custom node type when generating compiled code.

        The main idea is to "bake in" all the metadata about the template
        before it gets compiled to bytecode. This allows byte-code caching,
        provided by Jinja2 to work as expected - all the required info
        is part of the compiled source.

        The `_immunio_var` method is defined below.
        """
        # Use `context.environment` instead of just `environment` to ensure
        # we get the _immunio_var set by the `new_context` wrapper above.
        self.write("context.environment._immunio_var(")
        # Get the original code for our sub-node
        self.visit(node.node, frame)
        # Add the template sha and name from the global scope (added by
        # our custom Template node and patched visit_Template function).
        self.write(", ")
        self.write("_immunio_template_sha, ")
        self.write("_immunio_template_name, ")
        # Bake in the variable index within the template, and the line number.
        self.write("%d, " % node.var_definition_index)
        self.write("%s" % node.node.lineno)
        self.write(')')
    # Add it to the CodeGenerator.
    jinja2.compiler.CodeGenerator.visit_ImmunioVarNode = visit_ImmunioVarNode


def add_template_render_hook(run_hook):
    """
    Add a hook as early as possible in the Pyramid request flow to extract
    the user_id making the request. This is required because normally the
    user is not loaded unless the app-code actually requests it.
    """
    try:
        import jinja2.environment
        import jinja2.parser
        import jinja2.nodes
    except ImportError:
        return None

    local_storage = local()


    @monkeypatch(jinja2.environment.Template, "_from_namespace")
    def _from_namespace(orig, template_cls, environment, namespace,
                        *args, **kwargs):
        """
        Here we just need to grab a copy of the template name and sha, so
        we can use them for the top-level render metadata.
        """
        result = orig(template_cls, environment, namespace, *args, **kwargs)
        # Grab our special immunio data.
        result._immunio_template_name = namespace["_immunio_template_name"]
        result._immunio_template_sha = namespace["_immunio_template_sha"]
        return result


    @monkeypatch("jinja2.environment.Template.new_context")
    def _init(orig, *args, **kwargs):
        """
        Ensure that the `_immunio_var()` method (defined below) is
        accessible from within our template code.
        """
        context = orig(*args, **kwargs)
        context.environment._immunio_var = immunio_var
        return context


    def immunio_var(val, template_sha, filename, var_definition_index, lineno):
        """
        This helper method is called once for every variable injected
        into a page. The data is recorded and used to add our
        `immunio-var` tags to the output.
        """
        # Get a unique id for this variable replacement.
        var_instance_index = local_storage.var_instance_index
        local_storage.var_instance_index += 1

        # Grab the rendering nonce - this changes for every render.
        nonce = local_storage.render_nonce

        # Record metadata about the particular variable.
        var = {
            "template_sha": template_sha,
            "template_id": str(var_definition_index),
            "nonce": nonce,
            "code": "",
            "file": filename,
            "line": lineno,
        }
        local_storage.var_meta[str(var_instance_index)] = var

        # Wrap the value in our tags
        tag_body = "immunio-var:%d:%s" % (var_instance_index, nonce)

        return "{%(tag_body)s}%(val)s{/%(tag_body)s}" % {
            "val": val,
            "tag_body": tag_body,
        }


    @monkeypatch("jinja2.environment.Template.render")
    def _render(orig, template_self, *args, **kwargs):
        """
        Wrap the render function to track all the details for each
        rendering.
        """
        log.debug(
            "inja2.environment.Template.render"
            "(%(args)s, %(kwargs)s)", {
                "args": args,
                "kwargs": kwargs,
                })

        # If the first time through, make sure our local storage
        # variables are present.
        if not hasattr(local_storage, "render_depth"):
            local_storage.render_depth = 0

        # If this is our main rendering starting, reset a few variables
        if local_storage.render_depth == 0:
            local_storage.var_instance_index = 0
            local_storage.var_meta = {}
            # Generate a new nonce for this rendering
            local_storage.render_nonce = hexlify(os.urandom(2))

        # Now run the original rendering. Increment and decrement the
        # depth counter to handle any nested renderings.
        local_storage.render_depth += 1
        result = orig(template_self, *args, **kwargs)
        local_storage.render_depth -= 1

        # If this full rendering is done, call run_hook with all the data.
        if local_storage.render_depth == 0:
            hook_result = run_hook("template_render_done", {
                "rendered": result,
                "template_sha": template_self._immunio_template_sha,
                "name": template_self._immunio_template_name,
                "origin": template_self.filename,
                "nonce": local_storage.render_nonce,
                "vars": local_storage.var_meta,
            })

            # If hook overrides result, use `rendered` otherwise use the
            # original.
            result = hook_result.get("rendered", result)

            # If something goes wrong, the final_result may contain some immunio
            # placeholders. As a double check, ensure they are all removed.
            result = PLACEHOLDER_REGEX.sub("", result)
        return result
