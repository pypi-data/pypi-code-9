import zipfile
import contextlib
import os

from .. import results, lists
from .xmlparser import parse_xml
from .document_xml import read_document_xml_element
from .content_types_xml import read_content_types_xml_element
from .relationships_xml import read_relationships_xml_element, Relationships
from .numbering_xml import read_numbering_xml_element, Numbering
from .styles_xml import read_styles_xml_element
from .notes_xml import create_footnotes_reader, create_endnotes_reader
from .files import Files
from . import body_xml


_namespaces = [
    ("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main"),
    ("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"),
    ("a", "http://schemas.openxmlformats.org/drawingml/2006/main"),
    ("pic", "http://schemas.openxmlformats.org/drawingml/2006/picture"),
    ("content-types", "http://schemas.openxmlformats.org/package/2006/content-types"),
    ("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships"),
    ("relationships", "http://schemas.openxmlformats.org/package/2006/relationships"),
    ("v", "urn:schemas-microsoft-com:vml"),
    ("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006"),
]

def read(fileobj):
    zip_file = zipfile.ZipFile(fileobj)
    body_readers = _body_readers(getattr(fileobj, "name"), zip_file)
    
    return _read_notes(zip_file, body_readers).bind(lambda notes:
        _read_document(zip_file, body_readers, notes))


def _read_notes(zip_file, body_readers):
    empty_result = results.success([])
    
    read_footnotes_xml = create_footnotes_reader(body_readers("footnotes"))
    footnotes = _try_read_entry_or_default(
        zip_file, "word/footnotes.xml", read_footnotes_xml, default=empty_result)
    
    read_endnotes_xml = create_endnotes_reader(body_readers("endnotes"))
    endnotes = _try_read_entry_or_default(
        zip_file, "word/endnotes.xml", read_endnotes_xml, default=empty_result)
    
    return results.combine([footnotes, endnotes]).map(lists.collect)
    
def _read_document(zip_file, body_readers, notes):
    with _open_entry(zip_file, "word/document.xml") as document_fileobj:
        document_xml = _parse_docx_xml(document_fileobj)
        return read_document_xml_element(
            document_xml,
            body_reader=body_readers("document"),
            notes=notes,
        )


def _body_readers(document_path, zip_file):
    with _open_entry(zip_file, "[Content_Types].xml") as content_types_fileobj:
        content_types = read_content_types_xml_element(_parse_docx_xml(content_types_fileobj))

    numbering = _try_read_entry_or_default(
        zip_file, "word/numbering.xml", read_numbering_xml_element, default=Numbering({}))
    
    with _open_entry(zip_file, "word/styles.xml") as styles_fileobj:
        styles = read_styles_xml_element(_parse_docx_xml(styles_fileobj))
    
    def for_name(name):
        relationships_path = "word/_rels/{0}.xml.rels".format(name)
        relationships = _try_read_entry_or_default(
            zip_file, relationships_path, read_relationships_xml_element,
            default=Relationships({}))
            
        return body_xml.reader(
            numbering=numbering,
            content_types=content_types,
            relationships=relationships,
            styles=styles,
            docx_file=zip_file,
            files=Files(os.path.dirname(document_path)),
        )
    
    return for_name


def _parse_docx_xml(fileobj):
    return parse_xml(fileobj, _namespaces)


@contextlib.contextmanager
def _open_entry(zip_file, name):
    entry = zip_file.open(name)
    try:
        yield entry
    finally:
        entry.close()


def _try_read_entry_or_default(zip_file, name, reader, default):
    if _has_entry(zip_file, name):
        with _open_entry(zip_file, name) as fileobj:
            return reader(_parse_docx_xml(fileobj))
    else:
        return default


def _has_entry(zip_file, name):
    try:
        zip_file.getinfo(name)
        return True
    except KeyError:
        return False
