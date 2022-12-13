"""
RoboFont extension to change/append/replace glyph name suffixes

v1.2 / Nina Stoessinger / February 2020
With thanks to Frederik Berlaen, David Jonathan Ross, Ryan Bugden
"""

import os
from AppKit import NSApp, NSMenuItem, NSAlternateKeyMask, NSCommandKeyMask
from fontTools.feaLib import ast
from fontTools.feaLib.parser import Parser
from mojo.tools import CallbackWrapper
from mojo.extensions import registerExtensionDefaults, getExtensionDefault, setExtensionDefault
from mojo.UI import Message
from vanilla import *


class Suffixer:
	
	def __init__(self):
		""" Add the "Change Suffixes" menu item to the Font menu. """
		title = "Change Suffixes..."
		fontMenu = NSApp().mainMenu().itemWithTitle_("Font")
		if not fontMenu:
			print("Suffixer: Error, aborting")
			return
		fontMenu = fontMenu.submenu()
		if fontMenu.itemWithTitle_(title):
			return
			
		index = fontMenu.indexOfItemWithTitle_("Add Glyphs")
		self.target = CallbackWrapper(self.openWindow)
		newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, "action:", "S")
		newItem.setKeyEquivalentModifierMask_(NSAlternateKeyMask | NSCommandKeyMask);
		newItem.setTarget_(self.target)
		fontMenu.insertItem_atIndex_(newItem, index+1)
		
		
	def openWindow(self, sender=None):
		""" Initialize the input window. """
		presets = [
			"case", "dnom", "fina", "hist", "init", "isol", "locl", "lnum", "medi", "numr", "onum", "ordn", "tnum",
			"pcap", "salt", "sinf", "smcp", "ss01", "ss02", "ss03", "ss04", "ss05", "ss06", "ss07", "ss08",
			"ss09", "ss10", "ss11", "ss12", "ss13", "ss14", "ss15", "ss16", "ss17", "ss18", "ss19", "ss20",
			"subs", "sups", "swsh", "titl", "zero" ]
		presetList = " ".join(presets)
		registerExtensionDefaults({"nl.typologic.suffixer.presetSuffixes" : presetList})
		currentPresets = getExtensionDefault("nl.typologic.suffixer.presetSuffixes").split()
		
		self.f = CurrentFont()
		if self.f is None:
			print("Suffixer: No font open")
			return
		
		existingSuffixes = []
		for g in self.f:
			suf = self._findSuffix(g.name)
			if suf != None and suf not in existingSuffixes:
				existingSuffixes.append(suf)
		existingSuffixes.sort()
		
		currentSuffix = ""
		if CurrentGlyph() is not None:
			currentSuffix = self._findSuffix(CurrentGlyph().name)
		elif self.f.selectedGlyphNames is not None:
			for gn in self.f.selectedGlyphNames:
				currentSuffix = self._findSuffix(gn)
				if currentSuffix != None:
					break
		
		self.w = FloatingWindow((300, 200), "Suffixer")
		p = 10
		h = 20
		y1, y2, y3, y4, y5 = 15, 49, 82, 135, 169
		w1, x2 = 160, 180
		
		self.w.labelTwo = TextBox((p, y1, w1, h), "Add suffix to glyph names:")
		self.w.dotTwo = TextBox((x2, y1, 15, h), ".")
		self.w.newSuffix = ComboBox((x2+p, y1, -p, h), currentPresets)
		
		self.w.replace = CheckBox((p+2, y2, w1, h), "Replace existing suffix:", callback=self.replaceCheckCallback)
		
		self.w.dotOne = TextBox((x2, y2, 15, h), ".")
		self.w.oldSuffix = PopUpButton((x2+p, y2, -p, h), existingSuffixes)
		if currentSuffix != "" and currentSuffix != None:
			self.w.oldSuffix.set(existingSuffixes.index(currentSuffix))
		
		self.w.scope = RadioGroup((p, y3, -p, h*2), ["Target selected glyphs", "Replace all in current font"], isVertical=True)
		self.w.scope.set(0)

		self.w.inFeatureCode = CheckBox((p+2, y4, -p, h), "Change glyph names in feature code")
		self.w.inFeatureCode.set(0)

		currentState = 0 if currentSuffix == "" or currentSuffix == None else 1
		self.w.replace.set(currentState)
		self.w.scope.enable(currentState)
		self.w.inFeatureCode.enable(currentState)
			
		self.w.submit = Button((p, y5, -p, h), "Change suffixes", callback=self.replaceSuffixes)
		self.w.setDefaultButton(self.w.submit)
		self.w.open()
		self.w.makeKey()
		
		
	def replaceCheckCallback(self, sender):
		""" Toggle UI options depending on selection whether to replace or append the new suffix. """
		if self.w.replace.get() == False:
			self.w.scope.set(0)
			self.w.scope.enable(0)
			self.w.inFeatureCode.set(0)
			self.w.inFeatureCode.enable(0)
		else:
			self.w.scope.enable(1)
			self.w.inFeatureCode.enable(1)
		
	
	def _findSuffix(self, gname):
		""" Find the suffix (if any) in a given glyph name. """
		i = gname.find(".")
		if i != -1 and i != 0:
			return gname[i+1:]
		else:
			return None
		
		
	def replaceSuffixes(self, sender):
		""" Handle replacing/appending of suffixes. """
		mode = "replace" if self.w.replace.get() == 1 else "append"
		oldSuffix = self.w.oldSuffix.getItems()[self.w.oldSuffix.get()]
		enteredSuffix = self.w.newSuffix.get()
		suffixes_in = [oldSuffix, enteredSuffix]
		
		suffixes = [] # build proper suffixes list
		for s in suffixes_in:
			if s is not None and len(s) > 0:
				if s[0] == ".":
					s = s[1:] # handle suffixes without periods
			suffixes.append(s)

		if mode == "replace" and suffixes[0] == suffixes[1]:
			Message(u"Cannot replace a suffix with itself.\nI mean I could, but there seems to be little point :)")
		elif mode == "append" and suffixes[1] == "":
			Message(u"Cannot append an empty suffix.\n(Or you could just pretend I've already done it.)")

		else:
			scope = self.f.keys() if self.w.scope.get() == 1 else self.f.selectedGlyphNames

			renameDict = dict() # collect all name changes in one dict

			if mode == "replace":
				for gname in scope:
					if gname.endswith(suffixes[0]):
						sufLen = len(suffixes[0])
						if len(suffixes[1]) > 0:
							newName = gname[:-sufLen] + suffixes[1]
						else:
							sufLenWithPeriod = sufLen+1
							newName = gname[:-sufLenWithPeriod]
						renameDict[gname] = newName
							
			elif mode == "append":
				for gname in scope:
					newName = gname + "." + suffixes[1]
					renameDict[gname] = newName

			# change names in feature code first
			if self.w.inFeatureCode.get():
				self._changeInFeatureCode(self.f, renameDict)

			# then rename the glyphs themselves
			for oldName, newName in renameDict.items():
				self._changeGlyphname(oldName, newName)

			self.f.changed()
			
			# store new values as defaults
			savedPresets = getExtensionDefault("nl.typologic.suffixer.presetSuffixes")
			if enteredSuffix != "" and enteredSuffix not in savedPresets:
				savedPresetsList = savedPresets.split()
				savedPresetsList.append(enteredSuffix)
				savedPresetsList.sort()
				newPresets = " ".join(savedPresetsList) 
				setExtensionDefault("nl.typologic.suffixer.presetSuffixes", newPresets)
			
			self.w.close()
		
		
	def _changeGlyphname(self, gname, newName):
		""" Assign a new glyphname to a glyph. """
		print("Suffixer: Changing name of %s to %s" % (gname, newName))
		self.f[gname].prepareUndo("Change Suffix")
		
		# check if new name is already in use
		if newName in self.f.keys():
			i = 1
			while (newName + ".copy_" + str(i)) in self.f.keys():
				i = i+1
			cp = newName + ".copy_"+str(i)
			self.f.renameGlyph(newName, cp, renameComponents=True, renameGroups=True, renameKerning=True)
			self.f[cp].unicode = None
			print("Suffixer: A glyph named %s was already present in the font. It has been renamed to %s." % (newName, cp))
			### Note for future development:
			### At this point there is also the question which glyph existing composites should refer to
			### Think about how to address this
		# actual renaming of targeted glyph
		self.f.renameGlyph(gname, newName, renameComponents=True, renameGroups=True, renameKerning=True)
		self.f[newName].autoUnicodes()
		self.f[newName].performUndo()


	def _changeInFeatureCode(self, font, renameDict):
		""" Replace changed glyph names in feature file. """
		if font.path is None:
			return

		fea_path = os.path.join(font.path, 'features.fea')
		fea_ast = Parser(fea_path,font.glyphOrder).parse()

		### these next 2 blocks slightly alter extisting behavior
		### within feaLib to change glyph names when calling asFea
		oldFea = ast.asFea
		def newFea(g):
			# get new name from dict, otherwise return gname.
			return oldFea(renameDict.get(g, g))
		ast.asFea = newFea

		def glyphNameAsFea(self, indent=""):
			name = str(self.glyph)
			return renameDict.get(name, name)
		ast.GlyphName.asFea = glyphNameAsFea

		font.features.text = fea_ast.asFea()


Suffixer()
