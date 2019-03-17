# cybersec-project

An educational application to teach highschoolers various topics in cybersecurity

---

## Adding a new module

The process for adding a new module is documented here.

Create a new application

```shell
./manage.py startapp example
cd example
rm tests.py admin.py models.py
```

Then edit the `apps.py` file to edit the module config class to inherit from the `cybered.ModuleMixin`.
E.g., edit

```python
from django.apps import AppConfig

class ExampleConfig(AppConfig):
    name = 'example'
```

to look like this

```python
from shared.src import cybered

class ExampleConfig(cybered.ModuleMixin, CyberEdAppConfig):
    name = 'example'
    module_name = 'An Example Application'
    module_base_link = 'example/'
    module_start_link = 'page1'
    module_description = '...'
```

or alternatively

```python
from shared.src import cybered

class ExampleModule(cybered.ModuleMixin):
    name = 'example'
    module_name = 'An Example Application'
    module_base_link = 'example/'
    module_start_link = 'page1'
    module_description = '...'

class ExampleConfig(ExampleModule, CyberEdAppConfig):
  pass
```

Then create a `urls.py` file and add the first page to the `urlpatterns` list.

```python
from django.urls import path
from .apps import ExampleConfig
from .views import ExampleBeginView

app_name = ExampleConfig.name
urlpatterns = [path(ExampleConfig.module_start_link, ExampleBeginView.as_view(), name="page1")]
```

Finally, create a view and the corresponding HTML template for the begin page. Pages should inherit
from `cybered.PageMixin`. The page mixin will populate the header text for each page of the module
with the display name for the module. It is easiest to inherit pages from both your module and from
the page mixin, as in the first example below, but you may also create a separate type to do this,
as in the second example. Note that if you do the first, you must make sure your page is not indirectly
inheriting `django.apps.AppConfig`

```python
from django.views.generic import TemplateView
from example.apps import ExampleModule
from shared.src import cybered

class ExampleBeginView(ExampleModule, cybered.PageMixin, ExampleTemplateView):
    """The main page for the hashing module."""
    template_name = "example/page1.html"

"""Inhriting from ExampleConfig like this will not work, because ExampleConfig
inherits django.apps.AppConfig"""
# from example.apps import ExampleConfig
# class ExampleBeginView(ExampleConfig, cybered.PageMixin, ExampleTemplateView):
```

```python
from django.views.generic import TemplateView
from example.apps import ExampleModule
from shared.src import cybered

class ExamplePage(cybered.PageMixin):
    module_name = "Alternative module name"

class ExampleBeginView(ExamplePage, ExampleTemplateView):
    """The main page for the hashing module."""
    template_name = "example/page1.html"
```

Then create a templates directory and the the HTML template for the module begin page.

```shell
mkdir -p templates/example
touch templates/example/page1.html
```

The extra directory with the same name as the application is used to prevent collisions between
template names between modules.

Add the following HTML code to the `page1.html` file. The shared head.html and footer.html files
will set up the handle the `<body>` and `</body>` tags, as well as the page header, and the outermost div.

```html
<!doctype HTML>
<html>
{% include "includes/head.html" %}
    <p>Hello World.</p>

    <div class="container mt-3">
        <a href="{% url 'landingpage:index' %}" class="btn btn-secondary">Prev</a>
        <a href="{% url 'example:page2' %}" class="btn btn-primary">Next</a>
    </div>
{% include "includes/footer.html" %}
```

Finally, edit `cybered/cybered/settings.py` so that the `INSTALLED_APPS` list contains `"example.apps.ExampleConfig"`.
This will install the application in the CyberEd project, and cause a link to the application's first
page to appear on the landing page.

---

## TODOs

Questions

* Add a module-specific CSS to the global templates?
* Should we number the pages and indicate that to the user?
  * E.g. "page 3/12"
* (low priority) Ajaxify the hashing form
  * Enables the user to more seamlessly compare results from run-to-run
  * An opportunity for failure. I mean Excellence. Definitely excellence.

Outstanding TODO items

* (high priority) Make a list of potential modules
  * Hashing
  * Password Strength
    * Might include graphs (time to crack wrt different variables)
  * Password Cracking Methodology
  * How passwords are stored

    Will depend on the hashing module. Also, make the connection to current data breaches. Should
    this be baked into the password cracking module?
  * Classical Ciphers
    * Caesar, because that's what everyone begins with
    * Vigenere, because that's the next step up
  * Classical Cipher Cryptanalysis
    * Might include graphs (symbol frequency histograms)
  * Block ciphers
    * How to make interactive?
  * Steganography
    * Cool factor
    * Lots of work, and we'd potentially have to handle file uploads?
* (med priority) Add next/previous buttons to the module pages
  * Find a good way to paginate more automatically

    This could possibly be done via a template, bubblegum, and voodoo.
  * What about pagination using page numbers rather than URLs with meaning?
* (med priority) Get hashing module content nailed down
  * Produce an outline with desired outcomes
  * Address each outcome pointwise
* (low priority) Add Gen Cyber Camp branding
* (low priority) Finish Bootstrapifying
* (low priority) Make the site deployable with an Apache server
