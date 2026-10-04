namespace DndWizard;

// Pure rules shared by gameplay, the choice preview and offline checks.
public readonly record struct CastingPayment(int Slots, int Hp, bool Overcast, bool Allowed);
public static class SpellbookRules
{
    public const int MaxExperience = 12;
    public static int Level(int experience) => experience >= 12 ? 4 : experience >= 7 ? 3 : experience >= 3 ? 2 : 1;
    public static int CapacityBonus(int experience) => Level(experience) - 1;
    public static int MaxTier(int experience) => Level(experience) >= 4 ? 4 : 3;
    public static int HpPerSlot(int experience) => Level(experience) >= 3 ? 3 : 4;
    public static int NextThreshold(int experience) => Level(experience) switch { 1 => 3, 2 => 7, _ => 12 };
    public static CastingPayment Quote(int tier, int slots, int hp, int experience, bool discount, bool overcastUsed)
    {
        if (tier < 0 || tier > MaxTier(experience)) return new(0, 0, false, false);
        int cost = Math.Max(0, tier - (discount && tier > 0 ? 1 : 0));
        int paidSlots = Math.Min(Math.Max(0, slots), cost);
        int hpCost = (cost - paidSlots) * HpPerSlot(experience);
        bool overcast = hpCost > 0;
        // Do not offer a knowingly lethal payment; native HP-loss modifiers still apply.
        return new(paidSlots, hpCost, overcast, !overcast || (!overcastUsed && hp > hpCost));
    }
}
