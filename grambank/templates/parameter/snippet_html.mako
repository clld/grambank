<%namespace name="util" file="../util.mako"/>

<div class="span2">
    <table class="table table-condensed table-nonfluid">
        <% total = 0 %>
        % for de in ctx.domain:
        <% total += len(de.values) %>
            <tr>
                <td>${h.map_marker_img(req, de)}</td>
                <td>${de.name}</td>
                <td>${de.description}</td>
                <td class="right">${len(de.values)}</td>
            </tr>
        % endfor
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td class="right"><strong>${total}</strong></td>
        </tr>
    </table>
</div>

<div class="span10">
    ${u.process_markdown(ctx.description, req, section='Summary')|n}
</div>
