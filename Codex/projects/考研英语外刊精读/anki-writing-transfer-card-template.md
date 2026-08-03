# 外刊精读 Anki 作文复用卡模板

## 定位

作文复用卡不同于普通词汇卡。普通词汇卡训练“看懂、辨义、翻译”；作文复用卡训练“能不能把外刊表达改写进考研英语作文”。

## 收录标准

只给真正能写进作文的表达制作文卡。表达必须至少满足一项功能：

- 定义问题
- 强调重要性
- 解释原因
- 说明后果
- 表达转折 / 让步
- 提出建议
- 平衡效率与安全 / 公平
- 总结社会价值

优先适配主题：

教育、文化、经济、科技、健康、环境、道德文明、精神品质、职场生活、社会责任。

## Basic 卡字段

```text
Front | Back | Extra | Tags
```

`Tags` 永远只写：

```text
外刊精读
```

## 字段模板

### Front

```text
用 "[target expression]" 写一句[topic]作文句：如何表达“[Chinese idea]”？
```

### Back

```text
<b>原文句</b>：[full article sentence containing target expression]
译：[Chinese translation]
<b>表达功能</b>：[problem definition / cause / consequence / contrast / recommendation / value judgement]
<b>可复用句型</b>：[sentence pattern with slots, preserving the target expression]
<b>考研作文成句</b>：[complete kaoyan writing sentence using the target expression]
译：[Chinese translation]
```

### Extra

```text
<b>适配话题</b>：[topic list]
<b>替换槽位</b>：A = ...; B = ...; C = ...
<b>多场景改写</b>：
1. [complete English sentence]. 译：[Chinese translation]
2. [complete English sentence]. 译：[Chinese translation]
3. [complete English sentence]. 译：[Chinese translation]
<b>常见错误</b>：[grammar, collocation, register, or Chinglish warning]
<b>记忆抓手</b>：[short cue]
```

## 示例

### Front

```text
用 "pose an awkward question" 写一句科技监管类作文句：如何表达“人工智能给监管者提出了一个棘手问题”？
```

### Back

```text
<b>原文句</b>：Digital innovations pose an awkward question to those in charge of the arrangement: how to make the system more efficient without making it any less safe?
译：数字创新向负责这套安排的人提出了一个棘手问题：怎样让体系更高效，同时又不让它变得更不安全？
<b>表达功能</b>：定义问题；引出“效率与安全”的平衡。
<b>可复用句型</b>：A poses an awkward question to B: how to do X without doing Y.
<b>考研作文成句</b>：Artificial intelligence poses an awkward question to policymakers: how to improve social efficiency without weakening public accountability.
译：人工智能给政策制定者提出了一个棘手问题：如何在提高社会效率的同时，不削弱公共问责。
```

### Extra

```text
<b>适配话题</b>：科技监管、教育科技、社会责任、公共治理。
<b>替换槽位</b>：A = artificial intelligence / online education / digital platforms; B = policymakers / schools / companies; X = improve efficiency / expand access; Y = weakening fairness / harming privacy / reducing safety.
<b>多场景改写</b>：
1. Online education poses an awkward question to schools: how to expand access without lowering teaching quality. 译：在线教育给学校提出了一个棘手问题：如何在扩大教育机会的同时，不降低教学质量。
2. Digital platforms pose an awkward question to society: how to encourage innovation without sacrificing privacy. 译：数字平台给社会提出了一个棘手问题：如何在鼓励创新的同时，不牺牲隐私。
3. Fast economic growth poses an awkward question to governments: how to create wealth without damaging the environment. 译：快速经济增长给政府提出了一个棘手问题：如何在创造财富的同时，不破坏环境。
<b>常见错误</b>：`pose a question to sb`，不要写成 `pose sb a question`；后面常接 `how to...without...`。
<b>记忆抓手</b>：pose = put forward；awkward = hard to handle。
```

## 质量检查

- 目标表达必须出现在 `Front` 和 `Back` 的作文成句中。
- 原文句必须是完整句，不能只放词组。
- 多场景例句必须是真实作文语境，不能写“学生可以使用这个词”这类元话语。
- 如果表达太窄、太技术化、只能在原文语境里用，就不做作文复用卡。

