[app]
title = Instagram Manager
package.name = instamanager
package.domain = org.app

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.features = android.hardware.camera

[buildozer]
log_level = 2
warn_on_root = 1
