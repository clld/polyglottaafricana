<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameters')}</%block>

<h2>${title()}</h2>
<div>
    ${ctx.render()}
</div>

<%def name="sidebar()">
<div class="well well-small">
    <blockquote>
        In the selection of the words which were to compose the Vocabulary I was guided by the desire to take those only which are most easily understood by the natives - names of visible objects at which I could point - avoiding all abstract words.
        I think that in most of the words I have chosen the <em>affinity</em> of languages is especially likely to exhibit itself, so that any two given languages appear from this Polyglot to be rather more closely allied than if we could compare their whole glossarial treasure, but never <em>vice versa</em>.
        <div style="width: 100%; text-align: right; font-size: x-small">Polyglotta Africana. Preface.</div>
    </blockquote>
    <p>
        See also the related concept list in Concepticon:
        <a href="${req.dataset.jsondata['concept_list']}">${req.dataset.jsondata['concept_list'].split('/')[-1]}</a>
    </p>
</div>
</%def>
