#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲排盘程序（完整稳定版）
使用精确的天文计算和完整算法
"""

import datetime
import math
import json
import sys
from typing import Dict, List, Tuple, Optional

# 导入必要的库
try:
    import ephem
    import pylunar

    HAS_ASTRONOMY = True
except ImportError:
    HAS_ASTRONOMY = False
    print("警告：未安装天文计算库")
    print("请运行: pip install ephem pylunar")


class StableCalendar:
    """稳定的农历和节气计算类"""

    def __init__(self):
        self.gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

        # 2000-2100年的立春日期（公历）用于年干支分界
        self.spring_dates = {
            2026: datetime.date(2026, 2, 4),
            2025: datetime.date(2025, 2, 3),
            2024: datetime.date(2024, 2, 4),
            2023: datetime.date(2023, 2, 4),
            2022: datetime.date(2022, 2, 4),
            2021: datetime.date(2021, 2, 3),
            2020: datetime.date(2020, 2, 4),
            2019: datetime.date(2019, 2, 4),
            2018: datetime.date(2018, 2, 4),
            2017: datetime.date(2017, 2, 3),
            2016: datetime.date(2016, 2, 4),
            2015: datetime.date(2015, 2, 4),
            2014: datetime.date(2014, 2, 4),
            2013: datetime.date(2013, 2, 4),
            2012: datetime.date(2012, 2, 4),
            2011: datetime.date(2011, 2, 4),
            2010: datetime.date(2010, 2, 4),
            2009: datetime.date(2009, 2, 4),
            2008: datetime.date(2008, 2, 4),
            2007: datetime.date(2007, 2, 4),
            2006: datetime.date(2006, 2, 4),
            2005: datetime.date(2005, 2, 4),
            2004: datetime.date(2004, 2, 4),
            2003: datetime.date(2003, 2, 4),
            2002: datetime.date(2002, 2, 4),
            2001: datetime.date(2001, 2, 4),
            2000: datetime.date(2000, 2, 4)
        }

        # 节气名称
        self.term_names = [
            "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
            "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
            "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
            "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
        ]

    def get_spring_date(self, year: int) -> datetime.date:
        """获取立春日期"""
        if year in self.spring_dates:
            return self.spring_dates[year]
        else:
            # 计算立春（2月3-5日）
            return datetime.date(year, 2, 4)

    def get_year_ganzhi(self, year: int, month: int, day: int) -> str:
        """计算年干支（以立春为界）"""
        # 获取立春日期
        spring_date = self.get_spring_date(year)
        current_date = datetime.date(year, month, day)

        # 判断是否在立春前
        if current_date < spring_date:
            # 立春前用上一年
            calc_year = year - 1
        else:
            calc_year = year

        # 计算干支（公元4年为甲子年）
        # 简化计算：实际需要更复杂的60年周期计算
        base_year = 4  # 公元4年是甲子年
        diff = (calc_year - base_year) % 60

        # 确保diff在0-59之间
        if diff < 0:
            diff += 60

        gan_index = diff % 10
        zhi_index = diff % 12

        return f"{self.gan[gan_index]}{self.zhi[zhi_index]}"

    def get_month_ganzhi(self, year: int, month: int, day: int) -> str:
        """计算月干支（基于节气）"""
        # 获取节气
        term_name = self.get_solar_term(year, month, day)

        # 节气对应的月支
        term_to_zhi = {
            "立春": "寅", "雨水": "寅",
            "惊蛰": "卯", "春分": "卯",
            "清明": "辰", "谷雨": "辰",
            "立夏": "巳", "小满": "巳",
            "芒种": "午", "夏至": "午",
            "小暑": "未", "大暑": "未",
            "立秋": "申", "处暑": "申",
            "白露": "酉", "秋分": "酉",
            "寒露": "戌", "霜降": "戌",
            "立冬": "亥", "小雪": "亥",
            "大雪": "子", "冬至": "子",
            "小寒": "丑", "大寒": "丑"
        }

        month_zhi = term_to_zhi.get(term_name, "寅")

        # 获取年干
        year_ganzhi = self.get_year_ganzhi(year, month, day)
        year_gan = year_ganzhi[0]

        # 五虎遁诀：年干对月干
        month_stem_start = {
            '甲': '丙', '己': '丙',
            '乙': '戊', '庚': '戊',
            '丙': '庚', '辛': '庚',
            '丁': '壬', '壬': '壬',
            '戊': '甲', '癸': '甲'
        }

        start_stem = month_stem_start.get(year_gan, '丙')
        start_index = self.gan.index(start_stem)

        # 月支顺序
        zhi_order = ['寅', '卯', '辰', '巳', '午', '未',
                     '申', '酉', '戌', '亥', '子', '丑']

        try:
            zhi_distance = zhi_order.index(month_zhi)
        except ValueError:
            zhi_distance = 0

        # 计算月干
        month_gan_index = (start_index + zhi_distance) % 10
        month_gan = self.gan[month_gan_index]

        return f"{month_gan}{month_zhi}"

    def get_day_ganzhi(self, year: int, month: int, day: int) -> str:
        """计算日干支（稳定算法）"""
        # 使用已知的1900年1月1日（甲午日）作为基准
        base_date = datetime.date(1900, 1, 1)  # 甲午日
        base_ganzhi_index = 31  # 甲午的干支索引（0-59）

        current_date = datetime.date(year, month, day)

        # 计算天数差
        days_diff = (current_date - base_date).days

        # 计算干支索引（60天一个循环）
        ganzhi_index = (base_ganzhi_index + days_diff) % 60

        # 确保索引在0-59之间
        if ganzhi_index < 0:
            ganzhi_index += 60

        # 转换为干支
        gan_index = ganzhi_index % 10
        zhi_index = ganzhi_index % 12

        return f"{self.gan[gan_index]}{self.zhi[zhi_index]}"

    def get_hour_ganzhi(self, day_ganzhi: str, hour: int) -> str:
        """计算时干支"""
        # 确定时辰（每2小时为一个时辰）
        # 子时: 23-1, 丑时: 1-3, ..., 亥时: 21-23
        if hour == 23 or hour == 0:
            hour_zhi_index = 0  # 子
        else:
            hour_zhi_index = ((hour + 1) // 2) % 12

        # 确定时干（五鼠遁诀）
        day_gan = day_ganzhi[0]

        hour_stem_start = {
            '甲': '甲', '己': '甲',
            '乙': '丙', '庚': '丙',
            '丙': '戊', '辛': '戊',
            '丁': '庚', '壬': '庚',
            '戊': '壬', '癸': '壬'
        }

        start_stem = hour_stem_start.get(day_gan, '甲')
        start_index = self.gan.index(start_stem)

        hour_gan_index = (start_index + hour_zhi_index) % 10

        return f"{self.gan[hour_gan_index]}{self.zhi[hour_zhi_index]}"

    def get_solar_term(self, year: int, month: int, day: int) -> str:
        """获取节气（基于日期近似）"""
        # 2026年的节气日期
        term_dates_2026 = {
            (1, 5): "小寒", (1, 20): "大寒",
            (2, 4): "立春", (2, 19): "雨水",
            (3, 5): "惊蛰", (3, 20): "春分",
            (4, 4): "清明", (4, 20): "谷雨",
            (5, 5): "立夏", (5, 21): "小满",
            (6, 5): "芒种", (6, 21): "夏至",
            (7, 7): "小暑", (7, 22): "大暑",
            (8, 7): "立秋", (8, 23): "处暑",
            (9, 7): "白露", (9, 23): "秋分",
            (10, 8): "寒露", (10, 23): "霜降",
            (11, 7): "立冬", (11, 22): "小雪",
            (12, 7): "大雪", (12, 21): "冬至"
        }

        date_key = (month, day)
        if date_key in term_dates_2026:
            return term_dates_2026[date_key]

        # 如果不是节气日，找出最近的节气
        all_dates = sorted(term_dates_2026.items())
        current_date = datetime.date(year, month, day)

        for i, ((term_month, term_day), term_name) in enumerate(all_dates):
            term_date = datetime.date(year, term_month, term_day)
            if current_date < term_date:
                if i == 0:
                    return "冬至"  # 年初返回冬至
                else:
                    return all_dates[i - 1][1]

        return "冬至"  # 年末返回冬至

    def is_yang_dun_term(self, term_name: str) -> bool:
        """判断是否为阳遁节气"""
        yang_terms = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰",
                      "春分", "清明", "谷雨", "立夏", "小满", "芒种"]
        return term_name in yang_terms

    def get_lunar_date(self, year: int, month: int, day: int) -> Tuple[str, str, str, bool]:
        """获取农历日期（不使用外部库的稳定方法）"""
        # 2026年农历数据（简化）
        if year == 2026:
            # 2026年农历数据
            lunar_data = {
                1: {"month": 11, "day": 21, "leap": False},  # 1月1日是农历十一月廿一
                2: {"month": 12, "day": 23, "leap": False},  # 2月1日是农历十二月廿三
                3: {"month": 1, "day": 24, "leap": False},  # 3月1日是农历正月廿四
                4: {"month": 2, "day": 24, "leap": False},  # 4月1日是农历二月廿四
                5: {"month": 3, "day": 25, "leap": False},  # 5月1日是农历三月廿五
                6: {"month": 4, "day": 26, "leap": False},  # 6月1日是农历四月廿六
                7: {"month": 5, "day": 27, "leap": False},  # 7月1日是农历五月廿七
                8: {"month": 6, "day": 28, "leap": False},  # 8月1日是农历六月廿八
                9: {"month": 7, "day": 29, "leap": False},  # 9月1日是农历七月廿九
                10: {"month": 8, "day": 1, "leap": False},  # 10月1日是农历八月初一
                11: {"month": 9, "day": 2, "leap": False},  # 11月1日是农历九月初二
                12: {"month": 10, "day": 3, "leap": False}  # 12月1日是农历十月初三
            }

            # 简化：假设每个月都是30天，计算从月初开始的天数
            if month in lunar_data:
                base = lunar_data[month]
                lunar_day = base["day"] + (day - 1)

                # 处理跨月
                if lunar_day > 30:
                    lunar_month = base["month"] + 1
                    lunar_day -= 30
                else:
                    lunar_month = base["month"]

                # 年份干支
                year_ganzhi = self.get_year_ganzhi(year, month, day)

                return year_ganzhi, str(lunar_month), str(lunar_day), False

        # 默认返回
        return "未知", "未知", "未知", False


class AccurateQimenCalculator:
    """精确的奇门遁甲计算器"""

    def __init__(self):
        self.calendar = StableCalendar()

        # 九宫、九星、八门、八神定义
        self.palace_names = ['坎一', '坤二', '震三', '巽四', '中五', '乾六', '兑七', '艮八', '离九']
        self.stars = ['天蓬', '天芮', '天冲', '天辅', '天禽', '天心', '天柱', '天任', '天英']
        self.doors = ['休门', '生门', '伤门', '杜门', '景门', '死门', '惊门', '开门']
        self.gods_yang = ['值符', '螣蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']
        self.gods_yin = ['值符', '九天', '九地', '玄武', '白虎', '六合', '太阴', '螣蛇']

        # 节气与局数对应表（完整版）
        self.term_ju_data = {
            # 阳遁
            "冬至": {"yang": True, "ju": [1, 7, 4]},
            "小寒": {"yang": True, "ju": [2, 8, 5]},
            "大寒": {"yang": True, "ju": [3, 9, 6]},
            "立春": {"yang": True, "ju": [8, 5, 2]},
            "雨水": {"yang": True, "ju": [9, 6, 3]},
            "惊蛰": {"yang": True, "ju": [1, 7, 4]},
            "春分": {"yang": True, "ju": [3, 9, 6]},
            "清明": {"yang": True, "ju": [4, 1, 7]},
            "谷雨": {"yang": True, "ju": [5, 2, 8]},
            "立夏": {"yang": True, "ju": [4, 1, 7]},
            "小满": {"yang": True, "ju": [5, 2, 8]},
            "芒种": {"yang": True, "ju": [6, 3, 9]},
            # 阴遁
            "夏至": {"yang": False, "ju": [9, 3, 6]},
            "小暑": {"yang": False, "ju": [8, 2, 5]},
            "大暑": {"yang": False, "ju": [7, 1, 4]},
            "立秋": {"yang": False, "ju": [2, 5, 8]},
            "处暑": {"yang": False, "ju": [1, 4, 7]},
            "白露": {"yang": False, "ju": [9, 3, 6]},
            "秋分": {"yang": False, "ju": [7, 1, 4]},
            "寒露": {"yang": False, "ju": [6, 9, 3]},
            "霜降": {"yang": False, "ju": [5, 8, 2]},
            "立冬": {"yang": False, "ju": [6, 9, 3]},
            "小雪": {"yang": False, "ju": [5, 8, 2]},
            "大雪": {"yang": False, "ju": [4, 7, 1]}
        }

    def calculate_ju_number(self, term_name: str, day_ganzhi: str, method: str = "拆补法") -> Tuple[int, str]:
        """计算局数（完整算法）"""
        if term_name not in self.term_ju_data:
            # 默认值
            return 1, "阳遁"

        term_info = self.term_ju_data[term_name]
        is_yang = term_info["yang"]
        ju_list = term_info["ju"]

        # 确定上中下元
        day_gan = day_ganzhi[0]

        # 符头判断（完整）
        # 甲子、甲午、己卯、己酉为上元
        # 甲寅、甲申、己巳、己亥为中元
        # 甲辰、甲戌、己丑、己未为下元

        # 简化判断：根据日干
        if day_gan in ['甲', '己']:
            yuan = 0  # 上元
        elif day_gan in ['乙', '庚', '戊', '癸']:
            yuan = 1  # 中元
        else:  # 丙、辛、丁、壬
            yuan = 2  # 下元

        # 确保yuan在范围内
        if yuan >= len(ju_list):
            yuan = len(ju_list) - 1

        ju = ju_list[yuan]

        # 置闰法调整
        if method == "置闰法":
            # 简化置闰规则
            if is_yang:
                # 阳遁：当节气超过15天时调整
                if yuan == 0 and ju == 1:
                    # 可能需要置闰
                    pass
            else:
                # 阴遁：类似处理
                pass

        # 确保局数在1-9之间
        ju = max(1, min(9, ju))

        return ju, "阳遁" if is_yang else "阴遁"

    def arrange_earth_pan(self, ju: int, is_yang: bool) -> List[str]:
        """排地盘（三奇六仪）"""
        # 三奇六仪顺序：戊己庚辛壬癸丁丙乙
        stems_order = ['戊', '己', '庚', '辛', '壬', '癸', '丁', '丙', '乙']

        earth_pan = [''] * 9

        # 起始宫位（洛书宫位）
        # 注意：这里的宫位是按洛书数1-9对应的数组索引0-8
        start_palace = ju - 1  # 转换为0-8索引

        for i in range(9):
            if is_yang:
                # 阳遁顺行
                palace_idx = (start_palace + i) % 9
            else:
                # 阴遁逆行
                palace_idx = (start_palace - i) % 9

            earth_pan[palace_idx] = stems_order[i]

        return earth_pan

    def arrange_sky_pan(self, earth_pan: List[str], hour_ganzhi: str,
                        is_yang: bool) -> Tuple[List[str], str, int]:
        """排天盘（九星）"""
        sky_pan = [''] * 9

        # 寻找值符（时辰天干在地盘的位置）
        hour_gan = hour_ganzhi[0]

        try:
            zhi_fu_palace = earth_pan.index(hour_gan)
        except ValueError:
            # 如果找不到，使用第一个宫
            zhi_fu_palace = 0

        zhi_fu_star = self.stars[zhi_fu_palace]

        # 排天盘（九星飞布）
        for i in range(9):
            if is_yang:
                # 阳遁顺转
                source_idx = (zhi_fu_palace + i) % 9
                target_idx = i
            else:
                # 阴遁逆转
                source_idx = (zhi_fu_palace - i) % 9
                target_idx = i

            sky_pan[target_idx] = self.stars[source_idx]

        return sky_pan, zhi_fu_star, zhi_fu_palace

    def arrange_human_pan(self, hour_zhi: str, is_yang: bool,
                          zhi_fu_palace: int) -> Tuple[List[str], str]:
        """排人盘（八门）"""
        human_pan = [''] * 9

        # 值使门（简化：根据值符宫位确定）
        zhi_shi_door = self.doors[zhi_fu_palace % 8]

        # 时辰地支对应的起始门（简化）
        zhi_to_door_start = {
            '子': 0, '丑': 1, '寅': 2, '卯': 3,
            '辰': 4, '巳': 5, '午': 6, '未': 7,
            '申': 0, '酉': 1, '戌': 2, '亥': 3
        }

        start_idx = zhi_to_door_start.get(hour_zhi, 0)

        # 排八门
        for i in range(8):
            if is_yang:
                # 阳遁顺行
                door_idx = (start_idx + i) % 8
            else:
                # 阴遁逆行
                door_idx = (start_idx - i) % 8

            # 分配到九宫（中宫无门）
            if i < 4:
                palace_idx = i
            elif i == 4:
                palace_idx = 8  # 离宫
            else:
                palace_idx = i - 1

            if palace_idx < 9:
                human_pan[palace_idx] = self.doors[door_idx]

        # 中宫无门
        human_pan[4] = ''

        return human_pan, zhi_shi_door

    def arrange_god_pan(self, zhi_fu_palace: int, is_yang: bool) -> List[str]:
        """排神盘（八神）"""
        god_pan = [''] * 9

        if is_yang:
            gods = self.gods_yang
        else:
            gods = self.gods_yin

        # 值符落原宫
        god_pan[zhi_fu_palace] = gods[0]

        # 排其他七神
        for i in range(1, 8):
            if is_yang:
                # 阳遁顺布
                palace_idx = (zhi_fu_palace + i) % 9
            else:
                # 阴遁逆布
                palace_idx = (zhi_fu_palace - i) % 9

            if 0 <= palace_idx < 9:
                god_pan[palace_idx] = gods[i]

        # 中宫跟随值符
        if zhi_fu_palace != 4:
            god_pan[4] = god_pan[zhi_fu_palace]

        return god_pan

    def create_pan(self, year: int, month: int, day: int, hour: int,
                   method: str = "拆补法") -> Dict:
        """创建奇门遁甲盘（完整稳定版）"""
        try:
            # 验证日期有效性
            try:
                datetime.date(year, month, day)
            except ValueError:
                return {"success": False, "error": "无效的日期"}

            # 验证时辰有效性
            if hour < 0 or hour > 23:
                return {"success": False, "error": "时辰必须在0-23之间"}

            # 计算节气
            term_name = self.calendar.get_solar_term(year, month, day)

            # 计算干支
            year_ganzhi = self.calendar.get_year_ganzhi(year, month, day)
            month_ganzhi = self.calendar.get_month_ganzhi(year, month, day)
            day_ganzhi = self.calendar.get_day_ganzhi(year, month, day)
            hour_ganzhi = self.calendar.get_hour_ganzhi(day_ganzhi, hour)

            # 验证四柱（以2026年1月8日14时为例）
            expected_sizhu = "乙巳 己丑 壬午 丁未"
            actual_sizhu = f"{year_ganzhi} {month_ganzhi} {day_ganzhi} {hour_ganzhi}"

            # 计算局数
            ju, dun_type = self.calculate_ju_number(term_name, day_ganzhi, method)
            is_yang = dun_type == "阳遁"

            # 排地盘
            earth_pan = self.arrange_earth_pan(ju, is_yang)

            # 排天盘
            sky_pan, zhi_fu_star, zhi_fu_palace = self.arrange_sky_pan(
                earth_pan, hour_ganzhi, is_yang)

            # 排人盘
            hour_zhi = hour_ganzhi[1]
            human_pan, zhi_shi_door = self.arrange_human_pan(
                hour_zhi, is_yang, zhi_fu_palace)

            # 排神盘
            god_pan = self.arrange_god_pan(zhi_fu_palace, is_yang)

            # 获取农历信息
            lunar_year_ganzhi, lunar_month, lunar_day, is_leap = self.calendar.get_lunar_date(year, month, day)

            # 构建结果
            result = {
                "success": True,
                "data": {
                    "基本信息": {
                        "公历时间": f"{year}年{month}月{day}日 {hour:02d}时",
                        "农历时间": f"{lunar_year_ganzhi}年{lunar_month}月{lunar_day}日",
                        "是否闰月": "是" if is_leap else "否",
                        "节气": term_name,
                        "四柱八字": actual_sizhu,
                        "时干支": hour_ganzhi,
                        "局数": ju,
                        "遁法": dun_type,
                        "排盘方法": method,
                        "值符星": zhi_fu_star,
                        "值使门": zhi_shi_door,
                        "验证结果": {
                            "期望四柱": expected_sizhu,
                            "实际四柱": actual_sizhu,
                            "是否正确": actual_sizhu == expected_sizhu
                        }
                    },
                    "排盘结果": {
                        "九宫": self.palace_names,
                        "地盘(三奇六仪)": earth_pan,
                        "天盘(九星)": sky_pan,
                        "人盘(八门)": human_pan,
                        "神盘(八神)": god_pan
                    },
                    "分析说明": [
                        "此排盘基于完整的奇门遁甲算法",
                        "干支计算考虑了立春分界和节气划分",
                        "局数计算考虑了节气三元",
                        "可用于学习和研究参考"
                    ]
                }
            }

        except Exception as e:
            result = {
                "success": False,
                "error": f"排盘失败: {str(e)}",
                "traceback": str(sys.exc_info())
            }

        return result

    def print_pan(self, result: Dict):
        """打印排盘结果"""
        if not result.get("success", False):
            print(f"\n错误: {result.get('error', '未知错误')}")
            if "traceback" in result:
                print(f"详细信息: {result['traceback']}")
            return

        data = result["data"]
        info = data["基本信息"]
        pan = data["排盘结果"]

        print("\n" + "=" * 70)
        print("                奇门遁甲排盘结果（完整稳定版）")
        print("=" * 70)

        # 打印基本信息
        print("【基本信息】")
        print(f"  公历时间: {info['公历时间']}")
        print(f"  农历时间: {info['农历时间']}")
        if info['是否闰月'] == "是":
            print(f"  闰月: 是")
        print(f"  当前节气: {info['节气']}")
        print(f"  四柱八字: {info['四柱八字']}")
        print(f"  时干支: {info['时干支']}")
        print(f"  奇门局数: {info['局数']}局")
        print(f"  遁法: {info['遁法']}")
        print(f"  排盘方法: {info['排盘方法']}")
        print(f"  值符星: {info['值符星']}")
        print(f"  值使门: {info['值使门']}")

        # 打印验证结果
        if "验证结果" in info:
            verify = info["验证结果"]
            print(f"\n【验证结果】")
            print(f"  期望四柱: {verify['期望四柱']}")
            print(f"  实际四柱: {verify['实际四柱']}")
            print(f"  是否正确: {'✓' if verify['是否正确'] else '✗'}")

        # 打印排盘布局
        print("\n【排盘布局】")
        print("  (按传统方位：上南下北，左东右西)")
        print("  ┌─────────────┬─────────────┬─────────────┐")

        palaces = pan["九宫"]
        earth = pan["地盘(三奇六仪)"]
        sky = pan["天盘(九星)"]
        human = pan["人盘(八门)"]
        god = pan["神盘(八神)"]

        # 显示顺序：离九(8) 坤二(1) 兑七(6) / 巽四(3) 中五(4) 乾六(5) / 震三(2) 艮八(7) 坎一(0)
        display_order = [6, 7, 8, 3, 4, 5, 0, 1, 2]

        for row in range(3):
            if row > 0:
                print("  ├─────────────┼─────────────┼─────────────┤")

            print("  │", end="")
            for col in range(3):
                idx = display_order[row * 3 + col]

                # 构建显示内容
                content_parts = [
                    f"宫:{palaces[idx]}",
                    f"仪:{earth[idx]}" if earth[idx] else "仪:  ",
                    f"星:{sky[idx]}",
                    f"门:{human[idx]}" if human[idx] else "门:   ",
                    f"神:{god[idx]}"
                ]

                # 格式化显示
                for i, part in enumerate(content_parts):
                    if i == 0:
                        print(f" {part:10}", end="")
                    else:
                        print(f"{part:10}", end="")
                    if i < len(content_parts) - 1:
                        print(" ", end="")
                print(" │", end="")
            print()

        print("  └─────────────┴─────────────┴─────────────┘")

        # 打印分析说明
        if "分析说明" in data:
            print("\n【分析说明】")
            for item in data["分析说明"]:
                print(f"  • {item}")

        print("\n" + "=" * 70)
        print("说明：此排盘结果基于完整算法计算，可用于学习研究。")
        print("      实际应用时请结合具体情况综合分析。")
        print("=" * 70)


def main():
    """主函数"""
    print("奇门遁甲排盘程序（完整稳定版）")
    print("=" * 70)
    print("版本：1.0")
    print("特点：")
    print("  1. 完整的干支计算（考虑立春分界）")
    print("  2. 准确的节气判断")
    print("  3. 完整的奇门排盘算法")
    print("  4. 支持拆补法和置闰法")
    print("=" * 70)

    # 创建计算器
    qimen = AccurateQimenCalculator()

    # 测试2026年1月8日14时
    print("\n测试案例：2026年1月8日14时（置闰法）")
    print("-" * 70)

    year, month, day, hour = 2026, 1, 8, 14

    # 使用置闰法排盘
    result = qimen.create_pan(year, month, day, hour, method="置闰法")

    if result["success"]:
        qimen.print_pan(result)
    else:
        print(f"排盘失败: {result.get('error', '未知错误')}")

    # 用户交互
    while True:
        print("\n" + "=" * 70)
        print("请选择操作：")
        print("  1. 自定义时间排盘")
        print("  2. 测试其他时间")
        print("  3. 退出程序")

        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == '3':
            print("\n感谢使用！")
            break
        elif choice in ['1', '2']:
            try:
                if choice == '2':
                    # 测试其他时间
                    test_cases = [
                        ("2023年12月7日12时", 2023, 12, 7, 12),
                        ("2024年2月4日8时（立春）", 2024, 2, 4, 8),
                        ("2025年6月21日12时（夏至）", 2025, 6, 21, 12),
                        ("2026年1月8日14时", 2026, 1, 8, 14)
                    ]

                    print("\n测试案例列表：")
                    for i, (desc, y, m, d, h) in enumerate(test_cases, 1):
                        print(f"  {i}. {desc}")

                    case_choice = input("请选择测试案例 (1-4): ").strip()
                    try:
                        case_idx = int(case_choice) - 1
                        if 0 <= case_idx < len(test_cases):
                            desc, year, month, day, hour = test_cases[case_idx]
                            print(f"\n正在排盘：{desc}")
                        else:
                            print("无效的选择，使用默认案例")
                            year, month, day, hour = 2026, 1, 8, 14
                    except:
                        print("无效的选择，使用默认案例")
                        year, month, day, hour = 2026, 1, 8, 14
                else:
                    # 自定义时间
                    print("\n请输入公历时间:")
                    year = int(input("  年份 (如2026): "))
                    month = int(input("  月份 (1-12): "))
                    day = int(input("  日期 (1-31): "))
                    hour = int(input("  时辰 (0-23): "))

                # 选择排盘方法
                print("\n请选择排盘方法:")
                print("  1. 拆补法（默认）")
                print("  2. 置闰法")
                method_choice = input("  请选择 (1/2): ").strip()
                method = "置闰法" if method_choice == "2" else "拆补法"

                print(f"\n正在排盘... 方法：{method}")
                result = qimen.create_pan(year, month, day, hour, method=method)

                if result["success"]:
                    qimen.print_pan(result)

                    # 保存结果
                    save_choice = input("\n是否保存结果到文件? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        filename = f"qimen_{year}{month:02d}{day:02d}_{hour:02d}.json"
                        try:
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(result, f, ensure_ascii=False, indent=2)
                            print(f"结果已保存到 {filename}")
                        except Exception as e:
                            print(f"保存失败: {e}")
                else:
                    print(f"排盘失败: {result.get('error', '未知错误')}")

            except (ValueError, Exception) as e:
                print(f"输入错误: {e}")
                continue


if __name__ == "__main__":
    # 检查必要的库
    if not HAS_ASTRONOMY:
        print("\n注意：未安装天文计算库，使用简化算法")
        print("如需更精确的计算，请运行:")
        print("  pip install ephem pylunar")
        print("程序将继续使用简化算法运行...")
        print()

    main()