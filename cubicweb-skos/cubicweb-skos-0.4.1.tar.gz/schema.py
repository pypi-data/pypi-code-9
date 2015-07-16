# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-skos schema"""

from yams.buildobjs import (EntityType, RelationDefinition, ComputedRelation,
                            String, RichString)

from cubicweb.schema import RQLConstraint, RRQLExpression


_ = unicode


class ConceptScheme(EntityType):
    """Vocabulary made of concepts"""
    title = String(unique=True)
    description = RichString()


class Concept(EntityType):
    """Unit of thought: idea, meaning, or (category of) object(s) and event(s)"""
    # URI of the concept is stored in the standard cwuri attribute
    definition = RichString(fulltextindexed=True)
    example = RichString()


class Label(EntityType):
    """Expression used to refer to a concept in natural language"""
    __unique_together__ = [('language_code', 'pref_label_of')]
    label = String(required=True, fulltextindexed=True)
    language_code = String(maxsize=5,
                           description=_('language code, e.g. "en" or "fr-fr"'))


class in_scheme(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'delete': (RRQLExpression('O cw_source SO, SO name = "system"'), ),
        'add': (RRQLExpression('O cw_source SO, SO name = "system"'), ),
    }
    subject = 'Concept'
    object = 'ConceptScheme'
    cardinality = '+*'
    composite = 'object'
    description = _('scheme the concept has been attached to')


class pref_label_of(RelationDefinition):
    subject = 'Label'
    object = 'Concept'
    cardinality = '?+'
    inlined = True
    composite = 'object'
    description = _('concept preferred label')
    fulltext_container = 'object'
    constraints = [
        RQLConstraint('NOT EXISTS(S alt_label_of O)',
                      msg=_("can't apply twice a label on a concept")),
        RQLConstraint('NOT EXISTS(S hidden_label_of O)',
                      msg=_("can't apply twice a label on a concept"))]

class pref_label(ComputedRelation):
    rule  = 'O pref_label_of S'


class alt_label_of(RelationDefinition):
    subject = 'Label'
    object = 'Concept'
    cardinality = '?*'
    inlined = True
    composite = 'object'
    description = _('concept alternative label')
    fulltext_container = 'object'
    constraints = [
        RQLConstraint('NOT EXISTS(S pref_label_of O)',
                      msg=_("can't apply twice a label on a concept")),
        RQLConstraint('NOT EXISTS(S hidden_label_of O)',
                      msg=_("can't apply twice a label on a concept"))]

class alt_label(ComputedRelation):
    rule  = 'O alt_label_of S'


class hidden_label_of(RelationDefinition):
    subject = 'Label'
    object = 'Concept'
    cardinality = '?*'
    inlined = True
    composite = 'object'
    description = _('concept hidden label')
    fulltext_container = 'object'
    constraints = [
        RQLConstraint('NOT EXISTS(S pref_label_of O)',
                      msg=_("can't apply twice a label on a concept")),
        RQLConstraint('NOT EXISTS(S alt_label_of O)',
                      msg=_("can't apply twice a label on a concept"))]

class hidden_label(ComputedRelation):
    rule  = 'O hidden_label_of S'


class broader_concept(RelationDefinition):
    subject = 'Concept'
    object = 'Concept'
    cardinality = '**'
    description = _('more general concept')
    constraints = [RQLConstraint('S in_scheme CS, O in_scheme CS')]


class narrower_concept(ComputedRelation):
    rule  = 'O broader_concept S'


class related_concept(RelationDefinition):
    subject = 'Concept'
    object = 'Concept'
    description = _('related concept')
    symmetric = True
    constraints = [RQLConstraint('S in_scheme CS, O in_scheme CS')]


class exact_match(RelationDefinition):
    subject = 'Concept'
    object = ('Concept', 'ExternalUri')
    description = _('equivalent concept in another vocabulary')
    symmetric = True


class close_match(RelationDefinition):
    subject = 'Concept'
    object = ('Concept', 'ExternalUri')
    description = _('close concept in another vocabulary')


class SKOSSource(EntityType):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', ),
        'update': ('managers', ),
        'delete': ('managers', ),
    }
    # description are the same as for CWSource attributes hence shouldn't be marked for translation
    # here
    name = String(required=True, unique=True, maxsize=128,
                  description='name of the source')
    url = String(description='URLs from which content will be imported. You can put one url per line')


class through_cw_source(RelationDefinition):
    __permissions__ = {'read': ('managers', 'users'),
                       'add': (),
                       'delete': ()}
    subject = 'SKOSSource'
    object = 'CWSource'
    cardinality = '1*'
    composite = 'subject'
    inlined = True
