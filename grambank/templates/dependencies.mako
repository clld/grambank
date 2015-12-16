<%inherit file="home_comp.mako"/>

<h3>Functional Dependencies</h3>

<table class="table table-nonfluid table-striped">
    <thead>
        <tr>
            <th>Feature 1</th>
            <th>Feature 2</th>
            <th>Strength</th>
            <th>Significance</th>
        </tr>
    </thead>
    <tbody>
        % for v, f1, f2 in data:
        <tr>
            <td class="left">${f1}</td>
            <td class="left">${f2}</td>
            <td class="left">${v}</td>
            <td class="left"></td>
        </tr>
        % endfor
    </tbody>
</table>
