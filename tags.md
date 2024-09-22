---
layout: page
title: "Tags"
permalink: /tags/
---
<div>
{% for tag in site.tags %}
  <h5 id="{{ tag | first | slugify }}">{{ tag | first }}</h5>
  <ul>
    {% for post in tag.last %}
      <li><a href="{{ post.url }}">{{ post.title }}</a> - {{ post.date | date: "%b %d, %Y" }}</li>
    {% endfor %}
  </ul>
{% endfor %}
</div>
