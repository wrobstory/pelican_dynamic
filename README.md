pelican-dynamic
===============

Pelican dynamic makes it easy to embed custom CSS and JS into individual Pelican blog articles. 

Why?
----
Have you ever wanted to embed a dynamic D3 visualzation in your Pelican blog post? Me too. This makes it easy to do via the metadata tags for each article. 

How
---
To install the plugin, [follow the instructions on the Pelican plugin page.](https://github.com/getpelican/pelican-plugins) My settings look like the following: 

```python
PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['pelican_dynamic']
```

Next, create ```js``` and ```css``` directories in your ```content``` directory: 
```
website/
├── content
│   ├── js/
│   │   └── d3_vis_1.js
│   │   └── d3_vis_2.js
│   ├── css/
│   │   └── d3_styles.css
│   ├── article1.rst
│   ├── cat/
│   │   └── article2.md
│   └── pages
│       └── about.md
└── pelican.conf.py
```

and then add each resource as a comma-separated file name in the ```Scripts``` and ```Styles``` tags: 
```
Title: Pelican blog post with D3
Date: 2013-11-24
Category: Blog
Tags: D3
Slug: awesome-d3-vis
Author: Rob Story
Summary:  Pelican blog post with D3
D3:
Scripts: d3_vis_1.js, d3_vis_2.js
Styles: d3_styles.css
```

The ```D3:``` tag is a convenience method that will load a minified version of D3. All of the JS and CSS will live in corresponding ```js``` and ```css``` folders in your ```output``` folder. 

Finally, in your base template (likely named ```base.html```), you need to add the following in your ```head``` tags: 
```
{% if article %}
    {% if article.styles %}
        {% for style in article.styles %}
{{ style }}
        {% endfor %}
    {% endif %}
{% endif %}
```
and the following *after* your ```body``` tags: 
```
{% if article %}
    {% if article.scripts %}
        {% for script in article.scripts %}
{{ script }}
        {% endfor %}
    {% endif %}
{% endif %}
```

So, in the template I use for my blog ([Flasky](https://github.com/fjavieralba/flasky)), the [base template](https://github.com/fjavieralba/flasky/blob/master/templates/base.html) now looks like the following: 
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <link href='http://fonts.googleapis.com/css?family=Noticia+Text:400,700' rel='stylesheet' type='text/css' />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>{% block title %} {{SITENAME}} {% endblock %}</title>

    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/style.css" type="text/css" />
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/pygments.css" type="text/css" />
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/font-awesome.css" type="text/css"/>
    {% if article %}
        {% if article.styles %}
            {% for style in article.styles %}
    {{ style }}
            {% endfor %}
        {% endif %}
    {% endif %}
  </head>
  <body>
    <div class=container>
        {% block header %}
            {% include "header.html" %}
        {% endblock %}

        <div class="content">
        {% block content %} {% endblock %}
        </div>

        {% block footer %}
            {% include "footer.html" %}
        {% endblock %}
    </div>
    {% include 'googleanalytics.html' %}
    {% include 'piwik.html' %}
  </body>
    {% if article %}
        {% if article.scripts %}
            {% for script in article.scripts %}
    {{ script }}
            {% endfor %}
        {% endif %}
    {% endif %}
</html>
```

That's it! Run your standard ```make html``` or ```make publish``` commands and your JSS/CSS will be moved and ref'd in the right places.

Using D3 in a Blog Post
-----------------------
With Markdown, this is pretty easy. Just add the raw HTML for your chart element in the middle of your markdown text: 

```
This is going to be a blog post about D3. Here is my chart: 

<div class="d3-chart"></div>

Isn't that a nice looking chart up there?
```

Then with D3, make sure you're selecting that element: 

```javascript
var svg = d3.select(".d3-chart").append("svg")
```

Ensure that your D3 is loaded *after* your body tags (as outlined above) so that it selects an existing element on the page. 
