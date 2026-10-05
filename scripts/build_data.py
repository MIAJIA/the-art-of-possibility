"""Build data/data.json from the V-Dem v16 dataset.

Usage:  python scripts/build_data.py path/to/vdem.RData

vdem.RData ships with the vdemdata R package
(https://github.com/vdeminstitute/vdemdata, file data/vdem.RData).
Requires: pandas, numpy, pyreadr.
"""
import sys, json, math, warnings
from pathlib import Path
import numpy as np, pandas as pd, pyreadr
warnings.filterwarnings('ignore')

RDATA = sys.argv[1] if len(sys.argv) > 1 else 'vdem.RData'
OUT = Path(__file__).resolve().parent.parent / 'data' / 'data.json'

raw = pyreadr.read_r(RDATA)
raw = raw[list(raw.keys())[0]]
cols = ['country_name', 'country_text_id', 'year', 'v2x_polyarchy', 'v2x_rule',
        'v2svstterr', 'v2clrspct', 'v2stfisccap', 'v2stcritrecadm', 'e_gdppc']
df = raw[cols].copy()
df['year'] = df.year.astype(int)

# State capacity: mean of four V-Dem indicators, each standardised on all
# country-years from 1900 on; needs at least three of the four.
base = df[df.year >= 1900]
z = lambda c: (df[c] - base[c].mean()) / base[c].std()
parts = pd.DataFrame({'terr': z('v2svstterr'), 'adm': z('v2clrspct'),
                      'fisc': z('v2stfisccap'), 'merit': z('v2stcritrecadm')})
a4 = parts.mean(axis=1, skipna=True)
a4[parts.notna().sum(axis=1) < 3] = np.nan
LO, HI = -2.3, 1.9          # linear map to 0..1; 0 (the 1900-2025 mean) lands at 0.548
df['cap'] = ((a4 - LO) / (HI - LO)).clip(0, 1)

# Income: V-Dem's GDP per capita estimate as a share of the US level that year.
us = df[df.country_text_id == 'USA'].set_index('year').e_gdppc
df['rel'] = df.e_gdppc / df.year.map(us) * 100

