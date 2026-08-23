---
title: 医疗健康、健康中国与健身公共 API 索引
created: 2026-08-23
updated: 2026-08-23
source: https://github.com/public-apis/public-apis
status: verified-summary
tags:
  - API
  - 医疗健康
  - 健康中国
  - 健身
  - 公共卫生
  - 营养
---

# 医疗健康、健康中国与健身公共 API 索引

## 用途

从 `public-apis/public-apis` 中筛选医疗、公共卫生、营养、健身和环境健康相关 API，供后续选型、原型开发、数据分析和资料检索。

## 来源原意

- 主来源：[public-apis/public-apis](https://github.com/public-apis/public-apis)，社区手工整理的免费公共 API 索引。
- 相关分类：Health、Sports & Fitness、Food & Drink、Environment、Weather。
- 仓库的收录状态不等于 API 当前可用；关键项目还需查看官方文档、限额、许可和数据更新时间。

## 优先选型

| 场景 | 首选 | 备选 | 主要边界 |
|---|---|---|---|
| 药品、医疗器械、不良事件 | [openFDA](https://open.fda.gov/apis/) | [CMS.gov](https://data.cms.gov/provider-data/) | 主要是美国数据，不能直接替代中国药监数据 |
| 临床试验 | [Clinical Trials Directory](https://trials.starfile.org/api) | ClinicalTrials.gov 官方 API | 第三方索引应与官方源交叉核验 |
| 遗传学科普 | [MedlinePlus Genetics](https://medlineplus.gov/about/developers/geneticsdatafilesapi/) | — | 用于知识检索，不用于个体诊断 |
| 公共卫生与人道危机 | [Humanitarian Data Exchange](https://data.humdata.org/) | [Open Data NHS Scotland](https://www.opendata.nhs.scot/) | 数据地域、口径和时效性不同 |
| 食物成分与营养 | [USDA FoodData Central](https://fdc.nal.usda.gov/api-guide/) | [Open Food Facts](https://openfoodfacts.github.io/openfoodfacts-server/api/) | USDA 偏美国；Open Food Facts 是众包数据 |
| 跑步和训练活动 | [Strava API](https://developers.strava.com/docs/reference/) | [Tredict](https://www.tredict.com/blog/oauth_docs/) | 需用户 OAuth 授权；不是医疗级数据 |
| 健身动作与训练计划 | [wger](https://wger.de/en/software/api) | — | 动作内容仍需专业审核 |
| 可穿戴健康数据 | [Google Health API](https://developers.google.com/health) | [Fitbit Web API](https://dev.fitbit.com/build/reference/) | Fitbit 旧 Web API 计划于 2026-09 弃用，新项目应优先 Google Health |
| 症状评估与预分诊 | [Infermedica](https://developer.infermedica.com/documentation/overview/) | [ApiMedic](https://apimedic.com/) | 需商业授权与医疗合规，不能替代医生诊断 |
| 空气质量与环境健康 | [AQICN](https://aqicn.org/api/) | [OpenAQ](https://docs.openaq.org/)、[IQAir](https://www.iqair.com/air-pollution-data-api) | 中国城市覆盖和底层数据源需逐城市核验 |
| 中国户外运动环境 | [彩云天气](https://open.caiyunapp.com/ColorfulClouds_Weather_API) | AQICN | 更适合训练时间、高温和降水风险，不是医疗 API |

## 医疗与公共卫生备选

- [LAPIS](https://cov-spectrum.ethz.ch/public)：SARS-CoV-2 公开基因组序列。
- [Lexigram](https://docs.lexigram.io/)：从医疗文本抽取临床概念并映射术语体系；开发前需再测可用性。
- [NPPES](https://npiregistry.cms.hhs.gov/registry/help-api)：美国医疗机构和从业者注册信息。
- [ERstat](https://erstat.ca/developers)：加拿大急诊服务中断数据。
- [Orion Health](https://developer.orionhealth.io/)：企业级医疗平台整合，不适合轻量原型。
- [Longevity World Cup](https://longevityworldcup.com/api/data/athletes)：生物年龄、生物标志物和排名；仅适合演示或探索性分析。

## 营养与饮食备选

- [Nutritionix](https://developer.nutritionix.com/)：食物、餐馆菜品、热量和营养数据。
- [Edamam Nutrition](https://developer.edamam.com/edamam-docs-nutrition-api)：从食谱或食材计算营养成分。
- [Food Info](https://food-info.org/developer)：多个国家食品成分数据集。
- [Spoonacular](https://spoonacular.com/food-api)：食谱、食材、营养和膳食计划。
- [Chomp](https://chompthis.com/api/)：包装食品和零售商品数据。
- [RecipeAPI](https://recipeapi.io)：食谱、原料、营养和烹饪步骤。
- [Zestful](https://zestfuldata.com/)：将自然语言食材描述解析为结构化数据。

## 健身与运动备选

- [Tredict](https://www.tredict.com/blog/oauth_docs/)：读写耐力运动活动和健康数据。
- [Sport List & Data](https://developers.decathlon.com/products/sports)：运动项目分类和相关资源。
- [Sport Places](https://developers.decathlon.com/products/sport-places)：全球运动场所数据。
- [City Bikes](https://api.citybik.es/v2/)：全球共享单车站点，可用于城市身体活动研究。

## 中国适用性

该仓库未收录可直接支撑“健康中国”权威数据平台的国家卫健委、国家疾控局、国家医保局、国家药监局或《中国食物成分表》官方 API。

可用于中国场景的主要是：

1. AQICN、OpenAQ、IQAir 的部分中国城市空气质量数据。
2. 彩云天气的户外训练环境数据。
3. Open Food Facts 中的部分中国商品众包数据。
4. Infermedica 的简体中文配置，但需商业授权和本地医疗合规审查。

这些都不能替代中国官方公共卫生、药监、医保和食物成分数据。

## 限额与状态核验

- [FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/)：免费 API Key；默认每 IP 每小时 1000 次；数据为公共领域。
- [Open Food Facts API](https://openfoodfacts.github.io/openfoodfacts-server/api/)：v3 是新项目推荐版；读取商品不需认证；商品查询 15 次/分钟/IP，搜索 10 次/分钟/IP。
- [openFDA Authentication](https://open.fda.gov/apis/authentication/)：无密钥时每 IP 每分钟 240 次、每日 1000 次；免费密钥可提高至每日 120000 次。
- [Strava API](https://developers.strava.com/docs/reference/)：OAuth 2.0；数据访问范围取决于用户授权和应用审核。
- [Fitbit API Reference](https://dev.fitbit.com/build/reference/)：旧 Fitbit Web API 计划于 2026 年 9 月弃用，应迁移到 Google Health API。
- [Infermedica FAQ](https://developer.infermedica.com/documentation/overview/faq/)：试用通常为 2000 次 API 调用；商业公开使用需升级计划。

## 失效风险

- 仓库中十余个 COVID-19 API 多为疫情早期项目，仅适合历史研究且必须检查更新时间。
- [M-Media COVID-19 API](https://github.com/M-Media-Group/Covid-19-API) 已于 2022-10-31 弃用，仓库已归档。
- `PM25.in` 的仓库链接仅支持 HTTP，接入前必须重新确认申请通道、TLS 和数据更新状态。
- 任何医疗 API 均需单独检查数据许可、用户同意、隐私、数据跨境、临床声明及当地法规。

## 关联推断

- **可实践·考研**：与 [[长期目标#2026 上海体育大学运动康复专业考研]] 中的运动处方、运动与体重控制、运动机能评定有补充关系；可用于数据应用案例，不作为考纲知识本身。
- **可实践·HYROX**：Strava、Google Health 和可穿戴数据可支持 [[长期目标#HYROX 男子 Open 年龄组领奖台]] 的跑步配速、心率、训练量与恢复趋势分析。
- **补充·健康中国**：环境健康和公共卫生 API 可作为 [[运动康复政策与行业发展]] 的数据工具补充，但缺少中国官方数据时不能推导或代表健康中国官方结论。

## 后续使用检查表

1. 先确定任务是临床、科研、公共卫生、营养还是训练分析。
2. 查看官方文档的最后更新日期、API 版本、限额和认证方式。
3. 检查地域覆盖、数据来源和许可是否适用于中国。
4. 涉及个人健康数据时，先确认用户授权、最小必要范围和数据保留规则。
5. 不把众包、第三方聚合或研究数据当作临床诊断依据。

