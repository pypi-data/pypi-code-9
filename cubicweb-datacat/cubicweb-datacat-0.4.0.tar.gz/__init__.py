"""cubicweb-datacat application package

Data catalog
"""


def register_catalog_rdf_mapping(reg):
    """Register mapping between DCAT RDF vocabulary and DataCatalog entity type."""
    reg.register_prefix('dcat', 'http://www.w3.org/ns/dcat#')
    reg.register_prefix('dcterms', 'http://purl.org/dc/terms/')
    reg.register_etype_equivalence('DataCatalog', 'dcat:Catalog')
    reg.register_attribute_equivalence('DataCatalog', 'title', 'dcterms:title')
    reg.register_attribute_equivalence('DataCatalog', 'description', 'dcterms:description')
    reg.register_attribute_equivalence('DataCatalog', 'issued', 'dcterms:issued')
    reg.register_attribute_equivalence('DataCatalog', 'modified', 'dcterms:modified')
    reg.register_relation_equivalence('DataCatalog', 'catalog_publisher', 'Agent',
                                      'dcterms:publisher')
    reg.register_relation_equivalence('DataCatalog', 'theme_taxonomy', 'ConceptScheme',
                                      'dcat:themeTaxonomy')
    reg.register_relation_equivalence('Dataset', 'in_catalog', 'DataCatalog', 'dcat:dataset',
                                      reverse=True)


def register_dataset_rdf_mapping(reg):
    """Register mapping between DCAT RDF vocabulary and Dataset entity type."""
    reg.register_prefix('dcat', 'http://www.w3.org/ns/dcat#')
    reg.register_prefix('dcterms', 'http://purl.org/dc/terms/')
    reg.register_prefix('adms', 'http://www.w3.org/ns/adms#')
    reg.register_etype_equivalence('Dataset', 'dcat:Dataset')
    reg.register_attribute_equivalence('Dataset', 'title', 'dcterms:title')
    reg.register_attribute_equivalence('Dataset', 'description', 'dcterms:description')
    reg.register_attribute_equivalence('Dataset', 'issued', 'dcterms:issued')
    reg.register_attribute_equivalence('Dataset', 'modified', 'dcterms:modified')
    reg.register_attribute_equivalence('Dataset', 'identifier', 'adms:identifier')
    reg.register_relation_equivalence('Dataset', 'in_catalog', 'DataCatalog', 'dcat:dataset',
                                      reverse=True)
    reg.register_relation_equivalence('Dataset', 'dataset_publisher', 'Agent',
                                      'dcterms:publisher')
    reg.register_relation_equivalence('Dataset', 'dataset_contact_point', 'Agent',
                                      'dcat:contactPoint')
    reg.register_relation_equivalence('Distribution', 'of_dataset', 'Dataset', 'dcat:distribution',
                                      reverse=True)


def register_distribution_rdf_mapping(reg):
    """Register mapping between DCAT RDF vocabulary and Distribution entity type."""
    reg.register_prefix('dcat', 'http://www.w3.org/ns/dcat#')
    reg.register_prefix('dcterms', 'http://purl.org/dc/terms/')
    reg.register_etype_equivalence('Distribution', 'dcat:Distribution')
    reg.register_attribute_equivalence('Distribution', 'title', 'dcterms:title')
    reg.register_attribute_equivalence('Distribution', 'description', 'dcterms:description')
    reg.register_attribute_equivalence('Distribution', 'issued', 'dcterms:issued')
    reg.register_attribute_equivalence('Distribution', 'modified', 'dcterms:modified')
    reg.register_relation_equivalence('Distribution', 'of_dataset', 'Dataset', 'dcat:distribution',
                                      reverse=True)


def register_publisher_rdf_mapping(reg):
    """Register mapping between FOAF RDF vocabulary and Agent entity type."""
    reg.register_prefix('foaf', 'http://xmlns.com/foaf/0.1/')
    reg.register_prefix('dcterms', 'http://purl.org/dc/terms/')
    reg.register_etype_equivalence('Agent', 'foaf:Agent')
    reg.register_attribute_equivalence('Agent', 'name', 'foaf:name')
    reg.register_relation_equivalence('Dataset', 'dataset_publisher', 'Agent',
                                      'dcterms:publisher')


def register_contact_point_rdf_mapping(reg):
    """Register mapping between VCard RDF vocabulary and Agent entity type."""
    reg.register_prefix('vcard', 'http://www.w3.org/2006/vcard/ns#')
    reg.register_prefix('dcat', 'http://www.w3.org/ns/dcat#')
    reg.register_relation_equivalence('Dataset', 'dataset_contact_point', 'Agent',
                                      'dcat:contactPoint')
    reg.register_etype_equivalence('Agent', 'vcard:Kind')
    reg.register_attribute_equivalence('Agent', 'name', 'vcard:fn')
