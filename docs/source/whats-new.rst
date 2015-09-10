What's New?
===========


0.4
---

* Changed the implementation of the ``run`` tag to
  :class:`~climactic.tags.processes.ShellRunCommand`,
  which uses ``bash`` directly instead of running each line via
  :mod:`subprocess`.

* A plugin system has been introduced for loading YAML tags; it
  utilizes ``entry_points`` from :mod:`pkg_resources`
  (distributed with :mod:`setuptools`).

* All core tags are now implemented using this system.


0.3
---

* Added ``py.test`` support.


0.2
---

* Enabled YAML tag syntax (``!tag-name <tag-data>``).


0.1
---

* Initial release
