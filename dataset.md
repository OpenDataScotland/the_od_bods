---
schema: default
title: {{ d.title }}
organization: {{ d.owner }}
notes: {{ d.description }}
resources:
{% for df in d.files %}
  - name: {{ d.title }} {{ df.file_type }}
  - url: {{ df.url }}
  - format: {{ df.file_type }}
{% endfor %}
license: {{ d.license }}
category:
{% for t in d.original_tags %}
  - {{ t }}
{% endfor %}
{% for t in d.manual_tags %}
  - {{ t }}
{% endfor %}
maintainer: Tim Wisniewski
maintainer_email: tim@timwis.com
---
