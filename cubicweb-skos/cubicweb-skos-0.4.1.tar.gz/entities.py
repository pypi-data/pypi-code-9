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
"""cubicweb-skos entity classes"""

from logilab.common.decorators import cachedproperty

from cubicweb.predicates import is_instance
from cubicweb.entities import AnyEntity, fetch_config
from cubicweb.entities.adapters import ITreeAdapter


def _add_concept(scheme, label, language_code, **kwargs):
    cnx = scheme._cw
    concept = cnx.create_entity('Concept', in_scheme=scheme, **kwargs)
    cnx.create_entity('Label', label=label, language_code=language_code,
                      pref_label_of=concept)
    # hooks do use existing labels, clear cache here to ensure the label is considered
    concept.cw_clear_all_caches()
    return concept

class CSVParseError(Exception):
    """Error during CSV parsing, with a line information."""

    def __init__(self, line):
        super(CSVParseError, self).__init__()
        self.line = line


class CSVIndentationError(CSVParseError):
    """Invalid indentation (level was reduced by more than one indentation)."""


class CSVDecodeError(CSVParseError):
    """Decode exception, probably due to a wrongly specified encoding."""


class ConceptScheme(AnyEntity):
    __regid__ = 'ConceptScheme'
    fetch_attrs, cw_fetch_order = fetch_config(('title', 'cwuri'))

    def dc_title(self):
        if self.title:
            return self.title
        return self.cwuri

    @cachedproperty
    def top_concepts_rset(self):
        return self._cw.execute(
            'Any C,CU WHERE C cwuri CU, C in_scheme X, NOT C broader_concept SC, X eid %(x)s',
            {'x': self.eid})

    @property
    def top_concepts(self):
        return list(self.top_concepts_rset.entities())

    def add_concept(self, label, language_code=u'en', **kwargs):
        """Add a top-concept to this scheme"""
        return _add_concept(self, label, language_code, **kwargs)

    def add_concepts_from_file(self, stream, encoding, language_code, delimiter):
        """Read a stream and create the listed concepts inside the ConceptScheme

        'delimiters' are considered as hierarchical information. There must be a concept per line,
        each line starting by N delimiters (indicating the hierarchical level) or nothing if the
        concept has no parent.

        Example (delimiter = u';')
        titi
        ;toto
        ;;tata
        --> ok: titi is a top-concept of the scheme, toto is a narrower concept of titi, tata is a 
        narrower concept of toto

        titi
         ;toto
        --> 'titi' and ' ;toto' will be considered as two concepts of the scheme.
        """
        # This ordered list behaves like a state machine. It will contain all the concepts from
        # the conceptscheme to the more recent broader concept. The last element is consequently
        # the current parent concept. When de-indenting, the concepts are popped.
        level = -1
        broaderconcepts = [(self, level)]
        for nline, line in enumerate(stream, 1):
            try:
                line = line.rstrip().decode(encoding)
            except UnicodeDecodeError:
                raise CSVDecodeError(nline)
            if not line:
                continue
            # Find the label by removing leading delimiters (and spaces), then
            # remove trailing delimiters and spaces.
            label = line.lstrip(delimiter + ' ').rstrip(delimiter + ' ')
            if not label:
                # The line is full of delimiter.
                continue
            next_level = line[:line.index(label)].count(delimiter)
            if next_level - level > 1:
                # Concept must be at much one level below its parent.
                raise CSVIndentationError(nline)
            elif next_level <= level:
                # Walk back levels.
                while next_level <= level:
                    _, level = broaderconcepts.pop()
            concept = broaderconcepts[-1][0].add_concept(label, language_code)
            broaderconcepts.append((concept, level))
            level = next_level


class Concept(AnyEntity):
    __regid__ = 'Concept'
    fetch_attrs, cw_fetch_order = fetch_config(('cwuri',))

    def dc_title(self):
        return self.label()

    @property
    def parent_concept(self):
        return self.broader_concept[0] if self.broader_concept else None

    @property
    def scheme(self):
        return self.in_scheme[0]

    @property
    def labels(self):
        return dict((l.short_language_code, l.label) for l in self.pref_label)

    def label(self, language_code=None, default_language_code='en'):
        if language_code is None:
            language_code = self._cw.lang
        try:
            return self.labels[language_code[:2].lower()]
        except KeyError:
            try:
                return self.labels[default_language_code[:2].lower()]
            except KeyError:
                # pick one random label
                return self.labels.values()[0]

    def add_concept(self, label, language_code=u'en'):
        """Add a sub-concept to this concept"""
        return _add_concept(self.scheme, label, language_code, broader_concept=self)


class Label(AnyEntity):
    __regid__ = 'Label'
    fetch_attrs, cw_fetch_order = fetch_config(('language_code', 'label'))

    @property
    def short_language_code(self):
        """Return the 2 letters language code for this label"""
        if self.language_code is None:
            return None
        return self.language_code[:2].lower()


class ConceptITreeAdapter(ITreeAdapter):
    """ITree adapater for Concept"""
    __select__ = is_instance('Concept')
    tree_relation = 'broader_concept'


from yams import ValidationError
from cubicweb import UniqueTogetherError
from cubicweb.entities import adapters
from cubicweb.predicates import ExpectedValuePredicate

_ = unicode

# monkeypatched from cubicweb waiting for #5100373 to be integrated
class IUserFriendlyUniqueTogether(adapters.IUserFriendlyUniqueTogether):

    def raise_user_exception(self):
        rtypes = self.exc.rtypes
        errors = {}
        msgargs = {}
        i18nvalues = []
        for rtype in rtypes:
            errors[rtype] = _('%(KEY-rtype)s is part of violated unicity constraint')
            msgargs[rtype + '-rtype'] = rtype
            i18nvalues.append(rtype + '-rtype')
        errors[''] = _('some relations violate a unicity constraint')
        raise ValidationError(self.entity.eid, errors, msgargs=msgargs, i18nvalues=i18nvalues)


class unique_together_error_for(ExpectedValuePredicate):
    """Return 1 if exception given as `exc` in the input context is an UniqueTogetherError implying one
    of the relation type given on instanciation of this predicate.
    """
    def __call__(self, cls, req, exc=None, **kwargs):
        if exc is not None and isinstance(exc, UniqueTogetherError):
            return len(frozenset(exc.rtypes) & self.expected)
        return 0


class IUserFriendlyUniqueTogetherPrefLabelLanguageCode(IUserFriendlyUniqueTogether):
    __select__ =  (IUserFriendlyUniqueTogether.__select__
                   & unique_together_error_for('pref_label_of', 'language_code'))

    def raise_user_exception(self):
        errors = {'': _('a preferred label in "%(lang)s" language already exists'),
                  'language_code': _('please use another language code')}
        raise ValidationError(self.entity.eid, errors, {'lang': self.entity.language_code})


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (IUserFriendlyUniqueTogether,))
    vreg.register_and_replace(IUserFriendlyUniqueTogether, adapters.IUserFriendlyUniqueTogether)
