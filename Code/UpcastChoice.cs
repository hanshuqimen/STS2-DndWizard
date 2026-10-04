using BaseLib.Abstracts;
using BaseLib.Utils;
using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;

namespace DndWizard;

// Choice-only tokens never enter a pile or the card library. Selection is synchronized
// by the game's standard grid selector, including remote players and replays.
[Pool(typeof(WizardCardPool))]
public sealed class UpcastOption() : CustomCardModel(0, CardType.Skill, CardRarity.Token, TargetType.Self, showInCardLibrary: false)
{
    public int Tier { get; private set; }
    private WizardCard? _spell;
    private string _effects = "";
    public override string PortraitPath => _spell?.PortraitPath ?? "res://DndWizard/images/cards/MagicMissile.png";
    private bool _overcast;
    public override string Title => (_overcast ? new LocString("cards", "DNDWIZARD-UPCAST_OPTION.overcastTitle").GetFormattedText() + " · " : "") + (_spell?.Title ?? base.Title) + " · " + Tier;
    protected override IEnumerable<DynamicVar> CanonicalVars => [new DynamicVar("Tier", 0), new DynamicVar("Cost", 0), new DynamicVar("HpCost", 0), new DynamicVar("Current", 0), new DynamicVar("Capacity", 6)];
    protected override void AddExtraArgsToDescription(LocString description) => description.Add("Effects", _effects);
    public void Configure(WizardCard spell, int tier)
    {
        AssertMutable();
        _spell = spell;
        Tier = tier;
        DynamicVars["Tier"].BaseValue = tier;
        var payment = Arcana.Quote(spell.Owner.Creature, tier);
        _overcast = payment.Overcast;
        DynamicVars["Cost"].BaseValue = payment.Slots;
        DynamicVars["HpCost"].BaseValue = payment.Hp;
        DynamicVars["Current"].BaseValue = Arcana.Slots(spell.Owner.Creature);
        DynamicVars["Capacity"].BaseValue = Arcana.Cap(spell.Owner.Creature);
        _effects = spell.UpcastPreview(tier);
    }
    protected override Task OnPlay(PlayerChoiceContext context, CardPlay play) => Task.CompletedTask;
}

public static class UpcastChoice
{
    public static async Task<int> Select(PlayerChoiceContext context, WizardCard spell)
    {
        List<CardModel> choices = [];
        for (int tier = 0; tier <= Arcana.MaxTier(spell.Owner.Creature); tier++)
        {
            if (!Arcana.Quote(spell.Owner.Creature, tier).Allowed) continue;
            var choice = spell.CombatState!.CreateCard<UpcastOption>(spell.Owner);
            choice.Configure(spell, tier);
            choices.Add(choice);
        }
        if (choices.Count == 1) return 0;
        var prefs = new CardSelectorPrefs(new LocString("cards", "DNDWIZARD-UPCAST_OPTION.selectionScreenPrompt"), 1);
        var selected = (await CardSelectCmd.FromSimpleGrid(context, choices, spell.Owner, prefs)).FirstOrDefault();
        return selected is UpcastOption option ? option.Tier : 0;
    }
}
