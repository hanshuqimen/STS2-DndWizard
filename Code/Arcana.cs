using BaseLib.Abstracts;
using BaseLib.Utils;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Entities.Relics;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.ValueProps;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Saves.Runs;
using MegaCrit.Sts2.Core.Rooms;

namespace DndWizard;

public static class Arcana
{
    public const int SlotCap = 6;
    public static Spellbook? Book(Creature owner) => owner.Player?.Relics.OfType<Spellbook>().FirstOrDefault();
    public static int Experience(Creature owner) => Book(owner)?.ResearchExperience ?? 0;
    public static int MaxTier(Creature owner) => SpellbookRules.MaxTier(Experience(owner));
    public static int Cap(Creature owner) => SlotCap + SpellbookRules.CapacityBonus(Experience(owner)) + (owner.Player?.Relics.Any(r => r is ExpandedGrimoire) == true ? 2 : 0);
    public static int Slots(Creature owner) => Math.Clamp(Book(owner)?.StoredSlots ?? owner.GetPower<SpellSlotsPower>()?.Amount ?? 0, 0, Cap(owner));
    public static int Cost(Creature owner, int tier) => Math.Max(0, tier -
        (tier > 0 && owner.Player?.Relics.Any(r => r is EfficientFocus) == true && owner.GetPower<FocusSpentPower>() == null ? 1 : 0));
    public static CastingPayment Quote(Creature owner, int tier) => SpellbookRules.Quote(tier, Slots(owner), owner.CurrentHp,
        Experience(owner), Cost(owner, 1) == 0, owner.GetPower<OvercastSpentPower>() != null);
    public static async Task Sync(PlayerChoiceContext context, Creature owner, CardModel? source)
    {
        int delta = Slots(owner) - (owner.GetPower<SpellSlotsPower>()?.Amount ?? 0);
        if (delta > 0) await PowerCmd.Apply<SpellSlotsPower>(context, owner, delta, owner, source);
        else if (delta < 0 && owner.GetPower<SpellSlotsPower>() is { } power)
            await PowerCmd.ModifyAmount(context, power, delta, owner, source);
        if (owner.GetPower<SpellSlotsPower>() is { } slots) slots.DynamicVars["Capacity"].BaseValue = Cap(owner);
    }
    public static async Task Gain(PlayerChoiceContext context, Creature owner, int amount, CardModel? source)
    {
        int gain = Math.Clamp(amount, 0, Math.Max(0, Cap(owner) - Slots(owner)));
        if (Book(owner) is { } book)
        {
            book.StoredSlots = Slots(owner) + gain;
            await Sync(context, owner, source);
        }
        else if (gain > 0) await PowerCmd.Apply<SpellSlotsPower>(context, owner, gain, owner, source);
    }
    public static async Task<bool> Spend(PlayerChoiceContext context, Creature owner, CardPlay play, int tier)
    {
        var source = play.Card;
        if (tier < 1) return false;
        var payment = Quote(owner, tier);
        if (!payment.Allowed) return false;
        int cost = payment.Slots;
        // Reserve the once-per-combat action before any reactive HP-loss hooks.
        if (payment.Overcast)
            await PowerCmd.Apply<OvercastSpentPower>(context, owner, 1, owner, source);
        if (Book(owner) is { } book)
        {
            book.StoredSlots = Slots(owner) - cost;
            await Sync(context, owner, source);
        }
        else if (cost > 0 && owner.GetPower<SpellSlotsPower>() is { } slots)
            await PowerCmd.ModifyAmount(context, slots, -cost, owner, source);
        if (owner.Player?.Relics.Any(r => r is EfficientFocus) == true && owner.GetPower<FocusSpentPower>() == null)
            await PowerCmd.Apply<FocusSpentPower>(context, owner, 1, owner, source);
        if (payment.Hp > 0)
            await CreatureCmd.Damage(context, owner, payment.Hp, ValueProp.Unblockable | ValueProp.Unpowered | ValueProp.Move, source);
        if (owner.IsDead) return false;
        var ward = owner.GetPower<ArcaneWardPower>();
        if (ward != null) await CreatureCmd.GainBlock(owner, ward.Amount, ValueProp.Unpowered, play);
        if (owner.Player?.Relics.Any(r => r is RunicFocus) == true)
            await CreatureCmd.GainBlock(owner, 2, ValueProp.Unpowered, play);
        return true;
    }
    public static async Task Concentrate<T>(PlayerChoiceContext context, Creature owner, int amount, CardModel source) where T : PowerModel
    {
        bool switching = (owner.GetPower<ArcaneWardPower>() != null || owner.GetPower<EvocationPower>() != null || owner.GetPower<MeditationPower>() != null)
            && owner.GetPower<T>() == null;
        // One concentration spell at a time; recasting replaces instead of accumulating.
        await PowerCmd.Remove<ArcaneWardPower>(owner);
        await PowerCmd.Remove<EvocationPower>(owner);
        await PowerCmd.Remove<MeditationPower>(owner);
        await PowerCmd.Apply<T>(context, owner, amount, owner, source);
        if (switching) await Gain(context, owner, 1, source);
    }
}

