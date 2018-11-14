<%namespace name="util" file="../util.mako"/>

<table class="table table-condensed table-nonfluid">
    % for de in ctx.domain:
        <tr>
            <td>${h.map_marker_img(req, de)}</td>
            <td>${de.name}</td>
            <td>${de.description}</td>
            <td class="right">${len(de.values)}</td>
        </tr>
    % endfor
</table>
