# Week 3

本周作业用到的脚本和示例 CSV 放在这个目录里。主要脚本是 `week3_analysis_buggy.py`，数据文件是 `week3_survey_messy.csv`；另外还有清理 `responses.csv` 的 `clean_responses.py` 和统计角色的 `count_roles.py`。

运行示例：

```bash
python3 week3_analysis_buggy.py
```

---

## Competency claim（能力说明）

**C3 — Data cleaning and file handling**

我用 Python 从 CSV 读入真实数据（不是写在代码里的假数据）。数据里有缺字段的行、非数字的年限等情况：我根据报错信息定位到 `experience_years` 里出现了英文单词而不是整数，用 `try/except` 跳过无法转换的行，并在输出里说明跳过了哪几条。对既没有名字也没有角色的匿名行做了过滤，再统计角色和满意度。这样脚本在脏数据上也能稳定跑完，并给出可重复的输出。
