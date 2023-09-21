<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Cite as</h3>
        <blockquote>
            Sigismund Koelle. (2023). CLDF dataset derived from Koelle's "Polyglotta Africana" from 1854 (v1.2) [Data set]. Zenodo. <a href="https://doi.org/10.5281/zenodo.8365633">https://doi.org/10.5281/zenodo.8365633</a>
        </blockquote>
    </div>
</%def>

<h2>Koelle's Polyglotta Africana</h2>

<div style="width: 30%; float: left">
    <a href="https://resolver.sub.uni-hamburg.de/goobi/PPN862704383">
        <img title="Koelle's Polyglotta Africana in DFG Viewer"
             class="img-polaroid"
             src="https://pic.sub.uni-hamburg.de/kitodo/PPN862704383/00000001.tif"/>
    </a>
</div>

<div style="width: 62%; float: left; margin-left: 5%; margin-right: 3%">
    <p class="lead">or a comparative Vocabulary of nearly 300 words and phrases, in more than one hundred distinct African Languages</p>
    <p>
        This ${h.external_link('https://github.com/clld', label='clld')} web application serves the
        ${h.external_link('https://github.com/cldf/cldf/tree/master/modules/Wordlist', label='CLDF Wordlist')}
        derived from the comparative vocabularies of Koelle's "Polyglotta Africana".
        See <a href="download">the download page</a> for details about how to access the data.
    </p>
</div>
