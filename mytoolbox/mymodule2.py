"""
Module containing a class derived from another class.
"""
from mytoolbox.mymodule1 import myClass1
import click
import click.decorators


class myClass2(myClass1):
    """Derived class showing members from base class."""
    pass


@_data.command(name='create')
@click.argument("title", required=True)
@click.option("-a", "--alias", type=str, required=False,
              help="Record alias.")
@click.option("-d", "--description",type=str,required=False,
              help="Description text.")
@click.option("-k", "--keywords", type=str, required=False,
              help="Keywords (comma separated list).")
@click.option("-r", "--raw-data-file",type=str, required=False,
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
