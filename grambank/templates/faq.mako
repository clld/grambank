<%inherit file="grambank.mako"/>
<%! active_menu_item = "faq" %>

<h2>FAQ</h2>

${u.markdown(req.dataset.jsondata['faq'])|n}
