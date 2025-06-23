import re
from typing import Dict, List

class EmotionAnalyzer:
    def __init__(self):
        """初始化情緒分析器"""
        
        # 大幅擴展的情緒關鍵詞字典 - 支援更多音樂類型
        self.emotion_keywords = {
            "battle": [
                "衝", "攻擊", "戰鬥", "拔劍", "武器", "戰", "打", "殺", "刺", "砍",
                "向前", "衝鋒", "進攻", "反擊", "迎戰", "對抗", "抵抗", "戰士",
                "勇敢", "無畏", "挑戰", "格鬥", "廝殺", "血戰", "激戰", "迎擊",
                "fight", "attack", "battle", "combat", "strike", "sword", "weapon",
                "charge", "assault", "defend", "warrior", "brave", "courage"
            ],
            
            "tense_battle": [
                "激烈", "緊張", "危險", "白熱化", "生死", "拚命", "決死", "搏命",
                "千鈞一髮", "緊急", "關鍵", "重要", "決定性", "最後", "終極",
                "desperate", "intense", "critical", "crucial", "life or death",
                "final", "ultimate", "tension", "dangerous", "fierce"
            ],
            
            "heroic": [
                "獻出", "犧牲", "捨身", "以身殉", "為了", "守護", "保護", "英雄",
                "心臟", "生命", "付出", "奉獻", "義無反顧", "視死如歸", "慷慨",
                "壯烈", "悲壯", "崇高", "偉大", "光榮", "榮耀", "使命", "責任",
                "hero", "sacrifice", "dedicate", "protect", "guardian", "noble",
                "honor", "glory", "mission", "duty", "selfless", "brave heart"
            ],
            
            "advance": [
                "前進", "邁進", "推進", "突破", "穿越", "越過", "闖過", "衝破",
                "向前走", "往前", "不退縮", "繼續", "堅持", "持續", "前行",
                "advance", "progress", "move forward", "breakthrough", "push through",
                "continue", "persist", "march", "proceed", "onward"
            ],
            
            "charge": [
                "衝鋒", "突擊", "猛攻", "全力", "爆發", "衝刺", "突進", "猛衝",
                "一鼓作氣", "全速", "加速", "爆衝", "直衝", "猛撲", "撲向",
                "charge", "rush", "sprint", "dash", "burst", "surge", "storm",
                "blitz", "assault", "full speed", "all out", "rapid"
            ],
            
            "sad": [
                "逃跑", "害怕", "恐懼", "絕望", "無力", "退縮", "畏懼", "顫抖",
                "哭", "淚", "悲傷", "難過", "痛苦", "無助", "孤獨", "迷茫",
                "失望", "沮喪", "消極", "放棄", "認輸", "投降", "屈服", "逃離",
                "躲", "藏", "避", "退", "跑", "離開", "遠離", "憂鬱", "哀傷",
                "sad", "fear", "afraid", "despair", "hopeless", "cry", "tears",
                "escape", "run away", "hide", "retreat", "give up", "surrender"
            ],
            
            "wait_hide": [
                "等待", "藏", "躲藏", "隱藏", "等等", "暫停", "停下", "觀察",
                "小心", "謹慎", "潛伏", "蹲下", "趴下", "靜靜", "悄悄", "偷偷",
                "不動", "靜止", "屏住呼吸", "保持安靜", "隱蔽", "掩護",
                "wait", "hide", "hiding", "observe", "careful", "cautious",
                "stealth", "sneak", "quiet", "still", "lurk", "crouch", "duck"
            ],
            
            "retreat": [
                "撤退", "後退", "退後", "退縮", "逃跑", "逃走", "逃離", "躲避",
                "閃開", "迴避", "避開", "遠離", "離開", "撤離", "撤走", "退兵",
                "後撤", "戰略性撤退", "暫時撤退", "轉進", "退守", "退下",
                "retreat", "withdraw", "fall back", "pull back", "step back",
                "tactical retreat", "strategic withdrawal", "evacuate"
            ],
            
            "sacrifice": [
                "犧牲", "獻身", "捨命", "殉", "捨生", "以身", "奉獻生命", "殉職",
                "為國捐軀", "捨己", "自我犧牲", "犧牲自己", "付出生命", "獻出生命",
                "以死", "寧死", "情願死", "死也要", "拼死", "豁出去",
                "sacrifice", "martyrdom", "give life", "lay down life", "die for",
                "self-sacrifice", "ultimate sacrifice", "noble death"
            ],
            
            "victory": [
                "勝利", "成功", "贏", "戰勝", "打敗", "擊敗", "征服", "凱旋",
                "勝", "贏得", "成就", "完成", "達成", "實現", "克服", "超越",
                "triumph", "victory", "win", "succeed", "defeat", "conquer",
                "overcome", "achieve", "accomplish", "prevail", "champion"
            ],
            
            "defeat": [
                "失敗", "死", "死亡", "倒下", "敗", "輸", "完了", "結束",
                "不行", "沒用", "沒救", "完蛋", "毀滅", "覆滅", "滅亡", "慘敗",
                "defeat", "death", "die", "fail", "lose", "fallen", "destroyed",
                "doomed", "finished", "game over", "perish", "demise"
            ],
            
            "smile": [
                "笑", "微笑", "開心", "快樂", "高興", "愉快", "歡樂", "喜悅",
                "滿意", "得意", "輕鬆", "放鬆", "安心", "舒服", "愉悅", "欣慰",
                "幸福", "溫暖", "和諧", "平靜", "希望", "樂觀", "正面",
                "smile", "happy", "joy", "cheerful", "glad", "pleased", "content",
                "optimistic", "positive", "hopeful", "peaceful", "warm", "relief"
            ],
            
            "heroic_death": [
                "英勇犧牲", "壯烈犧牲", "英勇就義", "慷慨就義", "以身殉國", "以身殉職",
                "英雄末路", "壯烈成仁", "捨生取義", "為義而死", "光榮犧牲",
                "heroic death", "noble sacrifice", "glorious death", "martyrdom",
                "die with honor", "heroic end", "ultimate heroism"
            ],
            
            "peaceful": [
                "和平", "平靜", "安寧", "寧靜", "祥和", "溫和", "柔和", "安詳",
                "冷靜", "淡定", "從容", "平和", "協調", "和諧", "均衡", "穩定",
                "peaceful", "calm", "serene", "tranquil", "harmony", "balance",
                "gentle", "mild", "composed", "steady", "quiet", "still"
            ]
        }
        
        # 情緒權重 - 調整某些情緒的重要性
        self.emotion_weights = {
            "battle": 1.0,
            "tense_battle": 1.3,    # 緊張戰鬥權重高
            "heroic": 1.4,          # 英雄行為權重較高
            "advance": 1.1,         # 前進行為
            "charge": 1.4,          # 衝鋒權重高
            "sad": 1.1,             # 悲傷情緒權重提高
            "wait_hide": 1.3,       # 等待隱藏
            "retreat": 1.3,         # 撤退行為權重較高
            "sacrifice": 1.5,       # 犧牲權重最高
            "victory": 1.2,         # 勝利
            "defeat": 1.2,          # 失敗
            "smile": 1.1,           # 微笑/快樂
            "heroic_death": 1.5,    # 英勇犧牲權重最高
            "peaceful": 1.0         # 和平
        }
    
    def analyze_emotion(self, user_input: str) -> Dict[str, any]:
        """
        分析用戶輸入的情緒
        
        Args:
            user_input (str): 用戶輸入的文字
            
        Returns:
            Dict: 包含主要情緒、信心度和詳細分析
        """
        
        if not user_input.strip():
            return {
                "primary_emotion": "intro",
                "confidence": 0.0,
                "emotion_scores": {},
                "matched_keywords": {},
                "analysis": "輸入為空，使用預設情緒"
            }
        
        # 將輸入轉為小寫便於比對
        text_lower = user_input.lower()
        
        # 計算每種情緒的分數
        emotion_scores = {}
        matched_keywords = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            matches = []
            
            for keyword in keywords:
                # 使用正則表達式尋找關鍵詞
                if re.search(keyword, text_lower):
                    score += 1
                    matches.append(keyword)
            
            # 套用權重
            weighted_score = score * self.emotion_weights.get(emotion, 1.0)
            
            if weighted_score > 0:
                emotion_scores[emotion] = weighted_score
                matched_keywords[emotion] = matches
        
        # 找出得分最高的情緒
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[primary_emotion]
            
            # 特殊處理邏輯：
            # 1. 英勇犧牲優先於普通犧牲
            if "heroic_death" in emotion_scores and "sacrifice" in emotion_scores:
                if emotion_scores["heroic_death"] >= emotion_scores["sacrifice"] * 0.8:
                    primary_emotion = "heroic_death"
            
            # 2. 緊張戰鬥優先於普通戰鬥
            elif "tense_battle" in emotion_scores and "battle" in emotion_scores:
                if emotion_scores["tense_battle"] >= emotion_scores["battle"] * 0.8:
                    primary_emotion = "tense_battle"
            
            # 3. 衝鋒優先於前進
            elif "charge" in emotion_scores and "advance" in emotion_scores:
                if emotion_scores["charge"] >= emotion_scores["advance"] * 0.8:
                    primary_emotion = "charge"
            
            # 4. 逃跑相關情緒的優先處理
            escape_emotions = ["sad", "retreat", "wait_hide"]
            escape_total = sum(emotion_scores.get(emo, 0) for emo in escape_emotions)
            
            if escape_total > emotion_scores.get("battle", 0) and escape_total > emotion_scores.get("heroic", 0):
                # 在逃跑相關情緒中選擇最高分的
                escape_scores = {emo: emotion_scores.get(emo, 0) for emo in escape_emotions if emotion_scores.get(emo, 0) > 0}
                if escape_scores:
                    primary_emotion = max(escape_scores, key=escape_scores.get)
            
            # 計算信心度 (0-1之間)
            total_keywords = sum(len(keywords) for keywords in matched_keywords.values())
            confidence = min(max_score / 3.0, 1.0)  # 最多3個關鍵詞就達到100%信心
            
        else:
            # 沒有匹配到關鍵詞，使用預設情緒
            primary_emotion = "battle"  # 預設為戰鬥情緒
            confidence = 0.2  # 低信心度
            emotion_scores = {"battle": 0.2}
            matched_keywords = {}
        
        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "emotion_scores": emotion_scores,
            "matched_keywords": matched_keywords,
            "analysis": self._generate_analysis(primary_emotion, confidence, matched_keywords)
        }
    
    def _generate_analysis(self, emotion: str, confidence: float, matches: Dict) -> str:
        """生成情緒分析說明"""
        
        analysis_templates = {
            "battle": "檢測到戰鬥意圖，充滿戰鬥精神！ | Detected battle intent, full of fighting spirit!",
            "tense_battle": "檢測到激烈戰鬥情緒，情況緊張！ | Detected intense battle emotion, situation is tense!",
            "heroic": "檢測到英勇犧牲精神，令人敬佩的決心！ | Detected heroic sacrifice spirit, admirable determination!",
            "advance": "檢測到前進意志，勇往直前！ | Detected advancing will, moving forward bravely!",
            "charge": "檢測到衝鋒號令，全力攻擊！ | Detected charge command, full assault!",
            "sad": "檢測到悲傷情緒，內心充滿掙扎。 | Detected sadness, heart full of struggle.",
            "wait_hide": "檢測到等待隱藏策略，謹慎觀察中。 | Detected wait-and-hide strategy, observing cautiously.",
            "retreat": "檢測到撤退意圖，選擇戰略性後退。 | Detected retreat intention, choosing strategic withdrawal.",
            "sacrifice": "檢測到犧牲精神，準備為他人獻身。 | Detected sacrifice spirit, ready to give life for others.",
            "victory": "檢測到勝利的喜悅！ | Detected joy of victory!",
            "defeat": "檢測到失敗的沮喪情緒。 | Detected frustration of defeat.",
            "smile": "檢測到快樂正面情緒，心情愉悅！ | Detected happy positive emotion, joyful mood!",
            "heroic_death": "檢測到英勇就義精神，壯烈犧牲！ | Detected heroic martyrdom spirit, glorious sacrifice!",
            "peaceful": "檢測到平和寧靜情緒，內心安詳。 | Detected peaceful calm emotion, serene heart."
        }
        
        base_analysis = analysis_templates.get(emotion, f"檢測到{emotion}情緒 | Detected {emotion} emotion")
        
        confidence_desc = ""
        if confidence >= 0.8:
            confidence_desc = "非常確定 | Very certain"
        elif confidence >= 0.6:
            confidence_desc = "相當確定 | Quite certain"
        elif confidence >= 0.4:
            confidence_desc = "中等確定度 | Medium certainty"
        else:
            confidence_desc = "低確定度 | Low certainty"
        
        return f"{base_analysis} (信心度 | Confidence: {confidence_desc} {confidence:.1%})"