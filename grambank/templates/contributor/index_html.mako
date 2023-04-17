<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>

<%block name="head">
    <style>
        #people th {
            font-size: larger;
            text-align: left;
            padding-bottom: 10px;
        }
    </style>
</%block>


<%def name="profile(cid, coder=False)">
    <% cid = contributors[cid] if isinstance(cid, str) else cid %>
    % if cid is None:
        <td></td>
    % else:
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>${cid.name}</h5>
                % if coder:
                    <p>
                        ${h.link(req, cid, label='Contributed {} datapoints for {} languages and dialects'.format(ndatapoint.get(cid.pk, ''), nlangs.get(cid.pk, '')))}
                    </p>
                % endif
            </div>
        </td>
    % endif
</%def>

<h2>People</h2>

<ul class="nav nav-pills">
    % for role, rid, _ in contribs:
        <li class="active">
            <a href="#${rid}">${role}</a>
        </li>
    % endfor
</ul>

<table id="people">
    % for role, rid, people in contribs:
        <tr>
            <th colspan="4" id="${rid}">
                ${role}
                <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
            </th>
        </tr>
    % for batch in people:
        <tr>
            % for person in batch:
                ${profile(person, coder=rid == 'coder')}
            % endfor
        </tr>
    % endfor
    % endfor
</table>

