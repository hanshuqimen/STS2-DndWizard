"""Authoring source: card specifications, bilingual localization and reproducible C# classes."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CARDS = []
def card(id, zh, cost, type='Attack', rarity='Common', **kw):
    CARDS.append(dict(Id=id, Name=zh, Cost=cost, Type=type, Rarity=rarity, **kw))
card('FireBolt','火焰箭',1,rarity='Basic',Damage=6,DamageUp=3,Cantrip=True)
card('MageArmor','法师护甲',1,'Skill','Basic',Block=5,BlockUp=3)
card('MagicMissile','魔法飞弹',1,rarity='Basic',Damage=3,DamageUp=1,Hits=3,Upcast=True,BonusHits=1)
card('ArcaneRecovery','奥术回想',1,'Skill','Basic',Slots=2,SlotsUp=1,Draw=1)
card('RayOfFrost','冰霜射线',1,Damage=6,DamageUp=3,Weak=1,Cantrip=True)
card('ShockingGrasp','电爪',0,Damage=3,DamageUp=2,Cantrip=True)
card('AcidSplash','酸液飞溅',1,Damage=5,DamageUp=3,All=True,Cantrip=True)
card('Shield','护盾术',1,'Skill',Block=7,BlockUp=3,Upcast=True,BonusBlock=6,Retain=True)
card('BurningHands','燃烧之手',1,Damage=6,DamageUp=2,All=True,Upcast=True,BonusDamage=4)
card('ChromaticOrb','繁彩球',1,Damage=8,DamageUp=3,Upcast=True,BonusDamage=6)
card('Thunderwave','雷鸣波',1,Damage=5,DamageUp=2,Block=4,BlockUp=2,All=True,Upcast=True,BonusDamage=3)
card('FalseLife','虚假生命',1,'Skill',Block=10,BlockUp=4,Exhaust=True)
card('StudySpellbook','研读法术书',1,'Skill',Draw=2,DrawUp=1)
card('RitualCasting','仪式施法',1,'Skill',Block=4,BlockUp=2,Slots=1,SlotsUp=1)
card('TrueStrike','克敌机先',1,Damage=5,DamageUp=2,Empower=2,EmpowerUp=1)
card('WitchBolt','巫术箭',1,Damage=7,DamageUp=3,Upcast=True,BonusDamage=4,VsWeak=4,Draw=1)
card('Fireball','火球术',2,rarity='Uncommon',Damage=13,DamageUp=4,All=True,Upcast=True,BonusDamage=7)
card('ScorchingRay','灼热射线',2,rarity='Uncommon',Damage=4,DamageUp=1,Hits=3,Upcast=True,BonusHits=1)
card('MistyStep','迷踪步',0,'Skill','Uncommon',Block=4,BlockUp=3,Draw=1,Exhaust=True)
card('MirrorImage','镜影术',1,'Skill','Uncommon',Block=5,BlockUp=3,Mirror=2,MirrorUp=1)
card('Web','蛛网术',1,'Skill','Uncommon',Weak=2,Vulnerable=1,Draw=1,DrawUp=1,Upcast=True,BonusWeak=1)
card('MelfsAcidArrow','马友夫强酸箭',1,rarity='Uncommon',Damage=5,DamageUp=3,Poison=4,Upcast=True,BonusPoison=3)
card('Counterspell','法术反制',1,'Skill','Uncommon',Block=6,BlockUp=3,Counter=True,Retain=True)
card('ArcaneWard','奥术守御',1,'Power','Uncommon',Concentration='Ward',Power=4,PowerUp=2)
card('SculptSpells','塑能专精',1,'Power','Uncommon',Concentration='Evocation',Power=2,PowerUp=1)
card('DeepMeditation','深度冥想',1,'Power','Uncommon',Concentration='Meditation',Power=1,PowerUp=1)
card('ConeOfCold','寒冰锥',2,rarity='Rare',Damage=15,DamageUp=5,All=True,Upcast=True,BonusDamage=6,UpcastWeak=1)
card('Disintegrate','解离术',3,rarity='Rare',Damage=30,DamageUp=9,Upcast=True,BonusDamage=18,Exhaust=True)
card('GlobeOfInvulnerability','法术无效结界',2,'Skill','Rare',Block=18,BlockUp=6,Mirror=3,MirrorUp=1,Upcast=True,BonusBlock=8,Exhaust=True)
card('Wish','祈愿术',1,'Skill','Rare',Slots=3,SlotsUp=1,Draw=2,DrawUp=1,Energy=1,Exhaust=True)
card('ChainLightning','连锁闪电',2,rarity='Rare',Damage=8,DamageUp=2,Hits=2,All=True,Upcast=True,BonusDamage=4)
card('Foresight','预知术',1,'Skill','Rare',Block=8,BlockUp=3,Draw=3,DrawUp=1,Exhaust=True)
card('ShortMeditation','短暂冥想',0,'Skill',DelayedSlots=2,DelayedSlotsUp=1,Exhaust=True)
card('BurnScroll','焚卷回能',0,'Skill',Burn=True,Slots=2,SlotsUp=1,Exhaust=True)
card('LifeConversion','生命转化',0,'Skill','Uncommon',HpLoss=4,Slots=2,SlotsUp=1,Exhaust=True)
card('GreaterArcaneRecovery','高等奥术回想',2,'Skill','Rare',RestoreAll=True,Draw=1,DrawUp=1,Exhaust=True)
card('PrepareSpell','准备法术',1,'Skill','Uncommon',Prepare=True,Block=4,BlockUp=3,Exhaust=True)

def slug(name): return re.sub(r'(?<!^)(?=[A-Z])','_',name).upper()
def desc(c, zh):
    t=[]
    if c.get('Cantrip'): t.append('戏法。' if zh else 'Cantrip.')
    if c.get('Damage'):
        t.append(('对所有敌人' if c.get('All') else '')+'造成 {Damage:diff()} 点伤害'+(f"，重复 {c['Hits']} 次" if c.get('Hits',1)>1 else '')+'。' if zh else 'Deal {Damage:diff()} damage'+(' to ALL enemies' if c.get('All') else '')+(f" {c['Hits']} times" if c.get('Hits',1)>1 else '')+'.')
    if c.get('Block'): t.append('获得 {Block:diff()} 点格挡。' if zh else 'Gain {Block:diff()} Block.')
    for k,z,e in [('Weak','虚弱','Weak'),('Vulnerable','易伤','Vulnerable'),('Poison','中毒','Poison')]:
        if c.get(k): t.append(f"给予 {c[k]} 层{z}。" if zh else f"Apply {c[k]} {e}.")
    if c.get('Burn'): t.append('选择并消耗另一张手牌，成功后：' if zh else 'Choose and Exhaust another card in your hand. If successful:')
    if c.get('HpLoss'): t.append(f"失去 {c['HpLoss']} 点生命。" if zh else f"Lose {c['HpLoss']} HP.")
    if c.get('Slots'): t.append('恢复 {Slots:diff()} 点法术位（不超过当前上限）。' if zh else 'Recover {Slots:diff()} Spell Slots, up to your current capacity.')
    if c.get('DelayedSlots'): t.append('下回合开始时，恢复 {DelayedSlots:diff()} 点法术位。' if zh else 'At the start of your next turn, recover {DelayedSlots:diff()} Spell Slots.')
    if c.get('RestoreAll'): t.append('恢复全部法术位。' if zh else 'Restore ALL Spell Slots.')
    if c.get('Prepare'): t.append('从抽牌堆选择一张可升环法术，加入手牌，并使其在本场战斗中获得保留。' if zh else 'Choose an Upcast spell in your draw pile. Put it into your hand and give it Retain this combat.')
    if c.get('Draw'): t.append('抽 {Draw:diff()} 张牌。' if zh else 'Draw {Draw:diff()} cards.')
    if c.get('Energy'): t.append('获得 1 点能量。' if zh else 'Gain 1 Energy.')
    if c.get('Empower'): t.append('获得 {Empower:diff()} 点奥术蓄势（下一张升环攻击每击增伤，随后消耗）。' if zh else 'Gain {Empower:diff()} Empower (bonus damage per hit on your next Upcast attack, then consumed).')
    if c.get('Mirror'): t.append('获得 {Mirror:diff()} 层镜影（每层使一次未被格挡的攻击生命损失减少 4）。' if zh else 'Gain {Mirror:diff()} Mirror Images (each reduces HP lost from an unblocked attack by 4).')
    if c.get('VsWeak'): t.append(f"若目标已有虚弱，额外造成 {c['VsWeak']} 点伤害。" if zh else f"Deal {c['VsWeak']} additional damage if the target is already Weak.")
    if c.get('Counter'): t.append('若目标正准备攻击，给予 2 层虚弱并恢复 1 点法术位。' if zh else 'If the target intends to attack, apply 2 Weak and recover 1 Spell Slot.')
    if c.get('Upcast'):
        bonus=[]
        if c.get('BonusDamage'): bonus.append('每次伤害 +{BonusDamage}' if zh else '+{BonusDamage} damage per hit')
        if c.get('BonusBlock'): bonus.append('格挡 +{BonusBlock}' if zh else '+{BonusBlock} Block')
        if c.get('BonusPoison'): bonus.append(f"额外给予 {c['BonusPoison']} 层中毒" if zh else f"apply {c['BonusPoison']} additional Poison")
        if c.get('BonusHits'): bonus.append(f"攻击次数 +{c['BonusHits']}" if zh else f"+{c['BonusHits']} hits")
        if c.get('BonusWeak'): bonus.append(f"额外给予 {c['BonusWeak']} 层虚弱" if zh else f"apply {c['BonusWeak']} additional Weak")
        if c.get('UpcastWeak'): bonus.append(f"给予所有敌人 {c['UpcastWeak']} 层虚弱" if zh else f"apply {c['UpcastWeak']} Weak to ALL enemies")
        t.append(('可选升环（初始最多 3 阶，法术书满级 4 阶），每阶消耗 1 法术位并'+ '，'.join(bonus)+'。也可选择基础施法。') if zh else ('Choose base casting or Upcast (up to 3 tiers, 4 with a mastered spellbook). Each tier costs 1 Spell Slot and grants '+', '.join(bonus)+'.'))
    p=c.get('Concentration')
    if p:
        text={'Ward':('每次升环获得 {Power:diff()} 点格挡。','Gain {Power:diff()} Block whenever you Upcast.'),'Evocation':('你的法师攻击牌每次伤害 +{Power:diff()}。','Your Wizard attacks deal {Power:diff()} additional damage per hit.'),'Meditation':('下回合起，每回合开始恢复 {Power:diff()} 点法术位。','At the start of each following turn, recover {Power:diff()} Spell Slots.')}
        t.append(('专注（替换已有专注）：' if zh else 'Concentration (replaces existing Concentration): ')+text[p][0 if zh else 1])
        t.append('切换自另一种专注时，恢复 1 点法术位。' if zh else 'Recover 1 Spell Slot when switching from a different Concentration.')
    if c.get('Retain'): t.append('保留。' if zh else 'Retain.')
    if c.get('Exhaust'): t.append('消耗。' if zh else 'Exhaust.')
    return '\n'.join(t)

def main():
    code=['// Generated by generate_content.py; edit the authoring data to add cards.','using MegaCrit.Sts2.Core.Entities.Cards;','namespace DndWizard;']
    for c in CARDS:
        args=[json.dumps(c['Id']),str(c['Cost']),'CardType.'+c['Type'],'CardRarity.'+c['Rarity']]
        for k,v in c.items():
            if k in ['Id','Name','Cost','Type','Rarity']: continue
            val=str(v).lower() if isinstance(v,bool) else json.dumps(v)
            args.append(f'{k}: {val}')
        code.append(f'public sealed class {c["Id"]}() : WizardCard(new SpellSpec({", ".join(args)}));')
    (ROOT/'Code/Cards.g.cs').write_text('\n'.join(code),encoding='utf-8')
    for lang in ['eng','zhs']:
        loc=ROOT/'DndWizard/localization'/lang
        loc.mkdir(parents=True,exist_ok=True)
        zh=lang=='zhs'
        cards={}
        for c in CARDS:
            key='DNDWIZARD-'+slug(c['Id'])
            cards[key+'.title']=c['Name'] if zh else re.sub(r'(?<!^)(?=[A-Z])',' ',c['Id'])
            cards[key+'.description']=desc(c,zh)
        cards['DNDWIZARD-PREPARE_SPELL.selectionScreenPrompt']='选择一张可升环法术' if zh else 'Choose an Upcast spell'
        cards['DNDWIZARD-UPCAST_OPTION.overcastTitle']='超限施法' if zh else 'Overcast'
        cards['DNDWIZARD-UPCAST_OPTION.title']='施法方案' if zh else 'Casting option'
        cards['DNDWIZARD-UPCAST_OPTION.selectionScreenPrompt']='选择基础施法（0 阶）或升环施法' if zh else 'Choose base casting (tier 0) or Upcast'
        cards['DNDWIZARD-UPCAST_OPTION.description']=('升环阶数：{Tier}（0 为基础施法）\n消耗 {Cost} 法术位与 {HpCost} 生命；当前 {Current}/{Capacity}。\n{Effects}\n生命代价大于 0 即超限，每战限一次。列出基础数值，原牌其他效果照常生效。' if zh else 'Tier: {Tier} (0 = base casting)\nSpend {Cost} Spell Slots and lose {HpCost} HP; currently {Current}/{Capacity}.\n{Effects}\nHP payment is Overcast, once per combat. Base values shown; status modifiers and other spell effects still apply.')
        for key,z,e in [
            ('damage','基础伤害 {Value} × {Hits} 次。','Base damage: {Value} × {Hits} hits.'),
            ('allDamage','对所有敌人基础伤害 {Value} × {Hits} 次。','Base damage to ALL enemies: {Value} × {Hits} hits.'),
            ('block','基础格挡 {Value}。','Base Block: {Value}.'),
            ('weak','给予 {Value} 层虚弱。','Apply {Value} Weak.'),
            ('vulnerable','给予 {Value} 层易伤。','Apply {Value} Vulnerable.'),
            ('poison','给予 {Value} 层中毒。','Apply {Value} Poison.'),
            ('allWeak','给予所有敌人 {Value} 层虚弱。','Apply {Value} Weak to ALL enemies.'),
            ('empower','消耗蓄势：每击另加 {Value} 伤害。','Consume Empower: +{Value} damage per hit.'),
            ('ward','升环联动：另获 {Value} 格挡。','Upcast synergy: gain {Value} additional Block.')]:
            cards['DNDWIZARD-UPCAST_OPTION.preview.'+key]=z if zh else e
        characters={
            'DNDWIZARD-WIZARD.title':'法师' if zh else 'The Wizard',
            'DNDWIZARD-WIZARD.titleObject':'法师' if zh else 'the Wizard',
            'DNDWIZARD-WIZARD.description': '一位带着法术书踏入尖塔的奥术学者。\n以戏法应敌，消耗法术位升环，在专注与爆发之间作出选择。' if zh else 'An arcane scholar carrying a spellbook into the Spire.\nCast cantrips, spend spell slots to Upcast, and choose your Concentration.',
            'DNDWIZARD-WIZARD.pronounSubject':'他' if zh else 'he',
            'DNDWIZARD-WIZARD.pronounObject':'他' if zh else 'him',
            'DNDWIZARD-WIZARD.pronounPossessive':'他的' if zh else 'his',
            'DNDWIZARD-WIZARD.possessiveAdjective':'他的' if zh else 'his',
            'DNDWIZARD-WIZARD.cardsModifierTitle':'法师卡牌' if zh else 'Wizard Cards',
            'DNDWIZARD-WIZARD.cardsModifierDescription':'法师卡牌将出现在奖励和商店中。' if zh else 'Wizard cards appear in rewards and shops.',
            'DNDWIZARD-WIZARD.goldMonologue':'更多的抄写墨水。' if zh else 'More ink for my spellbook.',
            'DNDWIZARD-WIZARD.aromaPrinciple':'准备好了吗？' if zh else 'Prepared?',
            'DNDWIZARD-WIZARD.banter.alive.endTurnPing':'下一步。' if zh else 'Your move.',
            'DNDWIZARD-WIZARD.banter.dead.endTurnPing':'知识长存。' if zh else 'Knowledge endures.',
        }
        powers={}
        for id,z,e,zd,ed in [
            ('SpellSlotsPower','法术位','Spell Slots','当前 {Amount}/{Capacity}。可选择基础施法或升环（初始最多 3 阶，法术书满级 4 阶）。法术位不足可每战一次用生命补足。法术位跨战斗保留；营火选择休息时回满。上限基础为 6，可由遗物提高。','Currently {Amount}/{Capacity}. Choose base casting or Upcast (3 tiers, 4 at spellbook level 4). Once per combat, missing slots can be paid with HP. Slots persist across combats and refill when you choose Rest. Base capacity 6; relics can increase it.'),
            ('ArcaneWardPower','专注：奥术守御','Concentration: Arcane Ward','每次升环获得 {Amount} 点格挡。被其他专注法术替换。','Gain {Amount} Block whenever you Upcast. Replaced by another Concentration spell.'),
            ('EvocationPower','专注：塑能','Concentration: Evocation','法师攻击牌每次伤害增加 {Amount}。被其他专注法术替换。','Wizard attacks deal {Amount} extra damage per hit. Replaced by another Concentration spell.'),
            ('MeditationPower','专注：冥想','Concentration: Meditation','每回合开始恢复 {Amount} 点法术位，不超过当前上限。被其他专注法术替换。','At the start of your turn, recover {Amount} Spell Slots, up to your capacity. Replaced by another Concentration spell.'),
            ('DelayedRecoveryPower','延迟回想','Delayed Recovery','下回合开始时，恢复 {Amount} 点法术位，随后移除此效果。战斗结束时失效。','At the start of your next turn, recover {Amount} Spell Slots, then remove this effect. Expires when combat ends.'),
            ('OvercastSpentPower','超限已使用','Overcast Spent','本场战斗已使用超限施法，不能再用生命补足法术位。仍可正常升环；下场战斗重置。','Overcast has been used this combat. You cannot pay missing slots with HP again until next combat. Normal Upcast remains available.'),
            ('FocusSpentPower','法器已聚焦','Focus Spent','本场战斗已使用首次升环减免。下一场战斗重新可用。','Your first-Upcast discount has been used this combat. Available again next combat.')]:
            key='DNDWIZARD-'+slug(id)
            powers[key+'.title']=z if zh else e
            powers[key+'.description']=zd if zh else ed
            powers[key+'.smartDescription']=zd if zh else ed
        for id,z,e,zd,ed in [
            ('EmpowerPower','奥术蓄势','Empower','下一张升环攻击每击额外造成 {Amount} 点伤害，随后消耗全部蓄势。未升环的攻击和升环防御不消耗蓄势。','Your next Upcast attack deals {Amount} additional damage per hit, then consumes all Empower. Other cards do not consume it.'),
            ('MirrorImagePower','镜影','Mirror Images','受到未被格挡的攻击伤害时，消耗 1 层，使此次生命损失减少 4。完全格挡不消耗；不抵挡中毒或其他非攻击失血。','When an attack would deal unblocked damage, consume 1 stack to reduce HP lost by 4. Fully blocked attacks and non-attack HP loss do not consume it.'),
            ('CantripProgressPower','戏法研习','Cantrip Study','旅行法术书：每施放两次戏法恢复 1 点法术位。每回合最多触发一次，未完成进度跨回合保留；当前进度 {Amount}/2。','Traveling Spellbook: every two Cantrips recover 1 Spell Slot, at most once per turn. Incomplete progress persists across turns; current progress {Amount}/2.'),
            ('CantripSpentPower','研习已触发','Study Complete','本回合已通过戏法恢复过法术位。下回合重新开放戏法研习。','Cantrip recovery has triggered this turn. It becomes available again next turn.')]:
            key='DNDWIZARD-'+slug(id)
            powers[key+'.title']=z if zh else e
            powers[key+'.description']=zd if zh else ed
            powers[key+'.smartDescription']=zd if zh else ed
        relics={}
        for id,z,e,zd,ed in [
            ('Spellbook','旅行法术书','Traveling Spellbook','法术位 {Current}/{Capacity}。开局拥有 6 点法术位；跨战斗保留。营火选择休息恢复全部法术位；锻造不恢复。','Spell Slots: {Current}/{Capacity}. Start your run with 6 slots; slots persist across combats. Choosing Rest restores all slots; Smith does not.'),
            ('PearlOfPower','法力珍珠','Pearl of Power','每场战斗开始时，恢复 2 点法术位，不超过当前上限。','At the start of combat, recover 2 Spell Slots, up to your capacity.'),
            ('RunicFocus','符文法器','Runic Focus','每次升环，获得 2 点格挡。','Whenever you Upcast, gain 2 Block.'),
            ('ExpandedGrimoire','扩容法典','Expanded Grimoire','法术位上限增加 2（不立即恢复法术位）。','Increase Spell Slot capacity by 2. Does not immediately recover slots.'),
            ('CampfireIncense','营火熏香','Campfire Incense','营火选择休息时，额外恢复 6 点生命。','When you choose Rest at a campfire, heal 6 additional HP.'),
            ('EfficientFocus','节能法器','Efficient Focus','每场战斗首次升环少消耗 1 点法术位，最低为 0。基础施法不消耗此机会。','Your first Upcast each combat costs 1 fewer Spell Slot, minimum 0. Base casting does not use this discount.')]:
            key='DNDWIZARD-'+slug(id)
            relics[key+'.title']=z if zh else e
            relics[key+'.description']=zd if zh else ed
            relics[key+'.flavor']='知识就是力量，但力量需要准备。' if zh else 'Knowledge is power. Power takes preparation.'
        relics['DNDWIZARD-SPELLBOOK.description'] += ('\n法术书 Lv.{Level}；研习 {Research}/{Next}（12 为满级）。获胜：普通 +1、精英 +2、首领 +3。3/7/12 经验升级，每级容量 +1 并填充新增容量。Lv.3 超限每缺位消耗 3 生命（此前 4）；Lv.4 解锁四阶升环。当前最高 {MaxTier} 阶，超限每缺位 {BloodCost} 生命，每战限一次。' if zh else '\nSpellbook Lv.{Level}; research {Research}/{Next} (12 = mastered). Victories: normal +1, elite +2, boss +3. Level at 3/7/12 XP, gaining +1 capacity and filling only that new slot. Lv.3 lowers Overcast HP per missing slot from 4 to 3. Lv.4 unlocks tier 4. Current maximum tier {MaxTier}; Overcast costs {BloodCost} HP per missing slot, once per combat.')
        relics['DNDWIZARD-SPELLBOOK.description'] += ('\n每回合最多一次：每施放两次戏法恢复 1 点法术位；未完成进度跨回合保留。' if zh else '\nOnce per turn: every two Cantrips recover 1 Spell Slot. Incomplete progress persists across turns.')
        relics['DNDWIZARD-SPELLBOOK.restSiteHealText']='恢复全部法术位。' if zh else 'Restore all Spell Slots.'
        for name,data in [('cards',cards),('characters',characters),('powers',powers),('relics',relics)]:
            (loc/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'cards.json').write_text(json.dumps(CARDS,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Generated {len(CARDS)} cards and two localization sets.')
if __name__=='__main__': main()
