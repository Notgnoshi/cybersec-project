"""This is the Django project for the CyberEd website.

Each Django project is a collection of Django applications. Here, we have a number of different
applications. Of note, we have an application for the landing page of the website. The landing page
application searches through all other installed applications (determined by the `INSTALLED_APPS`
setting) for applications that derive from the CyberEdAppConfig base class. If such an application
is found, it is added to the landing page.

Each application implements what we have decided to call an "educational module". Each module is a
linear sequence of web pages, with  prev/next buttons to navigate through the module. There is a
strong suggestion that each module be implemented in as an interactive as possible manner. Further,
there is a strong suggestion that each module implement standalone tools that a student can use to
play around and explore the topics covered by that module.
"""
