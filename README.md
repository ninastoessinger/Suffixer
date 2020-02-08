Suffixer
==========

Suffixer is a little RoboFont extension for **editing glyph name suffixes**. It can *append* a suffix to the names of selected glyphs, or *replace* an existing suffix with a new one (or none) in selected glyphs or the whole font.

![Suffixer screenshot](/screenshot.png)

Suffixer comes with a list of suffix presets <sup>case, dnom, fina, hist, init, isol, locl, lnum, medi, numr, onum, ordn, tnum, pcap, salt, sinf, smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, zero</sup>. These are modeled after OpenType feature names – a frequent usage scenario. But you can of course also enter other suffixes; these will be saved to the extension preferences and subsequently included in the preset list. 

Suffixer does not live in the Extensions menu (which quickly becomes cluttered) but can be activated via the main *Font* menu of RoboFont under the heading *Change Suffixes...*, or with the shortcut Cmd+Alt+Shift+S.

**Update v1.2** (Feb 2020) includes compatibility fixes for RoboFont 3 (thanks to Ryan Bugden). I’ve also removed the global setting of default Unicodes, which seemed a bit too brute force. Auto Unicodes should still be assigned for renamed glyphs in case a suffix was added or removed (thanks to DJR for the question/report). 

![Suffixer menu](/menu.png)

**Some things about renaming glyphs, and a word of caution:**

If you rename a glyph from RoboFont’s main interface, you are asked to confirm that the glyph should also be renamed in groups, in kerning, and with regard to components. Suffixer has all these options *on* by default, which means it should not break things like composites or kerning. 

If Suffixer encounters that your current font already has a glyph with a name to be newly assigned to a different glyph, the previously existing glyph will be renamed to *[its present name].copy_1* (or if that is taken, *.copy_2* and so forth); so nothing should be lost.

Note the usage of the word “should” in the above two paragraphs; this is still an early version, so please use with caution (= make a copy of your font first), and report things that break.

**PS. Caution when removing suffixes, re. composites:** One scenario that has proven to be problematic is when you use Suffixer to make a previously-suffixed set of glyphs the new default – for instance, make *A.new B.new C.new* into *A, B,* and *C*, replacing your previous standard *A, B,* and *C* glyphs. As it is now, Suffixer will keep and rename the old *A, B,* and *C* glyphs; but any composite glyphs that have those in them will keep referencing these old glyphs instead of (what you maybe wanted) the new ones. Not sure how to best handle these cases: Maybe Suffixer should ask whether to keep or overwrite, and/or which glyphs the composites should refer to. Opinions welcome.
