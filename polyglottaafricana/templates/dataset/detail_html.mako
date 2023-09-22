<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Cite as</h3>
        <blockquote>
            Sigismund Koelle. (2023). CLDF dataset derived from Koelle's "Polyglotta Africana" from 1854 (v1.2) [Data set]. Zenodo. <a href="https://doi.org/10.5281/zenodo.8365633">https://doi.org/10.5281/zenodo.8365633</a>
        </blockquote>
    </div>
</%def>

<div style="width: 25%; float: left">
    <a href="https://resolver.sub.uni-hamburg.de/goobi/PPN862704383">
        <img title="Koelle's Polyglotta Africana in DFG Viewer"
             class="img-polaroid"
             src="${request.static_url('polyglottaafricana:static/polyglotta_cover_small.jpeg')}"/>
    </a>
</div>

<div style="width: 38%; float: left; margin-left: 5%; margin-right: 3%">
    <h2>Koelle's Polyglotta Africana</h2>

    <p class="lead">or a comparative Vocabulary of nearly 300 words and phrases, in more than one hundred distinct African Languages</p>
    <p>
        This ${h.external_link('https://github.com/clld', label='clld')} web application serves the
        ${h.external_link('https://github.com/cldf/cldf/tree/master/modules/Wordlist', label='CLDF Wordlist')}
        derived from the comparative vocabularies of Koelle's "Polyglotta Africana".
        See <a href="download">the download page</a> for details about how to access the data.
    </p>
</div>

<div style="width: 29%; float: left">
    <a href="https://resolver.sub.uni-hamburg.de/kitodo/PPN862704383/page/37">
        <img title="Koelle's Polyglotta Africana in DFG Viewer"
             class="img-polaroid"
             src="${request.static_url('polyglottaafricana:static/polyglotta_map_small.jpeg')}"/>
    </a>
</div>
