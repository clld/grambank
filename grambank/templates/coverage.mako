<%inherit file="home_comp.mako"/>

<h3>Coverage</h3>

<table class="table table-nonfluid table-striped">
    <thead>
        <tr>
            <th></th>
            <th colspan="3" style="text-align: center">Total families</th>
            <th colspan="3" style="text-align: center">Families or isolates with grammar</th>
            <th colspan="3" style="text-align: center">Families or isolates with grammar sketch</th>
        </tr>
        <tr>
            <th>Macroarea</th>
            <th>Glottolog</th>
            <th>Grambank</th>
            <th>Coverage</th>
            <th>Glottolog</th>
            <th>Grambank</th>
            <th>Coverage</th>
            <th>Glottolog</th>
            <th>Grambank</th>
            <th>Coverage</th>
        </tr>
    </thead>
    <tbody>
        % for ma, data in stats.items():
        <tr>
            <td>
                    <button type="button" class="ma btn" id="${ma}">${macroareas[ma]}</button>
            </td>
            <td class="right">${data['total']['glottolog']}</td>
            <td class="right">${data['total']['grambank']}</td>
            ${u.td_coverage(**data['total'])|n}
            <td class="right">${data['grammar']['glottolog']}</td>
            <td class="right">${data['grammar']['grambank']}</td>
            ${u.td_coverage(**data['grammar'])|n}
            <td class="right">${data['grammarsketch']['glottolog']}</td>
            <td class="right">${data['grammarsketch']['grambank']}</td>
            ${u.td_coverage(**data['grammarsketch'])|n}
        </tr>
        % endfor
    </tbody>
</table>

<hr/>

<table class="table table-nonfluid">
    <thead>
    <tr>
        <th></th>
        <th></th>
        <th colspan="3" style="text-align: center">Total subunits</th>
        <th></th>
        <th colspan="3" style="text-align: center">Subunits with grammar</th>
        <th colspan="3" style="text-align: center">Subunits with grammar sketch</th>
    </tr>
    <tr>
        <th>Family</th>
        <th>Subunit</th>
        <th>Glottolog</th>
        <th>Grambank</th>
        <th>Coverage</th>
        <th>Macroareas</th>
        <th>Glottolog</th>
        <th>Grambank</th>
        <th>Coverage</th>
        <th>Glottolog</th>
        <th>Grambank</th>
        <th>Coverage</th>
    </tr>
    </thead>
    <tbody>
        % for (fid, fname), data in cstats.items():
            <tr class="subunit ${' '.join([ma[1] for ma in data['macroareas']])}">
                ${u.td_coverage(label=fname, **data['total'])|n}
                <td>
                    % if not data['isolate']:
                    <button type="button" class="toggle btn" id="${fid}">expand</button>
                    % else:
                    <i>isolate</i>
                    % endif
                </td>
                <td class="right">${data['total']['glottolog']}</td>
                <td class="right">${data['total']['grambank']}</td>
                ${u.td_coverage(**data['total'])|n}
                <td>${', '.join([ma[0] for ma in data['macroareas']])}</td>
                <td class="right">${data['grammar']['glottolog']}</td>
                <td class="right">${data['grammar']['grambank']}</td>
                ${u.td_coverage(**data['grammar'])|n}
                <td class="right">${data['grammarsketch']['glottolog']}</td>
                <td class="right">${data['grammarsketch']['grambank']}</td>
                ${u.td_coverage(**data['grammarsketch'])|n}
            </tr>
            % for (sfid, fname), data in data.get('subgroups', {}).items():
                <tr class="subunit ${fid} ${' '.join([ma[1] for ma in data['macroareas']])}" style="display: none">
                    <td></td>
                    ${u.td_coverage(label=fname, **data['total'])|n}
                    <td class="right">${data['total']['glottolog']}</td>
                    <td class="right">${data['total']['grambank']}</td>
                    ${u.td_coverage(**data['total'])|n}
                    <td>${', '.join([ma[0] for ma in data['macroareas']])}</td>
                    <td class="right">${data['grammar']['glottolog']}</td>
                    <td class="right">${data['grammar']['grambank']}</td>
                    ${u.td_coverage(**data['grammar'])|n}
                    <td class="right">${data['grammarsketch']['glottolog']}</td>
                    <td class="right">${data['grammarsketch']['grambank']}</td>
                    ${u.td_coverage(**data['grammarsketch'])|n}
                </tr>
            % endfor
        % endfor
    </tbody>
</table>

<script>
    $(".ma").click(function() {
        var     button = $(this),
                ma = $(this).attr('id');

        $("tr.subunit").each(function(){
            var tr = $(this);
            if (tr.hasClass(ma)) {
                tr.show();
            } else {
                tr.hide();
            }
        });
    })
    $(".toggle").click(function() {
        var     button = $(this),
                fid = $(this).attr('id');
        $("tr." + fid).toggle();
        if (button.html() == 'expand') {
            button.html('collapse');
        } else {
            button.html('expand');
        }
    })
</script>