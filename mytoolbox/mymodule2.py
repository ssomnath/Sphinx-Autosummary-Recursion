"""
Module containing a class derived from another class.
"""
from mytoolbox.mymodule1 import myClass1
import click
import click.decorators


# =============================================================================
# ------------------------------------ Click Classes, Decorators, and Callbacks
# =============================================================================

# @cond

# Aliases click commands
class _AliasedGroup(click.Group):
    # Allows command matching by unique suffix
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]

        if not matches:
            # Cmd was not found - might be an invalid option
            if cmd_name[:1]=="-":
                raise Exception("Invalid option: " + cmd_name)
            # Or not, unknown command
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

    # This is to work-around a help bug in click production code
    def resolve_command(self, ctx, args):
        cmd_name, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args


# Same as AliasGroup but checks for global aliases
class _AliasedGroupRoot(_AliasedGroup):
    def get_command(self, ctx, cmd_name):
        if cmd_name == "dir":
            return _list
        elif cmd_name == "cd":
            return _wc
        elif cmd_name == "?":
            return _help_cli

        return super().get_command( ctx, cmd_name )


class _NoCommand(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

# @endcond


def _set_script_cb(ctx, param, value):
    global _interactive
    global _output_mode_sticky
    global _output_mode

    if value:
        _interactive = False
        _output_mode_sticky = _OM_JSON
        _output_mode = _OM_JSON


def _set_verbosity_cb(ctx, param, value):
    global _verbosity

    if value:
        _verbosity = int(value)


__global_context_options = [
    click.option('-X', '--context', required=False, type=str,
                 help="User or project ID for command alias context. See "
                      "'alias' command help for more information."),
    ]


# Decorator to add context option to click commands
def _global_context_options(func):
    for option in __global_context_options:
        func = option(func)
    return func


__global_output_options = [
    click.option('-v', '--verbosity', type=click.Choice(['0', '1', '2']),
                 callback=_set_verbosity_cb, expose_value=False,
                 help='Verbosity level of output'),
    ]


# Decorator to add output options to click commands
def _global_output_options(func):
    for option in reversed(__global_output_options):
        func = option(func)
    return func

# =============================================================================
# -------------------------------------------------- Click Entry Point Function
# =============================================================================


@click.group(cls=_AliasedGroupRoot, invoke_without_command=True,
             context_settings=_ctxt_settings)
@click.option("-m", "--manual-auth", is_flag=True,
              help="Force manual authentication")
@click.option("-s", "--script", is_flag=True, is_eager=True,
              callback=_set_script_cb,
              help="Start in non-interactive scripting mode. Output is in JSON"
                   ", all intermediate I/O is disabled, and certain "
                   "client-side commands are unavailable.")
@click.option("--version", is_flag=True,
              help="Print version number and exit.")
@click.pass_context
def _cli(ctx, *args, **kwargs):
    """'datafed' is the command-line interface (_cli) for the DataFed federated data management
    service. This _cli may be used to access most, but not all, of the features available
    via the DataFed web portal. This _cli may be used interactively (-i option), or for
    scripting (supports JSON output with the -J option).
    For more information about this _cli and DataFed in general, refer to https://datafed.ornl.gov/ui/docs
    """
    pass


# =============================================================================
# --------------------------------------------------------- CLI State Functions
# =============================================================================

@_cli.command(name='gendoc',hidden=True)
@click.pass_context
def _genDoc( ctx ):
    toc = []

    #print( _cli.get_help( ctx.parent ), "\n" )

    body = "<h1 id='main'>Main</h1>\n\n<pre>" + _cli.get_help( ctx.parent ) + "</pre>\n"
    toc.append("<a href='#main'>Main</a>")

    sec = 1
    for c in _cli.list_commands( ctx ):
        subcmd = _cli.get_command( _cli, c )
        if not subcmd.hidden:
            body = body + _genDocCmd( subcmd, click.Context( subcmd, info_name = subcmd.name, parent=ctx.parent ), str(sec), "", 2, toc )
            sec = sec + 1

    _toc = ""
    for t in toc:
        _toc = _toc + t + "<br>\n"

    print("<html><head><title>DataFed CLI Help</title></head><body style='margin:0;padding:0'><div style='display:flex;flex-direction:column;height:100%;width:100%'><div style='flex:none;background:#4040bb;color:#ffffff;padding:.5em'><span style='font-size:2em'>DataFed Command Line Interface Help</span>&nbsp&nbsp&nbsp&nbspCLI V-{}<br>This documentation is automatically generated from the latest released DataFed CLI, available as the 'datafed' package on PyPi.</div><div style='flex:1 1 auto;display:flex;flex-direction:row;min-height:0'><div style='flex:none;overflow:auto;padding:.25em;background:#bbbbbb'>{}</div><div style='flex:1 1 auto;overflow:auto;padding: 0em 2em 0em 2em'>{}</div></div></div></body></html>".format( version, _toc, body ))


def _genDocCmd( cmd, ctx, section, path, hlev, toc ):
    if hasattr( cmd, 'list_commands' ):
        is_group = True
    else:
        is_group = False

    cname = cmd.name.capitalize()
    html = "\n<h{} id='s{}'>{} {}{}{}</h{}>\n\n<pre>".format(hlev,section,section,path,cname," Commands" if is_group else "",hlev) + cmd.get_help( ctx ) + "</pre>\n"
    toc.append("<a href='#s{}'>{} {}{}{}</a>".format(section,section,path,cname," Commands" if is_group else ""))

    if is_group:
        sec = 1
        for c in cmd.list_commands( ctx ):
            subcmd = cmd.get_command( cmd, c )
            if not subcmd.hidden:
                html = html + _genDocCmd( subcmd, click.Context( subcmd, info_name = subcmd.name, parent=ctx ), section + "." + str(sec), path + cname + " ", hlev + 1, toc )
                sec = sec + 1

    return html


@_cli.command(name='data', cls=_AliasedGroup, help="Data subcommands.")
def _data():
    pass


@_data.command(name='create')
@click.argument("title", required=True)
@click.option("-a", "--alias", type=str, required=False,
              help="Record alias.")
@click.option("-d", "--description", type=str, required=False,
              help="Description text.")
@click.option("-k", "--keywords", type=str, required=False,
              help="Keywords (comma separated list).")
@click.option("-r", "--raw-data-file", type=str, required=False,
              help="Globus path to raw data file (local or remote) to upload"
                   " to new record. Default endpoint is used if none provided"
                   ".")
@click.option("-x", "--extension", type=str, required=False,
              help="Override raw data file extension if provided (default is"
                   " auto detect).")
@click.option("-m", "--metadata", type=str, required=False,
              help="Inline metadata in JSON format. JSON must define an object"
                   " type. Cannot be specified with --metadata-file option.")
@click.option("-f", "--metadata-file", type=str, required=False,
              help="Path to local metadata file containing JSON. JSON must "
                   "define an object type. Cannot be specified with --metadata"
                   " option.")
@click.option("-p", "--parent", type=str, required=False,
              help="Parent collection ID, alias, or listing index. Default is "
                   "the current working collection.")
@click.option("-R", "--repository", type=str, required=False,
              help="Repository ID. Uses default allocation if not specified.")
@click.option("-D", "--deps", multiple=True,
              type=click.Tuple([click.Choice(['der', 'comp', 'ver']), str]),
              help="Dependencies (provenance). Use one '--deps' option per "
                   "dependency and specify with a string consisting of the "
                   "type of relationship ('der', 'comp', 'ver') followed by "
                   "ID/alias of the referenced record. Relationship types are:"
                   " 'der' for 'derived from', 'comp' for 'a component of', "
                   "and 'ver' for 'a new version of'.")
@_global_context_options
@_global_output_options
def _dataCreate(title, alias, description, keywords, raw_data_file, extension,
                metadata, metadata_file, parent, repository, deps, context):
    """
    Create a new data record. The data record 'title' is required, but all
    other attributes are optional. On success, the ID of the created data
    record is returned. Note that if a parent collection is specified, and
    that collection belongs to a project or other collaborator, the creating
    user must have permission to write to that collection. The raw-data-file
    option is only supported in interactive mode and is provided as a
    convenience to avoid a separate dataPut() call.
    """
    pass


@_data.command(name='update')
@click.argument("data_id", metavar="ID", required=False)
@click.option("-t", "--title", type=str, required=False,
              help="Title")
@click.option("-a", "--alias", type=str, required=False,
              help="Alias")
@click.option("-d", "--description", type=str, required=False,
              help="Description text")
@click.option("-k", "--keywords", type=str, required=False,
              help="Keywords (comma separated list)")
@click.option("-r", "--raw-data-file", type=str, required=False,
              help="Globus path to raw data file (local or remote) to upload "
                   "with record. Default endpoint used if none provided.")
@click.option("-x", "--extension", type=str, required=False,
              help="Override extension for raw data file (default = auto "
                   "detect).")
@click.option("-m", "--metadata", type=str, required=False,
              help="Inline metadata in JSON format.")
@click.option("-f", "--metadata-file", type=str, required=False,
              help="Path to local metadata file containing JSON.")
@click.option("-S", "--metadata-set", is_flag=True, required=False,
              help="Set (replace) existing metadata with provided instead of "
                   "merging.")
@click.option("-A", "--deps-add", multiple=True, nargs=2,
              type=click.Tuple([click.Choice(['der', 'comp', 'ver']), str]),
              help="Specify dependencies to add by listing first the type of "
                   "relationship ('der', 'comp', or 'ver') follwed by ID/alias"
                   " of the target record. Can be specified multiple times.")
@click.option("-R", "--deps-rem", multiple=True, nargs=2,
              type=click.Tuple([click.Choice(['der', 'comp', 'ver']), str]),
              help="Specify dependencies to remove by listing first the type "
                   "of relationship ('der', 'comp', or 'ver') followed by "
                   "ID/alias of the target record. Can be specified multiple"
                   " times.")
@_global_context_options
@_global_output_options
def _dataUpdate(data_id, title, alias, description, keywords, raw_data_file,
                extension, metadata, metadata_file, metadata_set, deps_add,
                deps_rem, context):
    """
    Update an existing data record. The data record ID is required and can be
    an ID, alias, or listing index; all other record attributes are optional.
    The raw-data-file option is only supported in interactive mode and is
    provided as a convenience to avoid a separate dataPut() call.
    """
    pass


class myClass2(myClass1):
    """Derived class showing members from base class."""
    pass