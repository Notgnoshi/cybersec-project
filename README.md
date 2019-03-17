# cybersec-project

An educational application to teach highschoolers various topics in cybersecurity

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