public abstract class WizardPower : CustomPowerModel
{
    public override PowerType Type => PowerType.Buff;
    public override PowerStackType StackType => PowerStackType.Counter;
    public override string CustomPackedIconPath => "res://DndWizard/images/powers/" + GetType().Name + ".png";
    public override string CustomBigIconPath => CustomPackedIconPath;
}
public sealed class SpellSlotsPower : WizardPower
{
    protected override IEnumerable<DynamicVar> CanonicalVars => [new SlotCapacityVar()];
}
// Resolve capacity from the owner on display, including immediately after loading
// a save, before the next combat has had a chance to synchronize the power.
public sealed class SlotCapacityVar() : DynamicVar("Capacity", Arcana.SlotCap)
{
    private int Capacity => _owner switch
    {
        Spellbook book when book.IsMutable && book.Owner != null => Arcana.Cap(book.Owner.Creature),
        SpellSlotsPower power when power.IsMutable && power.Owner != null => Arcana.Cap(power.Owner),
        _ => Arcana.SlotCap
    };
    public override string ToString() => Capacity.ToString();
    protected override decimal GetBaseValueForIConvertible() => Capacity;
}
public sealed class FocusSpentPower : WizardPower { }
public sealed class OvercastSpentPower : WizardPower { }
public sealed class DelayedRecoveryPower : WizardPower
{
    public override async Task AfterPlayerTurnStart(PlayerChoiceContext context, Player player)
    {
        if (player != Owner.Player) return;
        int amount = Amount;
        await PowerCmd.Remove(this);
        await Arcana.Gain(context, Owner, amount, null);
    }
}
public sealed class EmpowerPower : WizardPower { }
public sealed class CantripProgressPower : WizardPower { }
public sealed class CantripSpentPower : WizardPower
{
    public override async Task AfterPlayerTurnStart(PlayerChoiceContext context, Player player)
    {
        if (player == Owner.Player) await PowerCmd.Remove(this);
    }
}
public sealed class MirrorImagePower : WizardPower
{
    public override decimal ModifyHpLostAfterOsty(Creature target, decimal amount, ValueProp props, Creature? dealer, CardModel? cardSource)
        => target == Owner && amount > 0 && props.IsPoweredAttack() ? Math.Max(0, amount - 4) : amount;
    public override async Task AfterModifyingHpLostAfterOsty()
    {
        Flash();
        await PowerCmd.Decrement(this);
    }
}
public sealed class ArcaneWardPower : WizardPower { }
public sealed class EvocationPower : WizardPower
{
    public override decimal ModifyDamageAdditive(Creature? target, decimal amount, ValueProp props, Creature? dealer, CardModel? cardSource)
        => dealer == Owner && props.IsPoweredAttack() && cardSource is WizardCard ? Amount : 0;
}
public sealed class MeditationPower : WizardPower
{
    public override async Task AfterPlayerTurnStart(PlayerChoiceContext context, Player player)
    {
        if (player == Owner.Player) await Arcana.Gain(context, Owner, Amount, null);
    }
}

