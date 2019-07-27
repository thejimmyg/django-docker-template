# Template

This example shows one way of setting up a base template with Flexbox layout. It requires the example SCSS integration to be set up too.

The example contains the following files:

* `README.md` - This file
* `base.html` - A base template that requires a Flexbox layout (place in `mysite/templates/`)
* `mystyle.scss` - The SCSS that will be compiled to CSS (place in `mysite/static/css/`)
* `test.html` - An example template inherited from `base.html` (place in `mysite/templates/`)
* `urls.py` - An example config that uses the view in `views.py` to render the test template (place in `mysite/`)
* `user.html` - An optional template that can be uncommented `base.html` that shows user information and login/logout links in the user block (place in `mysite/templates/`)
* `views.py` - An example view to  render the test template (place in `mysite/`)


The base template includes a setup for Django messages. The view adds a `Hello world.` success message each time it is called, so you'll see that in the template.

There is also some setup for buttons which is not included in the `test.html` template yet.

The important point in Flexbox is that elements shrink as well as grow. We want the grow behaviour but not the shrink behaviour so we set `flex-shrink: no`.

Also, if the content is very short we still want the footer to be at the bottom and the content to fill the space so we set `height: 100vh` in the outer `.frame` class.

To convert the SCSS to CSS, the `base.html` file has this:

```
{% load sass_tags %}
<!DOCTYPE html>
<html class="no-js" lang="en">
  <head>
    ...
    <link href="{% sass_src 'css/mystyle.scss' %}" rel="stylesheet" type="text/css" />
    ...
```

Note the `{% load sass_tags %}` tag and the use of `{% sass_src ... %}`.

The `test.html` file is setup so that if you don't want the `backbar` displayed you can add this:

```
{% block back_bar %}{% endblock %}
```

But if you do want it, you can customise the text and target like this:


```
{% block back_bar_text %}Back to Profile{% endblock %}
{% block back_bar_link %}https://www.google.com{% endblock %}
```

Also, the content background color can be set with:

```
{% block content_background_class %}mysite-cyan{% endblock %}
```
