Scriptname AixChangeBodySpellScript extends activemagiceffect  

AixBodySelectorScript Property SelectorScript Auto

Armor Property Skin01Naked Auto
Armor Property Skin02Naked Auto
Armor Property Skin03Naked Auto
Armor Property Skin04Naked Auto

Armor Property Skin01NakedF Auto
Armor Property Skin02NakedF Auto
Armor Property Skin03NakedF Auto
Armor Property Skin04NakedF Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)

	Debug.Notification("Updating RaceMenu Selector of Skins.")

	SelectorScript.Skin01Naked = Skin01Naked
	SelectorScript.Skin02Naked = Skin02Naked
	SelectorScript.Skin03Naked = Skin03Naked
	SelectorScript.Skin04Naked = Skin04Naked
	SelectorScript.Skin01NakedF = Skin01NakedF
	SelectorScript.Skin02NakedF = Skin02NakedF
	SelectorScript.Skin03NakedF = Skin03NakedF
	SelectorScript.Skin04NakedF = Skin04NakedF

	SelectorScript.UpdateBody()

endEvent