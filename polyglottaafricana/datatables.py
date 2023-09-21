from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.value import Values

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

from clld.db.models import common

from polyglottaafricana import models


class LocalID(Col):
    def order(self):
        return models.Variety.ord


class Words(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.parameter:
            query = query.outerjoin(models.Variety.family)

        return query

    def col_defs(self):
        if self.parameter:
            return [
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
                #
                # Add
                # - language family
                # - ID order
                #
                LinkCol(self, 'name', sTitle='Orthography'),
                Col(self, 'description', sTitle='IPA'),
                Col(self, 'segments', model_col=models.Form.segments),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]

        if self.language:
            return [
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
            LocalID(self, 'ID', model_col=models.Variety.local_id),
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


def includeme(config):
    config.register_datatable('values', Words)
    config.register_datatable('languages', Languages)
