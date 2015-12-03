<%inherit file="home_comp.mako"/>

<h3>Coverage</h3>

<table class="table table-nonfluid table-striped">
    <thead>
        <tr>
            <th></th>
            <th colspan="3">Families with grammar</th>
            <th colspan="3">Families with grammar sketch</th>
            <th colspan="3">Total</th>
        </tr>
        <tr>
            <th>Macroarea</th>
            <th>Glottolog</th>
            <th>GramBank</th>
            <th></th>
            <th>Glottolog</th>
            <th>GramBank</th>
            <th></th>
            <th>Glottolog</th>
            <th>GramBank</th>
            <th></th>
        </tr>
    </thead>
    <tbody>
        % for ma, data in stats.items():
        <tr>
            <td>${ma}</td>
            <td class="right">${data['grammar']['glottolog']}</td>
            <td class="right">${data['grammar']['grambank']}</td>
            <td>
                <img src="${u.coverage_badge(data['grammar']['glottolog'], data['grammar']['grambank'])}"/>
            </td>
            <td class="right">${data['grammar']['glottolog']}</td>
            <td class="right">${data['grammar']['grambank']}</td>
            <td>
                <img src="${u.coverage_badge(data['grammarsketch']['glottolog'], data['grammarsketch']['grambank'])}"/>
            </td>
            <td class="right">${data['total']['glottolog']}</td>
            <td class="right">${data['total']['grambank']}</td>
            <td>
                <img src="${u.coverage_badge(data['total']['glottolog'], data['total']['grambank'])}"/>
            </td>
        </tr>
        % endfor
    </tbody>
</table>

