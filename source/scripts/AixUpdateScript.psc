Scriptname AixUpdateScript extends ReferenceAlias

Spell Property UpdateSpell Auto
Actor Property PlayerREF Auto

int version

Event OnInit() ; This event will run once, when the script is initialized
	RegisterForSingleUpdate(2.0)
EndEvent

Event OnUpdate()			
	;Debug.Trace("OnInit code started, so stop polling!")

	UpdateSpell.Cast(PlayerREF)
	version = 103
	UnregisterForUpdate()

EndEvent

Event OnPlayerLoadGame()
	if !version
		UpdateSpell.Cast(PlayerREF)
		version = 103
	elseIf version < 103
		UpdateSpell.Cast(PlayerREF)
		version = 103
	endIf
EndEvent
