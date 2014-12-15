Suffixer
==========

Suffixer is a little RoboFont extension for **editing glyph name suffixes**. It can *append* a suffix to the names of selected glyphs, or *replace* an existing suffix with a new one (or none) in selected glyphs or the whole font.

![Suffixer screenshot](/screenshot.png)

Suffixer comes with a list of suffix presets <sup>case, dnom, fina, hist, init, isol, locl, lnum, medi, numr, onum, ordn, tnum, pcap, salt, sinf, smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, zero</sup>. These are modeled after OpenType feature names – a frequent usage scenario. But you can of course also enter other suffixes; these will be saved to the extension preferences and subsequently included in the preset list. 

Suffixer does not live in the Extensions menu (which quickly becomes cluttered) but can be activated via the main *Font* menu of RoboFont under the heading *Change Suffixes...*, or with the shortcut Cmd+Alt+Shift+S.

**Some things about renaming glyphs, and a word of caution:**

If you rename a glyph from RoboFont’s main interface, you are asked to confirm that the glyph should also be renamed in groups, in kerning, and with regard to components. Suffixer has all these options *on* by default, which means it should not break things like composites or kerning. It also globally assigns auto unicodes in the end (which is relevant if you are using it to add or remove suffixes). If you think any of these options should be deselectable, please let me know.

If Suffixer encounters that your current font already has a glyph with a name to be newly assigned to a different glyph, the previously existing glyph will be renamed to *[its present name].copy_1* (or if that is taken, *.copy_2* and so forth); so nothing should be lost.

Note the usage of the word “should” in the above two paragraphs; this is the very first version, so please use with caution (= make a backup copy of your font first), and report things that break.

