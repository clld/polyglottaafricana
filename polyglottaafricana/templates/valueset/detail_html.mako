<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>
    Words for ${h.link(request, ctx.parameter, label=ctx.parameter.name.split('[')[0])} in
    ${ctx.language.id} ${h.link(request, ctx.language)}</h2>

<div class="well">
    <table class="table table-condensed table-nonfluid">
        <thead>
        <th>Source</th>
        <th>Broad IPA</th>
        </thead>
        <tbody>
        % for i, value in enumerate(ctx.values):
        <tr>
            <td>${value.name}</td>
            <td>${value.description}</td>
        </tr>
        % endfor
        </tbody>
    </table>
</div>

<a href="${ctx.jsondata['scan']}">
    <img src="${ctx.jsondata['scan']}" class="img-polaroid"/>
</a>
