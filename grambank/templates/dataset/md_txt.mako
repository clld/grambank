${' and '.join(ed.contributor.name for ed in ctx.editors)} ${request.dataset.published.year if request.dataset.published else request.dataset.updated.year}.
${request.dataset.description or request.dataset.name}.
${request.dataset.publisher_place}: ${request.dataset.publisher_name}.
(Available online at http://${request.dataset.domain}, Accessed on ${h.datetime.date.today()}.)
