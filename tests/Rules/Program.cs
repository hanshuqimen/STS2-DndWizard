using DndWizard;

int checks = 0;
void Check(bool value, string reason)
{
    checks++;
    if (!value) throw new Exception(reason);
}
Check(SpellbookRules.Level(0) == 1 && SpellbookRules.Level(2) == 1, "Initial level");
Check(SpellbookRules.Level(3) == 2 && SpellbookRules.Level(6) == 2, "First milestone");
Check(SpellbookRules.Level(7) == 3 && SpellbookRules.Level(11) == 3, "Second milestone");
Check(SpellbookRules.Level(12) == 4, "Mastery");
Check(SpellbookRules.MaxTier(11) == 3 && SpellbookRules.MaxTier(12) == 4, "Tier 4 unlock");
Check(SpellbookRules.HpPerSlot(6) == 4 && SpellbookRules.HpPerSlot(7) == 3, "Blood efficiency unlock");
Check(SpellbookRules.Quote(3, 1, 20, 0, false, false) == new CastingPayment(1, 8, true, true), "Partial slot payment");
Check(SpellbookRules.Quote(1, 0, 1, 0, true, true) == new CastingPayment(0, 0, false, true), "Discount bypasses blood payment without using Overcast");
Check(!SpellbookRules.Quote(2, 0, 8, 0, false, false).Allowed, "Exactly lethal choice rejected");
Check(!SpellbookRules.Quote(1, 0, 50, 0, false, true).Allowed, "Only one Overcast per combat");
Check(SpellbookRules.Quote(3, 3, 1, 0, false, true).Allowed, "Regular Upcast after Overcast remains available");
for (int xp = 0; xp <= 12; xp++)
for (int slots = 0; slots <= 11; slots++)
for (int tier = 0; tier <= 5; tier++)
foreach (bool discount in new[] { false, true })
{
    var q = SpellbookRules.Quote(tier, slots, 100, xp, discount, false);
    Check(q.Slots >= 0 && q.Slots <= slots && q.Hp >= 0, "No negative or invented resources");
    if (q.Allowed)
        Check(q.Slots + q.Hp / SpellbookRules.HpPerSlot(xp) == Math.Max(0, tier - (discount && tier > 0 ? 1 : 0)), "Payment conserves required slot cost");
    Check(tier <= SpellbookRules.MaxTier(xp) || !q.Allowed, "Cannot bypass tier unlock");
    if (tier == 0) Check(q == new CastingPayment(0, 0, false, true), "Base casting is always free");
}
Console.WriteLine($"PASS: {checks} offline rule assertions; no game assemblies loaded.");
