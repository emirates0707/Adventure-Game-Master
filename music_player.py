import pygame
import os
from typing import Dict, Optional

class MusicPlayer:
    def __init__(self, music_folder: str = "music"):
        """初始化音樂播放器"""
        pygame.mixer.init()
        self.music_folder = music_folder
        self.current_playing = None
        
        # 擴展的音樂情緒映射表 - 覆蓋所有音樂文件
        self.music_mapping = {
            # 開場
            "intro": "intro.mp3",
            
            # 戰鬥類音樂
            "battle": "battle_2.mp3", 
            "tense_battle": "tense_battle.mp3",  # 緊張激烈的戰鬥
            "fight": "tense_battle.mp3",
            "combat": "battle_2.mp3",
            
            # 英雄/前進類音樂
            "heroic": "advance.mp3",
            "advance": "advance.mp3",        # 前進行軍音樂
            "march": "advance.mp3",
            "progress": "advance.mp3",
            
            # 衝鋒類音樂
            "charge": "charge.mp3",          # 衝鋒號音樂
            "rush": "charge.mp3",
            "assault": "charge.mp3",
            "attack": "charge.mp3",
            
            # 悲傷/恐懼類音樂
            "sad": "sad.mp3",
            "fear": "sad.mp3",
            "despair": "sad.mp3",
            "cry": "sad.mp3",
            "sorrow": "sad.mp3",
            
            # 等待/隱藏類音樂
            "wait_hide": "wait_hide.mp3",    # 等待隱藏音樂
            "hide": "wait_hide.mp3",
            "stealth": "wait_hide.mp3",
            "observe": "wait_hide.mp3",
            "cautious": "wait_hide.mp3",
            "lurk": "wait_hide.mp3",
            
            # 撤退類音樂
            "retreat": "retreat.mp3",        # 撤退音樂
            "withdraw": "retreat.mp3",
            "escape": "retreat.mp3",
            "flee": "retreat.mp3",
            "run_away": "retreat.mp3",
            
            # 犧牲類音樂
            "sacrifice": "sacrifice.mp3",    # 普通犧牲
            "martyrdom": "sacrifice.mp3",
            "give_life": "sacrifice.mp3",
            
            # 英勇犧牲音樂
            "heroic_death": "heroic_death.mp3",  # 英勇就義
            "noble_death": "heroic_death.mp3",
            "glorious_death": "heroic_death.mp3",
            "heroic_sacrifice": "heroic_death.mp3",
            
            # 快樂/微笑類音樂
            "smile": "smile.mp3",            # 快樂/微笑音樂
            "happy": "smile.mp3",
            "joy": "smile.mp3",
            "cheerful": "smile.mp3",
            "relief": "smile.mp3",
            "hope": "smile.mp3",
            
            # 結局音樂
            "victory": "ending(victory).mp3", # 勝利結局
            "win": "ending(victory).mp3",
            "triumph": "ending(victory).mp3",
            "success": "ending(victory).mp3",
            
            "defeat": "ending(defeat).mp3",   # 失敗結局
            "lose": "ending(defeat).mp3",
            "death": "ending(defeat).mp3",
            "failure": "ending(defeat).mp3",
            "game_over": "ending(defeat).mp3",
            
            "peaceful": "ending(peaceful).mp3", # 和平結局
            "peace": "ending(peaceful).mp3",
            "calm": "ending(peaceful).mp3",
            "harmony": "ending(peaceful).mp3",
            "serene": "ending(peaceful).mp3"
        }
        
        # 音樂文件描述（用於debug和日誌）
        self.music_descriptions = {
            "intro.mp3": "開場音樂 | Opening Music",
            "battle_2.mp3": "普通戰鬥音樂 | Regular Battle Music",
            "tense_battle.mp3": "緊張激烈戰鬥音樂 | Intense Battle Music",
            "advance.mp3": "前進行軍音樂 | Advancing March Music",
            "charge.mp3": "衝鋒號音樂 | Charge Attack Music",
            "sad.mp3": "悲傷情緒音樂 | Sad Emotion Music",
            "wait_hide.mp3": "等待隱藏音樂 | Wait & Hide Music",
            "retreat.mp3": "撤退音樂 | Retreat Music",
            "sacrifice.mp3": "犧牲精神音樂 | Sacrifice Music",
            "heroic_death.mp3": "英勇就義音樂 | Heroic Death Music",
            "smile.mp3": "快樂微笑音樂 | Happy Smile Music",
            "ending(victory).mp3": "勝利結局音樂 | Victory Ending Music",
            "ending(defeat).mp3": "失敗結局音樂 | Defeat Ending Music",
            "ending(peaceful).mp3": "和平結局音樂 | Peaceful Ending Music"
        }
        
    def play_music(self, emotion_type: str) -> Dict[str, str]:
        """
        根據情緒類型播放對應音樂
        
        Args:
            emotion_type (str): 情緒類型
            
        Returns:
            Dict: 播放狀態和音樂文件信息
        """
        try:
            # 獲取對應的音樂文件
            music_file = self.music_mapping.get(emotion_type.lower())
            
            if not music_file:
                return {
                    "status": "error",
                    "message": f"找不到對應情緒 '{emotion_type}' 的音樂 | Cannot find music for emotion '{emotion_type}'",
                    "available_emotions": list(set(self.music_mapping.keys()))  # 去除重複
                }
            
            # 構建完整路徑
            music_path = os.path.join(self.music_folder, music_file)
            
            if not os.path.exists(music_path):
                return {
                    "status": "error",
                    "message": f"音樂文件不存在 | Music file not found: {music_path}"
                }
            
            # 停止當前播放的音樂
            pygame.mixer.music.stop()
            
            # 載入並播放新音樂
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # -1 表示循環播放
            
            self.current_playing = music_file
            
            # 獲取音樂描述
            description = self.music_descriptions.get(music_file, f"未知音樂 | Unknown music: {music_file}")
            
            return {
                "status": "success",
                "message": f"正在播放 | Now playing: {music_file}",
                "description": description,
                "emotion": emotion_type,
                "file": music_file
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"播放音樂時發生錯誤 | Error playing music: {str(e)}"
            }
    
    def stop_music(self) -> Dict[str, str]:
        """停止播放音樂"""
        try:
            pygame.mixer.music.stop()
            current_file = self.current_playing
            self.current_playing = None
            return {
                "status": "success",
                "message": f"音樂已停止 | Music stopped: {current_file if current_file else 'None'}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"停止音樂時發生錯誤 | Error stopping music: {str(e)}"
            }
    
    def get_current_playing(self) -> Optional[str]:
        """獲取當前播放的音樂"""
        return self.current_playing
    
    def get_current_description(self) -> Optional[str]:
        """獲取當前播放音樂的描述"""
        if self.current_playing:
            return self.music_descriptions.get(self.current_playing)
        return None
    
    def list_available_emotions(self) -> list:
        """列出所有可用的情緒類型"""
        return sorted(list(set(self.music_mapping.keys())))
    
    def list_available_music_files(self) -> dict:
        """列出所有可用的音樂文件及其描述"""
        return self.music_descriptions
    
    def get_emotion_music_mapping(self) -> dict:
        """獲取情緒到音樂的完整映射"""
        return self.music_mapping.copy()
        
    def validate_music_files(self) -> dict:
        """驗證所有音樂文件是否存在"""
        results = {
            "valid_files": [],
            "missing_files": [],
            "total_files": len(set(self.music_mapping.values()))
        }
        
        unique_files = set(self.music_mapping.values())
        
        for music_file in unique_files:
            music_path = os.path.join(self.music_folder, music_file)
            if os.path.exists(music_path):
                results["valid_files"].append(music_file)
            else:
                results["missing_files"].append(music_file)
        
        results["validation_status"] = "完全正常 | All files present" if not results["missing_files"] else f"缺少 {len(results['missing_files'])} 個文件 | Missing {len(results['missing_files'])} files"
        
        return results