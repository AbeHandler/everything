---
layout: default
title: Blog
navigation_weight: 2
---

<div class="container">
	<h3 class="spacing">Posts</h3>

	<h4>Occasional posts and tutorials</h4>

	<div class="blog-posts">
		{% for post in site.posts %}
			<div class="blog-post spacing">
				<h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
				<p class="summary">
					{{ post.category }}
					<span class="date">
						{{ post.date | date: '%B %d, %Y' }}
					</span>
				</p>
				{{ post.excerpt }}
			</div>
		{% endfor %}
	</div>
</div>
