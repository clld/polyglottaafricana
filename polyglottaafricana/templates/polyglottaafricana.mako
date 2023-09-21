<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}"
       title="Koelle's Polyglotta Africana"
       style="padding-top: 0px; padding-bottom: 0px; padding-right: 0px; padding-left: 0px;">
        <img src="${request.static_url('polyglottaafricana:static/polyglotta1.png')}" width="440"/>
    </a>
</%block>

${next.body()}
