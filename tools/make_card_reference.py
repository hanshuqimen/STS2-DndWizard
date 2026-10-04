from pathlib import Path
import re, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from generate_content import CARDS, desc
lines=['# 法师卡牌图鉴','', '括号中的数值为升级后数值；升环在牌面基础效果之外额外结算。','', '| 卡牌 | 费用 | 类型 / 稀有度 | 效果 |','|---|---:|---|---|']
for c in CARDS:
    def replace(m):
        k=m[1]; v=c.get(k,0); u=c.get(k+'Up',0)
        return str(v)+(f'（{v+u}）' if u else '')
    text=re.sub(r'\{(\w+)(?::diff\(\))?\}',replace,desc(c,True)).replace('\n','<br>')
    typ={'Attack':'攻击','Skill':'技能','Power':'能力'}[c['Type']]
    rarity={'Basic':'初始','Common':'普通','Uncommon':'罕见','Rare':'稀有'}[c['Rarity']]
    lines.append(f"| {c['Name']} | {c['Cost']} | {typ} / {rarity} | {text} |")
(Path(__file__).resolve().parents[1]/'CARDS.zh-CN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
