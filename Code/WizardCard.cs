using BaseLib.Abstracts;
using BaseLib.Utils;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Localization;

namespace DndWizard;

public record SpellSpec(string Id, int Cost, CardType Type, CardRarity Rarity,
    int Damage = 0, int DamageUp = 0, int Block = 0, int BlockUp = 0,
    int Hits = 1, bool All = false, bool Upcast = false, int BonusDamage = 0, int BonusBlock = 0,
    int Draw = 0, int DrawUp = 0, int Slots = 0, int SlotsUp = 0,
    int Weak = 0, int Vulnerable = 0, int Poison = 0, int Energy = 0,
    string Concentration = "", int Power = 0, int PowerUp = 0, bool Exhaust = false, bool Retain = false,
    bool Cantrip = false, int Empower = 0, int EmpowerUp = 0, int Mirror = 0, int MirrorUp = 0,
    int VsWeak = 0, bool Counter = false, int BonusPoison = 0, int UpcastWeak = 0,
    int BonusHits = 0, int BonusWeak = 0, int DelayedSlots = 0, int DelayedSlotsUp = 0,
    bool Burn = false, int HpLoss = 0, bool RestoreAll = false, bool Prepare = false);

[Pool(typeof(WizardCardPool))]
public abstract class WizardCard : CustomCardModel
{
    public SpellSpec Spec { get; }
    protected WizardCard(SpellSpec spec) : base(spec.Cost, spec.Type, spec.Rarity,
        spec.All ? TargetType.AllEnemies : (spec.Counter || spec.Damage > 0 || spec.Weak > 0 || spec.Vulnerable > 0 || spec.Poison > 0) ? TargetType.AnyEnemy : TargetType.Self)
    { Spec = spec; }
    public override string PortraitPath => "res://DndWizard/images/cards/" + GetType().Name + ".png";
    protected override HashSet<CardTag> CanonicalTags => GetType() == typeof(FireBolt) ? [CardTag.Strike] : GetType() == typeof(MageArmor) ? [CardTag.Defend] : [];
    public override HashSet<CardKeyword> CanonicalKeywords
    {
        get
        {
            HashSet<CardKeyword> result = [];
            if (Spec.Exhaust) result.Add(CardKeyword.Exhaust);
            if (Spec.Retain) result.Add(CardKeyword.Retain);
            return result;
        }
    }
    protected override IEnumerable<DynamicVar> CanonicalVars
    {
        get
        {
            if (Spec.Damage > 0) yield return new DamageVar(Spec.Damage, ValueProp.Move);
            if (Spec.Block > 0) yield return new BlockVar(Spec.Block, ValueProp.Move);
            yield return new DynamicVar("BonusDamage", Spec.BonusDamage);
            yield return new DynamicVar("BonusBlock", Spec.BonusBlock);
            yield return new DynamicVar("Draw", Spec.Draw);
            yield return new DynamicVar("Slots", Spec.Slots);
            yield return new DynamicVar("Power", Spec.Power);
            yield return new DynamicVar("Empower", Spec.Empower);
            yield return new DynamicVar("Mirror", Spec.Mirror);
            yield return new DynamicVar("DelayedSlots", Spec.DelayedSlots);
        }
    }
    protected override IEnumerable<IHoverTip> ExtraHoverTips
    {
        get
        {
            if (Spec.Upcast || Spec.Slots > 0 || Spec.DelayedSlots > 0 || Spec.RestoreAll) yield return HoverTipFactory.FromPower<SpellSlotsPower>();
            if (Spec.Weak > 0) yield return HoverTipFactory.FromPower<WeakPower>();
            if (Spec.Vulnerable > 0) yield return HoverTipFactory.FromPower<VulnerablePower>();
            if (Spec.Poison > 0) yield return HoverTipFactory.FromPower<PoisonPower>();
            if (Spec.Empower > 0) yield return HoverTipFactory.FromPower<EmpowerPower>();
            if (Spec.Mirror > 0) yield return HoverTipFactory.FromPower<MirrorImagePower>();
            if (Spec.Cantrip) yield return HoverTipFactory.FromPower<CantripProgressPower>();
            if (Spec.Counter || Spec.UpcastWeak > 0 || Spec.VsWeak > 0) yield return HoverTipFactory.FromPower<WeakPower>();
            if (Spec.Concentration == "Ward") yield return HoverTipFactory.FromPower<ArcaneWardPower>();
            if (Spec.Concentration == "Evocation") yield return HoverTipFactory.FromPower<EvocationPower>();
            if (Spec.Concentration == "Meditation") yield return HoverTipFactory.FromPower<MeditationPower>();
        }
    }
    protected override async Task OnPlay(PlayerChoiceContext context, CardPlay play)
    {
        int tier = Spec.Upcast ? await UpcastChoice.Select(context, this) : 0;
        if (tier > 0 && !await Arcana.Spend(context, Owner.Creature, play, tier)) tier = 0;
        if (Owner.Creature.IsDead) return;
        bool upcast = tier > 0;
        if (Spec.Damage > 0)
        {
            // Consume before resolving the attack: echoes/replays cannot reuse one charge.
            int empower = upcast ? Owner.Creature.GetPower<EmpowerPower>()?.Amount ?? 0 : 0;
            if (empower > 0) await PowerCmd.Remove<EmpowerPower>(Owner.Creature);
            int controlBonus = play.Target?.GetPower<WeakPower>() != null ? Spec.VsWeak : 0;
            var attack = DamageCmd.Attack(DynamicVars.Damage.BaseValue + tier * Spec.BonusDamage + empower + controlBonus)
                .WithHitCount(Spec.Hits + tier * Spec.BonusHits).FromCard(this).WithHitFx("vfx/vfx_attack_blunt");
            if (Spec.All) attack.TargetingAllOpponents(CombatState!);
            else attack.Targeting(play.Target ?? throw new InvalidOperationException("A target is required."));
            await attack.Execute(context);
        }
        if (Spec.Block > 0)
            await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block.BaseValue + tier * Spec.BonusBlock, ValueProp.Move, play);
        if (play.Target is { IsDead: false } target)
        {
            if (Spec.Weak > 0) await PowerCmd.Apply<WeakPower>(context, target, Spec.Weak + tier * Spec.BonusWeak, Owner.Creature, this);
            if (Spec.Vulnerable > 0) await PowerCmd.Apply<VulnerablePower>(context, target, Spec.Vulnerable, Owner.Creature, this);
            if (Spec.Poison > 0) await PowerCmd.Apply<PoisonPower>(context, target, Spec.Poison + tier * Spec.BonusPoison, Owner.Creature, this);
            if (Spec.Counter && (target.Monster?.IntendsToAttack ?? false))
            {
                await PowerCmd.Apply<WeakPower>(context, target, 2, Owner.Creature, this);
                await Arcana.Gain(context, Owner.Creature, 1, this);
            }
        }
        if (upcast && Spec.UpcastWeak > 0)
            foreach (var enemy in CombatState!.HittableEnemies.ToList())
                await PowerCmd.Apply<WeakPower>(context, enemy, tier * Spec.UpcastWeak, Owner.Creature, this);
        if (Spec.Empower > 0) await PowerCmd.Apply<EmpowerPower>(context, Owner.Creature, DynamicVars["Empower"].BaseValue, Owner.Creature, this);
        if (Spec.Mirror > 0) await PowerCmd.Apply<MirrorImagePower>(context, Owner.Creature, DynamicVars["Mirror"].BaseValue, Owner.Creature, this);
        bool paid = true;
        if (Spec.Burn)
        {
            var selected = (await CardSelectCmd.FromHand(context, Owner, new CardSelectorPrefs(CardSelectorPrefs.ExhaustSelectionPrompt, 1), c => c != this, this)).FirstOrDefault();
            paid = selected != null;
            if (selected != null) await CardCmd.Exhaust(context, selected);
        }
        if (Spec.HpLoss > 0)
            await CreatureCmd.Damage(context, Owner.Creature, Spec.HpLoss, ValueProp.Unblockable | ValueProp.Unpowered | ValueProp.Move, this);
        if (Owner.Creature.IsDead) return;
        if (Spec.Slots > 0 && paid) await Arcana.Gain(context, Owner.Creature, (int)DynamicVars["Slots"].BaseValue, this);
        if (Spec.RestoreAll) await Arcana.Gain(context, Owner.Creature, Arcana.Cap(Owner.Creature), this);
        if (Spec.DelayedSlots > 0) await PowerCmd.Apply<DelayedRecoveryPower>(context, Owner.Creature, DynamicVars["DelayedSlots"].BaseValue, Owner.Creature, this);
        if (Spec.Prepare)
        {
            var selected = (await CardSelectCmd.FromCombatPile(context, PileType.Draw.GetPile(Owner), Owner,
                new CardSelectorPrefs(SelectionScreenPrompt, 1), c => c is WizardCard { Spec.Upcast: true })).FirstOrDefault();
            if (selected != null)
            {
                await CardPileCmd.Add(selected, PileType.Hand);
                CardCmd.ApplyKeyword(selected, CardKeyword.Retain);
            }
        }
        if (Spec.Draw > 0) await CardPileCmd.Draw(context, DynamicVars["Draw"].BaseValue, Owner);
        if (Spec.Energy > 0) await PlayerCmd.GainEnergy(Spec.Energy, Owner);
        int power = (int)DynamicVars["Power"].BaseValue;
        if (Spec.Concentration == "Ward") await Arcana.Concentrate<ArcaneWardPower>(context, Owner.Creature, power, this);
        if (Spec.Concentration == "Evocation") await Arcana.Concentrate<EvocationPower>(context, Owner.Creature, power, this);
        if (Spec.Concentration == "Meditation") await Arcana.Concentrate<MeditationPower>(context, Owner.Creature, power, this);
    }
    protected override void OnUpgrade()
    {
        if (Spec.DamageUp > 0) DynamicVars.Damage.UpgradeValueBy(Spec.DamageUp);
        if (Spec.BlockUp > 0) DynamicVars.Block.UpgradeValueBy(Spec.BlockUp);
        DynamicVars["Draw"].UpgradeValueBy(Spec.DrawUp);
        DynamicVars["Slots"].UpgradeValueBy(Spec.SlotsUp);
        DynamicVars["Power"].UpgradeValueBy(Spec.PowerUp);
        DynamicVars["Empower"].UpgradeValueBy(Spec.EmpowerUp);
        DynamicVars["Mirror"].UpgradeValueBy(Spec.MirrorUp);
        DynamicVars["DelayedSlots"].UpgradeValueBy(Spec.DelayedSlotsUp);
    }

    public string UpcastPreview(int tier)
    {
        List<string> lines = [];
        void Line(string key, decimal amount, int hits = 1)
        {
            var loc = new LocString("cards", "DNDWIZARD-UPCAST_OPTION.preview." + key);
            loc.Add("Value", amount);
            loc.Add("Hits", hits);
            lines.Add(loc.GetFormattedText());
        }
        // These are explicit base values; ordinary Strength/Weak/Vulnerable modifiers
        // are applied by the engine when the original spell resolves.
        if (Spec.Damage > 0) Line(Spec.All ? "allDamage" : "damage", DynamicVars.Damage.BaseValue + tier * Spec.BonusDamage, Spec.Hits + tier * Spec.BonusHits);
        if (Spec.Block > 0) Line("block", DynamicVars.Block.BaseValue + tier * Spec.BonusBlock);
        if (Spec.Weak > 0) Line("weak", Spec.Weak + tier * Spec.BonusWeak);
        if (Spec.Vulnerable > 0) Line("vulnerable", Spec.Vulnerable);
        if (Spec.Poison > 0) Line("poison", Spec.Poison + tier * Spec.BonusPoison);
        if (tier > 0 && Spec.UpcastWeak > 0) Line("allWeak", tier * Spec.UpcastWeak);
        if (tier > 0 && Spec.Damage > 0 && Owner.Creature.GetPower<EmpowerPower>() is { } empower) Line("empower", empower.Amount);
        if (tier > 0 && Owner.Creature.GetPower<ArcaneWardPower>() is { } ward) Line("ward", ward.Amount);
        if (tier > 0 && Owner.Relics.Any(r => r is RunicFocus)) Line("ward", 2);
        return string.Join("\n", lines);
    }
}
