# 政治坐标系 · The Art of Possibility

把刘瑜《可能性的艺术：比较政治学30讲》里的两个维度，做成一张可以交互的图。

An interactive reading companion to Liu Yu's *The Art of Possibility* (可能性的艺术): every country placed on two axes, state capacity and accountability, from 1789 to 2025.

**在线看：** https://miajia.dev/project/the-art-of-possibility/

## 这是什么

书的第一讲用两根轴给国家定位：

- **国家能力**：政府决定的事，在全国真的做得到吗？
- **民主问责**：政府做错了，民众有办法让它改吗？

这个页面把 179 个国家和地区、两百多年的数据放到这两根轴上。你可以：

- 拖动年份，看各国从哪里出发、走到了哪里；
- 点任意圆点，看它的轨迹，最多同时对照三个；
- 按书的章节切换，每一章预选一组对照国家；
- 把坐标轴换成法治或经济发展。

书中 16 个案例国家各有一段"缘起、转折、结果"。

## 数据与方法

数据来自 [V-Dem](https://www.v-dem.net/data/the-v-dem-dataset/) 第 16 版。

| 维度 | 用的指标 |
|---|---|
| 民主问责 | 选举民主指数 `v2x_polyarchy`，0 到 1，参考线 0.5 |
| 国家能力 | 自己合成的指数，见下 |
| 法治 | 法治指数 `v2x_rule` |
| 经济发展 | 人均 GDP 估计值 `e_gdppc`，换算成同年美国水平的百分比 |

**国家能力指数是这个项目自己合成的，书里没有这个数。** 它取四项 V-Dem 指标：

- 国家实际控制的领土比例 `v2svstterr`
- 行政是否严格公正 `v2clrspct`
- 财政主要靠什么收入 `v2stfisccap`
- 官员任用看关系还是看能力 `v2stcritrecadm`

每一项按 1900 年以来全部国家年份标准化，取平均（至少要有三项），再线性换算到 0 到 1。参考线 0.548 是 1900–2025 年的世界平均。它与世界银行"政府效能"指标（1996–2024 年）的相关系数是 0.85。

### 读图时要留意

- 这个指数只衡量行政是否规范，动员和执行的力度不在其中。
- 它和选举民主指数本身相关（约 0.74），所以"弱国家、强问责"那一角偏空，有一部分是指标造成的。
- 人均 GDP 数据到 2019 年为止，之后沿用 2019 年的值。
- "世界平均"是各国简单平均，每国一票，不按人口加权。
- 统计单元按 V-Dem 的划分，名称只表示数据集里的单元。

## 哪些来自书，哪些不是

- **来自书：** 两个维度的框架，各章和各讲的标题。
- **不是书中原文：** 每个国家的缘起、转折、结果，各章的看点，四个象限的名字。这些是根据公开史实和上面的数据写的概括。

## 仓库结构

```
index.html              构建好的页面，单文件，可以直接打开
src/page.html           页面源码，数据处留了一个占位标记
data/data.json          处理后的数据
scripts/build_data.py   从 V-Dem 原始数据生成 data/data.json
scripts/build_page.py   把数据填进页面，生成 index.html
```

页面是纯 HTML、CSS 和 JavaScript，没有依赖，也不发任何外部请求。

## 本地构建

只改页面：

```sh
python scripts/build_page.py
```

重新生成数据（需要 `pandas`、`numpy`、`pyreadr`，以及 [vdemdata](https://github.com/vdeminstitute/vdemdata) 里的 `data/vdem.RData`）：

```sh
python scripts/build_data.py path/to/vdem.RData
python scripts/build_page.py
```

## 许可

- **代码**（`src/`、`scripts/`、`index.html` 里的页面代码）：MIT，见 [LICENSE](LICENSE)。
- **数据**（`data/data.json` 以及内嵌在 `index.html` 里的同一份数据）：派生自 V-Dem 数据集，按 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 发布。

引用 V-Dem：

> Coppedge, Michael, John Gerring, Carl Henrik Knutsen, Staffan I. Lindberg, Jan Teorell, et al. 2026. "V-Dem [Country-Year/Country-Date] Dataset v16." Varieties of Democracy (V-Dem) Project.

## 致谢

- 刘瑜《可能性的艺术：比较政治学30讲》，广西师范大学出版社，2022。
- V-Dem Institute。
- 页面和数据处理由 Mia 与 AI（Claude）协作完成。
