<%inherit file="home_comp.mako"/>

<h3>Coverage</h3>

<table class="table table-nonfluid table-striped">
    <thead>
        <tr>
            <th></th>
            <th colspan="3" style="text-align: center">Families with grammar</th>
            <th colspan="3" style="text-align: center">Families with grammar sketch</th>
            <th colspan="3" style="text-align: center">Total</th>
        </tr>
        <tr>
            <th>Macroarea</th>
            <th>Glottolog</th>
            <th>GramBank</th>
            <th>Coverage</th>
            <th>Glottolog</th>
            <th>GramBank</th>
            <th>Coverage</th>
            <th>Glottolog</th>
            <th>GramBank</th>
            <th>Coverage</th>
        </tr>
    </thead>
    <tbody>
        % for ma, data in stats.items():
        <tr>
            <td>${ma}</td>
            <td class="right">${data['grammar']['glottolog']}</td>
            <td class="right">${data['grammar']['grambank']}</td>
            ${u.td_coverage(**data['grammar'])|n}
            <td class="right">${data['grammarsketch']['glottolog']}</td>
            <td class="right">${data['grammarsketch']['grambank']}</td>
            ${u.td_coverage(**data['grammarsketch'])|n}
            <td class="right">${data['total']['glottolog']}</td>
            <td class="right">${data['total']['grambank']}</td>
            ${u.td_coverage(**data['total'])|n}
        </tr>
        % endfor
    </tbody>
</table>