[Pool(typeof(WizardRelicPool))]
public abstract class WizardRelic : CustomRelicModel
{
    public override string PackedIconPath => "res://DndWizard/images/relics/" + GetType().Name + ".png";
    protected override string BigIconPath => PackedIconPath;
    protected override string PackedIconOutlinePath => PackedIconPath;
}
public sealed class Spellbook : WizardRelic
{
    private int _researchExperience;
    [SavedProperty]
    public int ResearchExperience
    {
        get => _researchExperience;
        set
        {
            AssertMutable();
            _researchExperience = Math.Clamp(value, 0, SpellbookRules.MaxExperience);
            DynamicVars["Research"].BaseValue = _researchExperience;
            DynamicVars["Level"].BaseValue = SpellbookRules.Level(_researchExperience);
            DynamicVars["Next"].BaseValue = SpellbookRules.NextThreshold(_researchExperience);
            DynamicVars["MaxTier"].BaseValue = SpellbookRules.MaxTier(_researchExperience);
            DynamicVars["BloodCost"].BaseValue = SpellbookRules.HpPerSlot(_researchExperience);
        }
    }
    private int _storedSlots = Arcana.SlotCap;
    [SavedProperty]
    public int StoredSlots
    {
        get => _storedSlots;
        set
        {
            AssertMutable();
            _storedSlots = Math.Max(0, value);
            DynamicVars["Current"].BaseValue = _storedSlots;
            DynamicVars["Capacity"].BaseValue = Owner == null ? Arcana.SlotCap : Arcana.Cap(Owner.Creature);
            InvokeDisplayAmountChanged();
        }
    }
    protected override IEnumerable<DynamicVar> CanonicalVars => [new DynamicVar("Current", _storedSlots), new SlotCapacityVar(),
        new DynamicVar("Research", _researchExperience), new DynamicVar("Level", SpellbookRules.Level(_researchExperience)),
        new DynamicVar("Next", SpellbookRules.NextThreshold(_researchExperience)), new DynamicVar("MaxTier", SpellbookRules.MaxTier(_researchExperience)),
        new DynamicVar("BloodCost", SpellbookRules.HpPerSlot(_researchExperience))];
    public override bool ShowCounter => true;
    public override int DisplayAmount => _storedSlots;
    public override RelicRarity Rarity => RelicRarity.Starter;
    public override Task AfterCombatVictory(CombatRoom room)
    {
        if (Owner.Creature.IsDead || ResearchExperience >= SpellbookRules.MaxExperience) return Task.CompletedTask;
        int oldCapacity = Arcana.Cap(Owner.Creature);
        ResearchExperience += room.RoomType switch { RoomType.Boss => 3, RoomType.Elite => 2, _ => 1 };
        // Only fill newly unlocked capacity, not the whole book.
        StoredSlots = Math.Min(Arcana.Cap(Owner.Creature), StoredSlots + Arcana.Cap(Owner.Creature) - oldCapacity);
        Flash();
        return Task.CompletedTask;
    }
    public override async Task BeforeCombatStart()
    {
        StoredSlots = Arcana.Slots(Owner.Creature);
        await Arcana.Sync(new ThrowingPlayerChoiceContext(), Owner.Creature, null);
    }
    public override Task AfterRestSiteHeal(Player player, bool isMimicked)
    {
        if (player == Owner && !isMimicked)
        {
            StoredSlots = Arcana.Cap(Owner.Creature);
            Flash();
        }
        return Task.CompletedTask;
    }
    public override IReadOnlyList<LocString> ModifyExtraRestSiteHealText(Player player, IReadOnlyList<LocString> currentExtraText)
    {
        if (player != Owner) return currentExtraText;
        return [..currentExtraText, new LocString("relics", "DNDWIZARD-SPELLBOOK.restSiteHealText")];
    }
    public override async Task AfterCardPlayed(PlayerChoiceContext context, CardPlay play)
    {
        if (play.Card.Owner != Owner || play.Card is not WizardCard { Spec.Cantrip: true }) return;
        var creature = Owner.Creature;
        if (creature.GetPower<CantripSpentPower>() != null) return;
        if (creature.GetPower<CantripProgressPower>() == null)
            await PowerCmd.Apply<CantripProgressPower>(context, creature, 1, creature, play.Card);
        else
        {
            await PowerCmd.Remove<CantripProgressPower>(creature);
            await PowerCmd.Apply<CantripSpentPower>(context, creature, 1, creature, play.Card);
            await Arcana.Gain(context, creature, 1, play.Card);
            Flash();
        }
    }
}
public sealed class PearlOfPower : WizardRelic
{
    public override RelicRarity Rarity => RelicRarity.Uncommon;
    public override async Task BeforeCombatStart()
    {
        Flash();
        await Arcana.Gain(new ThrowingPlayerChoiceContext(), Owner.Creature, 2, null);
    }
}
public sealed class RunicFocus : WizardRelic
{
    public override RelicRarity Rarity => RelicRarity.Rare;
}
public sealed class ExpandedGrimoire : WizardRelic
{
    public override RelicRarity Rarity => RelicRarity.Uncommon;
    public override Task AfterObtained()
    {
        if (Arcana.Book(Owner.Creature) is { } book) book.StoredSlots = Arcana.Slots(Owner.Creature);
        return Task.CompletedTask;
    }
    public override Task AfterRemoved()
    {
        if (Arcana.Book(Owner.Creature) is { } book) book.StoredSlots = Math.Min(book.StoredSlots, Arcana.SlotCap + SpellbookRules.CapacityBonus(book.ResearchExperience));
        return Task.CompletedTask;
    }
}
public sealed class CampfireIncense : WizardRelic
{
    public override RelicRarity Rarity => RelicRarity.Uncommon;
    public override async Task AfterRestSiteHeal(Player player, bool isMimicked)
    {
        if (player != Owner || isMimicked) return;
        Flash();
        await CreatureCmd.Heal(Owner.Creature, 6);
    }
}
public sealed class EfficientFocus : WizardRelic
{
    public override RelicRarity Rarity => RelicRarity.Rare;
}
