---
layout: page
permalink: /publications/
title: Publications
description: Conference and workshop papers in reverse chronological order.
years: [2019,2018,2017,2016,2015]
nav: true
---

<div class="publications">

{% for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
