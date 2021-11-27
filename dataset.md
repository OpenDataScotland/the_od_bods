---
schema: default
title: {{ d.title }}
organization: {{ d.owner }}
notes: >-
    {{ d.description|indent(4) }}
resources:
{%- for df in d.files %}
  - name: {{ d.title }} {{ df.file_type }}
  - url: >-
      {{ df.url }}
  - format: {{ df.file_type }}
{% endfor -%}
license: {{ d.license }}
category:
{% if d.original_tags %}{% for t in d.original_tags %}
  - {{ t }}
{%- endfor %}{% endif %}
{% if d. manual_tags %}{% for t in d.manual_tags %}
  - {{ t }}
{%- endfor %}{% endif -%}
maintainer: {{ d.owner }}
maintainer_email: someone@example.com
---