ZH={'AFG':'阿富汗','AGO':'安哥拉','ALB':'阿尔巴尼亚','ARE':'阿联酋','ARG':'阿根廷','ARM':'亚美尼亚','AUS':'澳大利亚','AUT':'奥地利','AZE':'阿塞拜疆','BDI':'布隆迪','BEL':'比利时','BEN':'贝宁','BFA':'布基纳法索','BGD':'孟加拉国','BGR':'保加利亚','BHR':'巴林','BIH':'波黑','BLR':'白俄罗斯','BOL':'玻利维亚','BRA':'巴西','BRB':'巴巴多斯','BTN':'不丹','BWA':'博茨瓦纳','CAF':'中非','CAN':'加拿大','CHE':'瑞士','CHL':'智利','CHN':'中国','CIV':'科特迪瓦','CMR':'喀麦隆','COD':'刚果（金）','COG':'刚果（布）','COL':'哥伦比亚','COM':'科摩罗','CPV':'佛得角','CRI':'哥斯达黎加','CUB':'古巴','CYP':'塞浦路斯','CZE':'捷克','DEU':'德国','DJI':'吉布提','DNK':'丹麦','DOM':'多米尼加','DZA':'阿尔及利亚','ECU':'厄瓜多尔','EGY':'埃及','ERI':'厄立特里亚','ESP':'西班牙','EST':'爱沙尼亚','ETH':'埃塞俄比亚','FIN':'芬兰','FJI':'斐济','FRA':'法国','GAB':'加蓬','GBR':'英国','GEO':'格鲁吉亚','GHA':'加纳','GIN':'几内亚','GMB':'冈比亚','GNB':'几内亚比绍','GNQ':'赤道几内亚','GRC':'希腊','GTM':'危地马拉','GUY':'圭亚那','HKG':'香港','HND':'洪都拉斯','HRV':'克罗地亚','HTI':'海地','HUN':'匈牙利','IDN':'印度尼西亚','IND':'印度','IRL':'爱尔兰','IRN':'伊朗','IRQ':'伊拉克','ISL':'冰岛','ISR':'以色列','ITA':'意大利','JAM':'牙买加','JOR':'约旦','JPN':'日本','KAZ':'哈萨克斯坦','KEN':'肯尼亚','KGZ':'吉尔吉斯斯坦','KHM':'柬埔寨','KOR':'韩国','KWT':'科威特','LAO':'老挝','LBN':'黎巴嫩','LBR':'利比里亚','LBY':'利比亚','LKA':'斯里兰卡','LSO':'莱索托','LTU':'立陶宛','LUX':'卢森堡','LVA':'拉脱维亚','MAR':'摩洛哥','MDA':'摩尔多瓦','MDG':'马达加斯加','MDV':'马尔代夫','MEX':'墨西哥','MKD':'北马其顿','MLI':'马里','MLT':'马耳他','MMR':'缅甸','MNE':'黑山','MNG':'蒙古','MOZ':'莫桑比克','MRT':'毛里塔尼亚','MUS':'毛里求斯','MWI':'马拉维','MYS':'马来西亚','NAM':'纳米比亚','NER':'尼日尔','NGA':'尼日利亚','NIC':'尼加拉瓜','NLD':'荷兰','NOR':'挪威','NPL':'尼泊尔','NZL':'新西兰','OMN':'阿曼','PAK':'巴基斯坦','PAN':'巴拿马','PER':'秘鲁','PHL':'菲律宾','PNG':'巴布亚新几内亚','POL':'波兰','PRK':'朝鲜','PRT':'葡萄牙','PRY':'巴拉圭','PSE':'巴勒斯坦（西岸）','PSG':'巴勒斯坦（加沙）','QAT':'卡塔尔','ROU':'罗马尼亚','RUS':'俄罗斯','RWA':'卢旺达','SAU':'沙特阿拉伯','SDN':'苏丹','SEN':'塞内加尔','SGP':'新加坡','SLB':'所罗门群岛','SLE':'塞拉利昂','SLV':'萨尔瓦多','SML':'索马里兰','SOM':'索马里','SRB':'塞尔维亚','SSD':'南苏丹','STP':'圣多美和普林西比','SUR':'苏里南','SVK':'斯洛伐克','SVN':'斯洛文尼亚','SWE':'瑞典','SWZ':'斯威士兰','SYC':'塞舌尔','SYR':'叙利亚','TCD':'乍得','TGO':'多哥','THA':'泰国','TJK':'塔吉克斯坦','TKM':'土库曼斯坦','TLS':'东帝汶','TTO':'特立尼达和多巴哥','TUN':'突尼斯','TUR':'土耳其','TWN':'台湾','TZA':'坦桑尼亚','UGA':'乌干达','UKR':'乌克兰','URY':'乌拉圭','USA':'美国','UZB':'乌兹别克斯坦','VEN':'委内瑞拉','VNM':'越南','VUT':'瓦努阿图','XKX':'科索沃','YEM':'也门','ZAF':'南非','ZMB':'赞比亚','ZWE':'津巴布韦','ZZB':'桑给巴尔',
'BDN':'巴登','BRW':'不伦瑞克','BVR':'巴伐利亚','DDR':'东德','HDM':'黑森-达姆施塔特','HKS':'黑森-卡塞尔','HRG':'汉堡','HVR':'汉诺威','MCL':'梅克伦堡-什未林','MDN':'摩德纳','NSS':'拿骚','OLD':'奥尔登堡','PPS':'教皇国','PRM':'帕尔马','PSB':'巴勒斯坦（英国托管）','SAX':'萨克森-魏玛-艾森纳赫','SPD':'皮埃蒙特-撒丁','SXN':'萨克森','TSC':'托斯卡纳','TWS':'两西西里','VDR':'南越','WRG':'符腾堡','YMD':'南也门'}
ids=sorted(df.country_text_id.unique()); miss=[i for i in ids if i not in ZH]; assert not miss, miss
A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
def enc(vals):
    out=[]
    for v in vals:
        if v is None or (isinstance(v,float) and math.isnan(v)): out.append('~~')
        else:
            n=int(round(min(max(v,0),1)*4095)); out.append(A[n>>6]+A[n&63])
    return ''.join(out)
GLO,GHI=math.log10(0.5),math.log10(400)
df['g']=(np.log10(df.rel)-GLO)/(GHI-GLO)
# carry gdp forward after last obs
df=df.sort_values(['country_text_id','year'])
df['g_ff']=df.groupby('country_text_id').g.ffill(limit=6)
# component percentiles within year
comps={'t':'v2svstterr','a':'v2clrspct','f':'v2stfisccap','m':'v2stcritrecadm'}
for k,c in comps.items():
    df['pc_'+k]=df.groupby('year')[c].rank(pct=True)
units={}; comp={}
for cid,d in df.groupby('country_text_id'):
    d=d.set_index('year'); ys=range(int(d.index.min()),int(d.index.max())+1); d=d.reindex(ys)
    units[cid]={'n':ZH[cid],'s':ys[0],'p':enc(d.v2x_polyarchy.tolist()),'c':enc(d.cap.tolist()),'r':enc(d.v2x_rule.tolist()),'g':enc(d.g_ff.tolist())}
    comp[cid]={k:enc(d['pc_'+k].tolist()) for k in comps}
    comp[cid]['T']=enc((d.v2svstterr/100).tolist())
out={'y0':1789,'y1':2025,'glo':GLO,'ghi':GHI,'units':units,'comp':comp}
OUT.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('wrote',OUT,len(units),'units')
