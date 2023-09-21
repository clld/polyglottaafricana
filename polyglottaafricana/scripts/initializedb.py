import string
import itertools
import collections

from pycldf import Sources
from clldutils.misc import nfilter, slug
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from nameparser import HumanName

from clld_ipachart_plugin.util import load_inventories, clts_from_input
from clld_glottologfamily_plugin.util import load_families
from pyglottolog.references.roman import romanint

import polyglottaafricana
from polyglottaafricana import models


def iteritems(cldf, t, *cols):
    cmap = {cldf[t, col].name: col for col in cols}
    for item in cldf[t]:
        for k, v in cmap.items():
            item[v] = item[k]
        yield item


def main(args):

    assert args.glottolog, 'The --glottolog option is required!'

    clts = clts_from_input('../../cldf-clts/clts-data')
    data = Data()
    ds = data.add(
        common.Dataset,
        polyglottaafricana.__name__,
        id=polyglottaafricana.__name__,
        name="Koelle's Polyglotta Africana",
        domain='polyglottaafricana',
        description=args.cldf.properties.get('dc:bibliographicCitation'),
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )

    for i, name in enumerate(['Guillaume Segerer', 'Robert Forkel', 'Johann-Mattis List']):
        common.Editor(
            dataset=ds,
            ord=i,
            contributor=common.Contributor(id=slug(HumanName(name).last), name=name)
        )

    contrib = data.add(
        common.Contribution,
        None,
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )

    for lang in iteritems(args.cldf, 'LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
            local_id=lang['Local_ID'],
            reflex_name=lang['RefLex_Name'],
            glottolog_name=lang['Glottolog_Name'],
        )

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    refs = collections.defaultdict(list)


    for param in iteritems(args.cldf, 'ParameterTable', 'id', 'concepticonReference', 'name'):
        data.add(
            models.Concept,
            param['id'],
            id=param['id'],
            name='{} [{}]'.format(param['name'], param['id']),
        )

    scans = {r['id']: r['downloadUrl'].unsplit()
             for r in args.cldf.iter_rows('MediaTable', 'id', 'downloadUrl')}

    for form in iteritems(
            args.cldf,
            'FormTable',
            'id', 'form', 'languageReference', 'parameterReference', 'mediaReference', 'source'):
        vsid = (form['languageReference'], form['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][form['languageReference']],
                parameter=data['Concept'][form['parameterReference']],
                contribution=contrib,
                jsondata=dict(scan=scans[form['mediaReference']]),
            )
        for ref in form.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        data.add(
            models.Form,
            form['id'],
            id=form['id'],
            name=form['form'],
            description=''.join([s.split('/')[-1] for s in form['Segments']]).replace('+', ' '),
            segments=' '.join(form['Segments']),
            valueset=vs,
        )

    load_inventories(args.cldf, clts, data['Variety'])
    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))
    load_families(
        Data(),
        [(l.glottocode, l) for l in data['Variety'].values()],
        glottolog_repos=args.glottolog,
        isolates_icon='tcccccc',
        strict=False,
    )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    def lid2ord(lid, name):
        comps = lid.split('-')
        part = romanint(comps.pop(0).lower())
        res = [part]
        if part in {2, 6, 11}:  # 2-a
            res.append(int(comps.pop(0)))
            if comps:
                res.append(ord(comps.pop(0)))
            else:
                res.append(999)
            res.append(999)
        else:  # A-1-a
            res.append(ord(comps.pop(0)))
            if part != 12:
                res.append(int(comps.pop(0)))
                if comps:
                    res.append(ord(comps.pop(0)))
                else:
                    res.append(999)
            else:  # A-a-2a
                third = comps.pop(0)
                res.append(ord(third) if third in 'ab' else int(third))
                if comps:
                    fourth = comps.pop()
                    res.append(ord(fourth) if fourth in string.ascii_lowercase else int(fourth[0]))
                else:
                    res.append(999)

        assert not comps and len(res) == 4, lid
        res.append(name)
        return tuple(res)

    for i, l in enumerate(sorted(
            DBSession.query(models.Variety), key=lambda l_: lid2ord(l_.local_id, l_.name))):
        l.ord = i + 1
