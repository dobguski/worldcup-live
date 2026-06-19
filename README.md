# ⚽ DobGuski 世界杯小站 | FIFA World Cup 2026 Live Dashboard

> 🏆 48支球队 · 104场比赛 · 实时比分 · 积分榜 · 球员档案 · Polymarket预测

**🌐 Live Site:** [datamenu.xyz](https://datamenu.xyz) | [www.datamenu.xyz](https://www.datamenu.xyz)

![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-live-brightgreen)
![WC2026](https://img.shields.io/badge/World%20Cup-2026-gold)
![Teams](https://img.shields.io/badge/teams-48-blue)
![Matches](https://img.shields.io/badge/matches-104-orange)

---

## ✨ 功能亮点 / Features

| 模块 | 说明 |
|------|------|
| 📰 **最新战报** | 实时比分、自动刷新、比赛状态（进行中/已结束） |
| 📊 **积分榜** | 12组完整积分、净胜球、最佳第三标识 |
| 🔴 **直播** | 时间窗口智能检测、今日比赛一目了然 |
| 👥 **球队** | 48队完整档案、球员名单、双语中英文 |
| 🏆 **淘汰赛** | 晋级路线图 |
| 📈 **PM预测** | Polymarket市场预测 vs 实际结果对照 |
| 🌍 **时区适配** | 自动检测用户时区、北京时间参考 |

## 🛠 技术栈 / Tech Stack

- **前端:** 纯静态 HTML/CSS/JS（零框架依赖）
- **数据:** Football.TXT → JSON → GitHub Pages
- **同步:** Python 自动化脚本（ESPN + TheSportsDB + FIFA API）
- **部署:** GitHub Pages + 自定义域名
- **特性:** 双语 i18n、localStorage UV/PV、访客时区统计

## 📂 目录结构 / Structure

```
├── dashboard.html      # 主看板
├── welcome.html        # 欢迎页
├── stats.html          # 访问统计后台
├── sync_worldcup.py    # 数据同步引擎
├── match_data.json     # 比赛数据
├── standings.json      # 积分榜
├── teams.json          # 球队数据
├── polymarket.json     # 预测市场数据
├── counter.json        # 访客计数
├── visitors.json       # 访客日志
└── 2026--usa/cup.txt   # 原始赛程数据
```

## 🚀 快速开始 / Quick Start

```bash
# 启动同步服务器
python3 sync_worldcup.py --serve

# 持续监控模式（后台同步 + Web服务器）
python3 sync_worldcup.py --watch

# 单次同步
python3 sync_worldcup.py --once
```

访问 `http://localhost:8888/dashboard.html`

## 📊 数据源 / Data Sources

| 来源 | 类型 | 状态 |
|------|------|------|
| ESPN API | 实时比分 | ✅ 主力源 |
| TheSportsDB | 交叉验证 | ✅ 辅助 |
| FIFA API | 补充数据 | ✅ 三级源 |
| Polymarket | 预测市场 | ✅ 本地静态 |

## 🔗 相关链接 / Links

- 网站: [datamenu.xyz](https://datamenu.xyz)
- 数据源: [openfootball/worldcup](https://github.com/openfootball/worldcup)
- 2026世界杯: [FIFA Official](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026)

---

> 🇨🇦 Canada · 🇺🇸 United States · 🇲🇽 Mexico | TRIONDA Official Match Ball
> 
> Built with ❤️ by [DobGuski](https://github.com/dobguski)
