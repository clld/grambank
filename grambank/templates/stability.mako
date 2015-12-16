<%inherit file="home_comp.mako"/>

<h3>Parsimony Stability Rankings</h3>

${request.get_datatable('stability', h.models.Parameter).render()}

<table class="table table-nonfluid table-striped">
    <thead>
        <tr>
            <th>Feature</th>
            <th>Stability</th>
            <th>Retentions</th>
            <th>Transitions</th>
        </tr>
    </thead>
    <tbody>
        % for feature, dt in data:
        <tr>
            <td class="left">${feature}</td>
            <td class="left">${dt['stability']}</td>
            <td class="left">${dt['retentions']}</td>
            <td class="left">${dt['transitions']}</td>
        </tr>
        % endfor
    </tbody>
</table>

