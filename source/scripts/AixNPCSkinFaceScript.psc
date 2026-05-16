Scriptname AixNPCSkinFaceScript extends ActiveMagicEffect

; Reference to the main quest script — filled in ESP via property
AixBodySelectorScript Property SkinQuestScript Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
	; Player is managed by AixBodySelectorScript directly
	if akTarget == Game.GetPlayer()
		return
	endIf
	; Female NPCs only
	if akTarget.GetSex() != 1
		return
	endIf
	; Read the skin SPID assigned to this NPC
	Armor npcSkin = akTarget.GetActorBase().GetSkin()
	if !npcSkin
		return
	endIf
	int slot = SkinQuestScript.GetSlotForSkin(npcSkin)
	if slot < 2
		return
	endIf
	SkinQuestScript.ApplyFaceToActor(akTarget, slot)
EndEvent
