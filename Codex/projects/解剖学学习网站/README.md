# 解剖学背诵资料

## 目标

建设一个面向 2026 年上海体育大学运动康复考研的人体解剖学背诵资料库，用于全身骨骼肌肉按部位分类、快速背诵、动作反查和考点复现。

## 已确认方向

- 第一版选择“三个都要，但先做最小可用版”：考研学习、2D/3D 可视化、训练动作分析。
- 覆盖范围：全身骨骼肌肉。
- 细分程度：考研标准版，包含骨骼细分、肌肉起止点、功能、神经支配和易考点。
- 视觉主体：2D 为主，预留 3D 区域。
- 内容来源：以 Neumann《骨骼肌肉功能解剖学》第 2 版为主来源；网站内容应结构化整理，不直接长篇搬运原文。
- 2026-07-11 方向收束：短期目标从“资料库/交互系统”调整为“考研解剖主动回忆背诵器”，优先提升背诵速度和复现率。
- 2026-07-11 用户决定不要网站，改为按部位分类的 Markdown 背诵文档；保留已有网站代码作为历史产物，不再作为当前优先方向。

## 当前产物

- 设计文档：`/Users/HaoQi/Documents/Codex/2026-06-28/new-chat/docs/superpowers/specs/2026-07-03-anatomy-learning-site-design.md`
- 实施计划：`/Users/HaoQi/Documents/Codex/2026-06-28/new-chat/docs/superpowers/plans/2026-07-03-anatomy-learning-site.md`
- Task 1 脚手架已完成并提交。
- Task 2 数据基础已完成并提交：`85bd5f1 feat: add anatomy data foundation`。
  - 新增 anatomy 类型、9 个身体区域、肩复合体种子结构、动作、关系和数据引用校验。
  - 已验证：`npm test -- src/data/validation.test.ts`、`npm test`、`npm run build`。
- Task 2 质量修复已完成并提交：`aed65e6 test: harden anatomy data validation`。
  - 补强重复 ID、结构引用类型、动作引用类型和关系端点形状校验。
  - 已验证：`npm test -- src/data/validation.test.ts`、`npm test`、`npm run build`。
- Task 2 re-review 修复已完成并提交：`34a1a57 test: enforce anatomy relation consistency`。
  - 补强 relation triple 去重、可选 relation id 去重，以及 primeMover/synergist/antagonist 与目标 action 数组的一致性校验。
  - 已验证：`npm test -- src/data/validation.test.ts`、`npm test`、`npm run build`。
- Task 3 数据选择器已完成并提交：`d145912 feat: add anatomy selectors`。
  - 新增 ID 查找、按区域/模式筛选和中英文搜索。
  - 已验证：`npm test -- src/data/selectors.test.ts`、`npm test`、`npm run build`。
- Task 4 学习工作台 UI 已完成并提交：`c513098 feat: build anatomy study workspace`。
  - 新增全身分区、骨骼/肌肉/动作模式切换、搜索、详情面板和 3D 预览占位。
  - 已验证：`npm test -- src/App.test.tsx`、`npm test`、`npm run build`。
- Task 5 最终验证已完成。
  - `npm test`：15 个测试通过。
  - `npm run build`：通过。
  - 浏览器烟测：桌面三列布局、移动一列布局、搜索三角肌、详情显示腋神经、模式切换均通过。
- 下一阶段肩复合体扩充已完成。
  - 扩充 Neumann 第 2 版第 5 章肩复合体结构：肩胛骨、锁骨、肱骨、胸骨、关节盂、喙突、肩峰、大/小结节、三角肌粗隆、结节间沟，胸锁/肩锁/肩胛胸壁/盂肱关节。
  - 扩充肩袖、三角肌、前锯肌、斜方肌上中下束、胸大肌、背阔肌、大圆肌、喙肱肌、肱二头肌长头等肌肉；补起止点、神经支配、功能、考点提示。
  - 扩充肩屈伸、外展内收、内外旋、肩胛上提下降、前伸后缩、上/下回旋动作反查，并在详情页显示主动肌、协同肌、拮抗肌和来源页码。
  - 已验证：`npm test` 21 个测试通过，`npm run build` 通过，浏览器烟测肩外展详情与来源字段通过。
