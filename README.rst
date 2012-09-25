========
mappp.me
========

A simple, anonymous, location sharing site.

Motivation
==========
This was initially created for me to share my location on long drives.
Priorities when developing this were:

 * Simplicity
 
 * Privacy & preservation of anonymity
 
 * Support for a wide range of devices
 
 * The ability to scale if the need arose at a later date
 
To these ends, the following design decisions were made:

 * HTTPS everywhere in production.

 * Location history will not be kept. A single location will only be
   stored, for a maximum of 30 minutes without update.
   
 * No user registration will be required. Security of the
   administration URIs is only in the length and randomness of their
   paths. iptables should be used to block brute-force attacks.
   
   View URIs are not considered a risk as they contain no information
   to link the location with a user.
   
 * While the source device requires JavaScript with AJAX, many viewing
   devices should be supported. This includes support for small and
   low resolutions screens, inadequate or missing JavaScript support
   and WML.
 
 * To determine the possible available features of a user's device in
   the absence of scripting support, the WURFL database is used and
   some styling & script content is served on a per-device basis.
   
 * While keeping a small memory footprint, session data will be cached
   in memory, in the user's browser and in caching proxies when
   possible.
   
 * Storage and caching implementations should be able to be switched
   out with relative ease e.g. for deployment on GAE [INCOMPLETE].
 
Building
========
::
  virtualenv -p python2.7 --no-site-packages .
  bin/python bootstrap.py -c development.cfg
  bin/buildout -c development.cfg
  
Running
=======
::
  bin/instance start