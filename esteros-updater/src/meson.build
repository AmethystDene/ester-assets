esteros_updater_sources = [
  'main.c',
  'esteros-updater-application.c',
  'esteros-updater-window.c',
]

esteros_updater_deps = [
  dependency('gtk4'),
  dependency('libadwaita-1', version: '>= 1.2'),
]

esteros_updater_sources += gnome.compile_resources('esteros-updater-resources',
  'esteros-updater.gresource.xml',
  c_name: 'esteros_updater'
)

executable('esteros-updater', esteros_updater_sources,
  dependencies: esteros_updater_deps,
       install: true,
)