- 下一阶段髋关节扩充已完成。
  - 扩充 Neumann 第 2 版第 12 章髋关节结构：髋骨、股骨、髋臼、髂前上棘、髂嵴、坐骨结节、股骨头、股骨颈、大/小转子和髋关节。
  - 扩充臀大肌、臀中肌、臀小肌、髂腰肌、阔筋膜张肌、长收肌、大收肌、梨状肌、股方肌和腘绳肌近端；补起止点、神经支配、功能、考点提示。
  - 扩充髋屈伸、外展内收、内外旋动作反查；来源页码校验覆盖肩复合体和髋区。
  - 已验证：`npm test` 26 个测试通过，`npm run build` 通过，浏览器烟测髋屈详情与来源字段通过。
- 下一阶段膝关节扩充已完成。
  - 扩充 Neumann 第 2 版第 13 章膝关节结构：髌骨、胫骨、腓骨、股骨远端、股骨髁、胫骨平台、胫骨粗隆、胫股关节、髌股关节。
  - 扩充内/外侧半月板、前/后交叉韧带、内/外侧副韧带，并以 landmark 类型记录为膝关节稳定结构。
  - 扩充股四头肌、股直肌、股内侧肌、股外侧肌、腘绳肌远端、腓肠肌和腘肌；补起止点、神经支配、功能、考点提示。
  - 扩充膝伸、膝屈、胫骨内/外旋、髌骨上/下滑动作反查；来源页码校验覆盖肩复合体、髋区和膝区。
  - 已验证：`npm test` 31 个测试通过，`npm run build` 通过，浏览器烟测膝伸详情与来源字段通过。
- 下一阶段踝足扩充已完成。
  - 扩充 Neumann 第 2 版第 14 章踝足结构：胫骨远端、腓骨远端、距骨、跟骨、舟骨、骰骨、跖骨、内/外侧纵弓和横弓。
  - 扩充距小腿关节、距下关节、横跗关节，以及胫骨前肌、趾长伸肌、腓肠肌-比目鱼肌复合体、胫骨后肌、腓骨长/短肌、拇长屈肌和足内在肌。
  - 扩充踝背屈/跖屈、足内翻/外翻、足旋前/旋后、足趾屈/伸动作反查；来源页码校验覆盖肩复合体、髋、膝和踝足。
  - 已验证：`npm test` 36 个测试通过，`npm run build` 通过，浏览器烟测踝背屈详情与来源字段通过。
- 背诵器改造已完成。
  - 新增从现有肌肉和动作数据自动生成的单点回忆卡：肌肉起点、止点、神经支配、功能，以及动作主动肌、协同肌、拮抗肌。
  - 首页改为“今日背诵”优先，支持显示答案、标记不会/模糊/会，并将掌握度保存到浏览器本地。
  - 原有部位浏览、搜索和详情页保留为辅助查阅。
  - 已验证：`npm test` 39 个测试通过，`npm run build` 通过，浏览器烟测显示答案与评分统计通过。
- PDF 背诵文档第一版已完成。
  - 已抽取 Neumann 第 2 版中文 PDF 全书 720 页 OCR 文本，并按目录切分章节语料。
  - 新增 Markdown 文档目录：`/Users/HaoQi/Documents/Codex/2026-06-28/new-chat/docs/anatomy-memorization/`。
  - 当前覆盖：总纲、肩复合体、肘与前臂、腕与手、中轴骨骼、髋、膝、踝足、步态与动作分析。
  - 文档采用统一格式：骨与骨性标志、关节与韧带、肌肉起止点/神经/功能、动作反查、易考点、背诵卡片。
- PDF 背诵文档已移动到 Obsidian 知识库。
  - 知识库入口：`/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/projects/解剖学背诵资料/README.md`
  - 知识点目录：`/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/projects/解剖学背诵资料/知识点/`
  - 当前包含 11 个 Markdown 文件：总纲、8 个部位/动作文档、肌肉速查表、考研问答模板。
	
## 下一步

下一阶段优先继续细化 Markdown 背诵文档：把各部位肌肉表扩充到更完整的起点、止点、神经支配和功能，并补“考研问答题模板”；网站开发暂停。
