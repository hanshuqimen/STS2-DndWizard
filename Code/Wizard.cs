using BaseLib.Abstracts;
using Godot;
using MegaCrit.Sts2.Core.Entities.Characters;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Unlocks;

namespace DndWizard;

public sealed class Wizard : PlaceholderCharacterModel
{
    public override string PlaceholderID => "silent";
    public override Color NameColor => new("b7c9ff");
    public override Color MapDrawingColor => new("6ce4e5");
    public override CharacterGender Gender => CharacterGender.Masculine;
    public override int StartingHp => 66;
    public override CardPoolModel CardPool => ModelDb.CardPool<WizardCardPool>();
    public override RelicPoolModel RelicPool => ModelDb.RelicPool<WizardRelicPool>();
    public override PotionPoolModel PotionPool => ModelDb.PotionPool<WizardPotionPool>();
    public override IEnumerable<CardModel> StartingDeck => [
        ModelDb.Card<FireBolt>(), ModelDb.Card<FireBolt>(), ModelDb.Card<FireBolt>(), ModelDb.Card<TrueStrike>(),
        ModelDb.Card<MageArmor>(), ModelDb.Card<MageArmor>(), ModelDb.Card<MageArmor>(), ModelDb.Card<MageArmor>(),
        ModelDb.Card<MagicMissile>(), ModelDb.Card<ArcaneRecovery>()];
    public override IReadOnlyList<RelicModel> StartingRelics => [ModelDb.Relic<Spellbook>()];
    public override string CustomVisualPath => "res://DndWizard/scenes/wizard.tscn";
    public override string CustomCharacterSelectBg => "res://DndWizard/scenes/select.tscn";
    public override string CustomIconPath => "res://DndWizard/scenes/icon.tscn";
    public override string CustomIconTexturePath => "res://DndWizard/images/icon.png";
    public override string CustomIconOutlineTexturePath => CustomIconTexturePath;
    public override string CustomCharacterSelectIconPath => CustomIconTexturePath;
    public override string CustomCharacterSelectLockedIconPath => CustomIconTexturePath;
    public override string CustomMapMarkerPath => CustomIconTexturePath;
    protected override IEnumerable<string> ExtraAssetPaths => [
        "res://DndWizard/images/powers/SpellSlotsPower.png",
        "res://DndWizard/images/powers/ArcaneWardPower.png",
        "res://DndWizard/images/powers/EvocationPower.png",
        "res://DndWizard/images/powers/MeditationPower.png",
        "res://DndWizard/images/powers/EmpowerPower.png",
        "res://DndWizard/images/powers/MirrorImagePower.png",
        "res://DndWizard/images/powers/CantripProgressPower.png",
        "res://DndWizard/images/powers/DelayedRecoveryPower.png",
        "res://DndWizard/images/powers/FocusSpentPower.png",
        "res://DndWizard/images/powers/OvercastSpentPower.png",
        "res://DndWizard/images/powers/CantripSpentPower.png"];
}

public sealed class WizardCardPool : CustomCardPoolModel
{
    protected override IEnumerable<CardModel> FilterThroughEpochs(UnlockState unlockState, IEnumerable<CardModel> cards)
        => base.FilterThroughEpochs(unlockState, cards).Where(c => c is not UpcastOption);
    public override string Title => "Wizard";
    public override float H => 0.64f;
    public override float S => 0.65f;
    public override float V => 0.85f;
    public override Color DeckEntryCardColor => new("697cbd");
    public override bool IsColorless => false;
    public override string BigEnergyIconPath => "res://DndWizard/images/energy.png";
    public override string TextEnergyIconPath => "res://DndWizard/images/energy_text.png";
}
public sealed class WizardRelicPool : CustomRelicPoolModel
{
    public override string EnergyColorName => "blue";
    public override Color LabOutlineColor => new("6ce4e5");
}
public sealed class WizardPotionPool : CustomPotionPoolModel
{
    public override string EnergyColorName => "blue";
    public override Color LabOutlineColor => new("6ce4e5");
}
