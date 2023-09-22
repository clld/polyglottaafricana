from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.util import concepticon

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

from clld.db.models import common

from polyglottaafricana import models


class VarietyID(Col):
    def order(self):
        return models.Variety.ord


class ConceptID(Col):
    def order(self):
        return models.Concept.ord


class Words(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.parameter:
            query = query.outerjoin(models.Variety.family)

        return query

    def col_defs(self):
        if self.parameter:
            return [
                VarietyID(
                    self,
                    'No',
                    model_col=common.Language.id,
                    get_object=lambda i: i.valueset.language),
                LinkCol(
                    self,
                    'language',
                    model_col=common.Language.name,
                    get_object=lambda i: i.valueset.language),
                FamilyCol(
                    self,
                    'family',
                    models.Variety,
                    get_object=lambda i: i.valueset.language),
                LinkCol(self, 'name', sTitle='Orthography'),
                Col(self, 'description', sTitle='IPA'),
                Col(self, 'segments', model_col=models.Form.segments),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]

        if self.language:
            return [
                ConceptID(
                    self,
                    'ID',
                    model_col=common.Parameter.id,
                    input_size='mini',
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(self,
                        'parameter',
                        sTitle=self.req.translate('Parameter'),
                        model_col=common.Parameter.name,
                        get_object=lambda i: i.valueset.parameter),
                LinkCol(self, 'name', sTitle='Orthography'),
                Col(self, 'description', sTitle='IPA'),
                Col(self, 'segments', model_col=models.Form.segments),
            ]

        return [
            Col(self, 'name', sTitle='Orthography'),
            Col(self, 'description', sTitle='IPA'),
            Col(self, 'segments', model_col=models.Form.segments),
        ]


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.join(Family).options(joinedload(models.Variety.family)).distinct()

    def col_defs(self):
        return [
            VarietyID(self, 'ID', model_col=models.Variety.id),
            LinkCol(self, 'name'),
            Col(self, 'RefLex', model_col=models.Variety.reflex_name),
            Col(self, 'Glottolog', model_col=models.Variety.glottolog_name),
            FamilyCol(self, 'Family', models.Variety),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class ConcepticonCol(Col):
    def format(self, item):
        if not item.concepticon_id:
            return ''
        return concepticon.link(self.dt.req, id=item.concepticon_id, label=item.description)


class Vocabulary(Parameters):
    def col_defs(self):
        return [
            ConceptID(
                self,
                'No',
                model_col=common.Parameter.id,
                input_size='mini'),
            LinkCol(self, 'name'),
            ConcepticonCol(self, 'description', sTitle='Concepticon'),
        ]


def includeme(config):
    config.register_datatable('parameters', Vocabulary)
    config.register_datatable('values', Words)
    config.register_datatable('languages', Languages)
