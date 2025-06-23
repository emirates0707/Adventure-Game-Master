class GameState:
    def __init__(self):
        self.current_turn = 0
        self.max_turns = 3
        self.story_history = []
        self.user_actions = []
        self.emotion_history = []  # 新增：追蹤情緒歷史
        self.current_emotion = "intro"
        
    def add_story(self, story: str):
        """添加故事內容到歷史記錄"""
        self.story_history.append(story)
        
    def add_user_action(self, action: str):
        """添加用戶行動到記錄"""
        self.user_actions.append(action)
        
    def add_emotion(self, emotion: str):
        """添加情緒到歷史記錄"""
        self.emotion_history.append(emotion)
        self.current_emotion = emotion
        
    def get_previous_emotion(self):
        """獲取前一個情緒"""
        if len(self.emotion_history) > 0:
            return self.emotion_history[-1]
        return "intro"
        
    def next_turn(self):
        """進入下一回合"""
        self.current_turn += 1
        
    def is_game_over(self):
        """檢查遊戲是否結束"""
        return self.current_turn >= self.max_turns
        
    def get_context(self):
        """獲取遊戲上下文，用於AI生成故事"""
        return {
            "turn": self.current_turn,
            "story_history": self.story_history,
            "user_actions": self.user_actions,
            "emotion_history": self.emotion_history,
            "current_emotion": self.current_emotion
        }