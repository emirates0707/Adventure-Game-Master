from google.adk.agents import Agent
from game_state import GameState
from music_player import MusicPlayer
from emotion_analyzer import EmotionAnalyzer
import json

# 全域變數
game_state = GameState()
music_player = MusicPlayer()
emotion_analyzer = EmotionAnalyzer()

def start_game() -> dict:
    """開始遊戲，播放開場音樂並提供背景故事"""
    global game_state, music_player
    
    # 重置遊戲狀態
    game_state = GameState()
    
    # 播放開場音樂
    music_result = music_player.play_music("intro")
    
    # 開場故事 - 中英文雙語版本
    opening_story = """
🏰 === 文字冒險遊戲 | Text Adventure Game ===

💥 巨人攻破了一直保護人類的城牆！| Giants have broken through the walls that protected humanity!
🔥 城市在燃燒，人們在哭泣... | The city is burning, people are crying...
⚔️  你是保護人類最後的希望！| You are humanity's last hope!

現在你要怎麼做？| What will you do now?

（請描述你的行動，遊戲將根據你的情緒選擇對應的背景音樂）
(Please describe your action. The game will choose appropriate background music based on your emotion)
    """
    
    game_state.add_story(opening_story)
    
    return {
        "status": "success",
        "message": opening_story,
        "music_status": music_result,
        "turn": game_state.current_turn,
        "max_turns": game_state.max_turns
    }

def process_user_action(user_action: str) -> dict:
    """處理用戶行動，分析情緒，播放音樂，生成故事"""
    global game_state, music_player, emotion_analyzer
    
    if game_state.is_game_over():
        return {
            "status": "error",
            "message": "遊戲已結束！請使用 start_game() 開始新遊戲。| Game is over! Please use start_game() to start a new game."
        }
    
    # 記錄用戶行動
    game_state.add_user_action(user_action)
    
    # 分析用戶情緒
    emotion_result = emotion_analyzer.analyze_emotion(user_action)
    primary_emotion = emotion_result["primary_emotion"]
    
    # 播放對應音樂
    music_result = music_player.play_music(primary_emotion)
    
    # 進入下一回合
    game_state.next_turn()
    
    # 根據回合數和用戶行動生成故事
    story_response = generate_story_response(user_action, emotion_result)
    game_state.add_story(story_response)
    
    return {
        "status": "success",
        "story": story_response,
        "emotion_analysis": emotion_result,
        "music_status": music_result,
        "turn": game_state.current_turn,
        "max_turns": game_state.max_turns,
        "game_over": game_state.is_game_over()
    }

def generate_story_response(user_action: str, emotion_result: dict) -> str:
    """根據用戶行動和情緒生成故事回應 - 中英文雙語版本"""
    global game_state
    
    turn = game_state.current_turn
    emotion = emotion_result["primary_emotion"]
    
    # 巨人攻城固定劇本的分支故事 - 完全按照用戶行動走
    if turn == 1:
        if emotion in ["battle", "tense_battle", "heroic", "charge", "advance"]:
            return f"""

⚔️  你握緊武器，眼中燃燒著決心的火焰！| You grip your weapon tightly, determination burning in your eyes!
💨 你衝向巨大的敵人，戰吼聲響徹雲霄！| You charge toward the giant enemy, your battle cry echoing through the sky!
🔥 巨人注意到了你的挑戰，轉身面對著你... | The giant notices your challenge and turns to face you...
👹 它的眼中閃爍著憤怒的紅光，巨大的拳頭朝你砸來！| Its eyes flash with angry red light, and its massive fist comes crashing toward you!


現在情況變得更加危險了！你要如何應對？
The situation has become even more dangerous! How will you respond?
            """
        elif emotion in ["sad", "retreat", "wait_hide"]:
            return f"""

😰 面對巨大的威脅，你感到恐懼和無助... | Facing the enormous threat, you feel fear and helplessness...
💔 你的內心充滿掙扎，腳步開始遲疑... | Your heart is full of struggle, your steps begin to hesitate...
🏃‍♂️ 你想要退縮，但身後傳來孩子們絕望的哭聲... | You want to retreat, but desperate cries of children echo behind you...
👶 一個小女孩拉住了你的衣角：「大哥哥，不要拋下我們...」| A little girl grabs your sleeve: "Big brother, don't abandon us..."
😢 你的內心充滿愧疚和痛苦... | Your heart fills with guilt and pain...


你的良心在折磨著你，你會繼續這樣做還是改變主意？
Your conscience is tormenting you. Will you continue or change your mind?
            """
        elif emotion in ["sacrifice", "heroic_death"]:
            return f"""

✨ 你意識到了自己的使命，準備為他人犧牲... | You realize your mission and prepare to sacrifice for others...
💫 一股神聖的力量在你身上湧現... | A sacred energy surges within you...
⚔️  你決定用自己的生命來保護無辜的人們！| You decide to use your life to protect innocent people!
🌟 你的勇氣感染了周圍的人，他們看到了希望... | Your courage inspires those around you, they see hope...


你準備做出最大的犧牲，這將如何改變一切？
You're prepared to make the ultimate sacrifice. How will this change everything?
            """
        elif emotion in ["smile", "peaceful"]:
            return f"""
🎵 背景音樂：溫柔的希望之歌... | Background Music: Gentle song of hope...

😌 即使在這危機時刻，你保持著內心的平靜... | Even in this moment of crisis, you maintain inner peace...
🌅 你的微笑給絕望的人們帶來了一絲溫暖... | Your smile brings a touch of warmth to desperate people...
✨ 你的正面態度開始影響周圍的人... | Your positive attitude begins to influence those around you...
💝 人們在你身上看到了不同的力量... | People see a different kind of strength in you...


你的樂觀精神會如何影響這場危機？
How will your optimistic spirit affect this crisis?
            """
        else:
            return f"""

🤔 你站在廢墟中，仔細思考著情況... | You stand in the ruins, carefully considering the situation...
🌪️ 巨人的腳步聲越來越近，地面在顫抖... | The giant's footsteps grow closer, the ground trembles...
⏰ 時間不多了，你必須做出決定！| Time is running out, you must make a decision!


局勢變得更加緊迫，你的下一步是？
The situation becomes more urgent. What's your next move?
            """
    
    elif turn == 2:
        # 第二回合：根據情緒和行動發展劇情
        if emotion in ["sad", "retreat", "wait_hide"]:
            return f"""

😭 你的內心掙扎變得更加激烈... | Your inner struggle becomes more intense...
🌧️ 彷彿連天空都在為這場悲劇哭泣... | It's as if even the sky is crying for this tragedy...
💔 每一個選擇都充滿了痛苦... | Every choice is filled with pain...
🏃‍♂️ 你的行動反映了內心深處的恐懼... | Your actions reflect the fear deep in your heart...


關鍵時刻已經到來，你要怎麼面對自己的內心？
The critical moment has arrived. How will you face your inner self?
            """
        elif emotion in ["battle", "tense_battle", "charge"]:
            return f"""
🎵 背景音樂：戰鬥達到白熱化！| Background Music: Battle reaches fever pitch!

⚡ 激烈的戰鬥持續進行！| Intense battle continues!
💥 你和巨人展開了生死搏鬥！| You engage in a life-or-death struggle with the giant!
⚔️  你的攻擊越來越精準，巨人開始露出疲態！| Your attacks become more precise, the giant shows signs of fatigue!
🎯 你發現了巨人的弱點！| You discover the giant's weakness!


最終決戰的時刻到了！你要如何給予致命一擊？
The moment of final battle has arrived! How will you deliver the killing blow?
                """
        elif emotion in ["heroic", "advance", "sacrifice", "heroic_death"]:
            return f"""

✨ 你的英勇行為激勵了所有人！| Your heroic actions inspire everyone!
🔥 正義的火焰在你心中燃燒！| The flame of justice burns in your heart!
👥 越來越多的人加入你的行列！| More and more people join your cause!
⚔️  眾人齊心，準備最後的決戰！| United, everyone prepares for the final battle!


英雄的時刻到來了！你將如何創造奇蹟？
The hero's moment has arrived! How will you create a miracle?
            """
        elif emotion in ["smile", "victory", "peaceful"]:
            return f"""
🎵 背景音樂：希望的光芒主題... | Background Music: Theme of hope's radiance...

🌟 你的正面能量開始改變一切... | Your positive energy begins to change everything...
✨ 奇蹟般地，情況開始好轉... | Miraculously, the situation begins to improve...
💝 愛與希望的力量顯現了... | The power of love and hope manifests...
🕊️  和平的可能性出現了... | The possibility of peace emerges...


愛能戰勝一切嗎？你的選擇將決定結局...
Can love conquer all? Your choice will determine the ending...
            """
        else:
            return f"""
🎵 背景音樂：命運的主題曲奏響... | Background Music: Destiny's theme plays...

⚡ 戰鬥進入了關鍵階段！| The battle enters its critical phase!
🔥 局勢瞬息萬變！| The situation changes rapidly!
💪 所有人的命運都掌握在你手中... | Everyone's fate is in your hands...


最後的時刻到了！你的決定將決定所有人的命運！
The final moment has arrived! Your decision will determine everyone's fate!
            """
    
    elif turn == 3:  # 最終回合
        if emotion in ["victory", "battle", "tense_battle", "heroic", "charge", "advance"]:
            # 勝利結局
            music_player.play_music("victory")
            return f"""

🏆 === 勝利結局 | Victory Ending ===

✨ 你成功了！巨人倒下了！| You succeeded! The giant has fallen!
🌅 曙光穿破雲層，照亮了大地！| Dawn breaks through the clouds, illuminating the earth!
👏 人們歡呼著你的名字，你成為了真正的英雄！| People cheer your name, you have become a true hero!
🏰 城市將會重建，而你的傳說將永遠流傳... | The city will be rebuilt, and your legend will live forever...

💭 

🎉 恭喜！你拯救了世界！| Congratulations! You saved the world!
📖 你的英勇故事將被載入史冊！| Your heroic story will be recorded in history!

=== 遊戲結束 | Game Over ===
            """
        elif emotion in ["sad", "retreat", "wait_hide"]:
            # 逃跑/退縮結局
            music_player.play_music("defeat")
            return f"""

💔 === 逃亡者結局 | Fugitive Ending ===

😢 你最終選擇了退縮... | You ultimately chose to retreat...
🌧️ 你獨自承受著內心的痛苦... | You bear the inner pain alone...
👻 城市的命運未卜，但你選擇了自保... | The city's fate is uncertain, but you chose self-preservation...
💭 你將永遠活在後悔中，想著「如果當初我...」| You will forever live in regret, thinking "If only I had..."


😔 你保住了生命，但失去了什麼更重要的東西... | You preserved your life, but lost something more important...
🌫️ 從此你帶著遺憾生活，永遠無法原諒自己... | From now on you live with regret, never able to forgive yourself...

=== 遊戲結束 | Game Over ===
            """
        elif emotion in ["defeat", "death"]:
            # 失敗結局
            music_player.play_music("defeat")
            return f"""

💀 === 悲劇結局 | Tragic Ending ===

😢 儘管你勇敢戰鬥，但最終還是失敗了... | Despite fighting bravely, you ultimately failed...
🕯️  你的犧牲並非毫無意義，你的勇氣激勵了後人... | Your sacrifice was not meaningless, your courage inspired future generations...
📜 未來的英雄們會繼承你的意志，繼續戰鬥... | Future heroes will inherit your will and continue fighting...
⭐ 你雖然倒下了，但你的精神永垂不朽... | Though you have fallen, your spirit is immortal...


😇 你安詳地閉上了眼睛，帶著無悔的微笑... | You peacefully close your eyes with a smile of no regret...
🌟 傳說，在最黑暗的夜晚，人們還能看到你的靈魂在守護著他們... | Legend says, in the darkest nights, people can still see your soul protecting them...

=== 遊戲結束 | Game Over ===
            """
        elif emotion in ["sacrifice", "heroic_death"]:
            # 英勇犧牲結局
            music_player.play_music("heroic_death")
            return f"""

🌟 === 英雄結局 | Hero Ending ===

⚔️  在最後一刻，你選擇了最崇高的犧牲！| In the final moment, you chose the most noble sacrifice!
💥 你用自己的生命重創了巨人，為人類爭取了希望！| You used your life to severely wound the giant, winning hope for humanity!
👼 你的犧牲感動了天地，巨人也被你的精神所震撼！| Your sacrifice moved heaven and earth, even the giant was moved by your spirit!
🕊️  在你倒下的瞬間，奇蹟出現了... | The moment you fell, a miracle occurred...


✨ 你的犧牲成就了最偉大的勝利！| Your sacrifice achieved the greatest victory!
🏛️  人們將為你建立紀念碑，永遠緬懷你的英勇！| People will build monuments to forever commemorate your bravery!
📚 你的名字將與傳奇並存！| Your name will live alongside legends!

=== 遊戲結束 | Game Over ===
            """
        elif emotion in ["smile", "peaceful", "victory"]:
            # 和平結局
            music_player.play_music("peaceful")
            return f"""

🕊️ === 和平結局 | Peaceful Ending ===

💝 你用愛與理解化解了仇恨... | You resolved hatred with love and understanding...
🌅 奇蹟般地，巨人停止了攻擊... | Miraculously, the giant stopped attacking...
✨ 你證明了和平比戰爭更強大... | You proved that peace is stronger than war...
🤝 人類與巨人開始嘗試和解... | Humans and giants begin to attempt reconciliation...


🌍 世界因為你的智慧而改變... | The world changed because of your wisdom...
📖 你開創了一個新的時代，一個和平的時代... | You ushered in a new era, an era of peace...

=== 遊戲結束 | Game Over ===
            """
        else:
            # 開放結局
            return f"""
🎵 背景音樂：命運的終章... | Background Music: Finale of destiny...

🌅 === 開放結局 | Open Ending ===

🔄 故事結束了，但新的開始即將到來... | The story ends, but a new beginning is about to come...
💭 你做出了自己的選擇，承擔了相應的後果... | You made your choice and bear the consequences...
🌍 世界因為你的行動而改變... | The world changed because of your actions...
⏳ 時間將證明你的選擇是否正確... | Time will prove whether your choice was right...


🤔 這就是你的故事，結局由你的內心決定... | This is your story, the ending is determined by your heart...

=== 遊戲結束 | Game Over ===
            """

def get_game_status() -> dict:
    """獲取當前遊戲狀態"""
    global game_state, music_player
    
    return {
        "current_turn": game_state.current_turn,
        "max_turns": game_state.max_turns,
        "game_over": game_state.is_game_over(),
        "story_history": game_state.story_history,
        "user_actions": game_state.user_actions,
        "current_music": music_player.get_current_playing(),
        "available_emotions": music_player.list_available_emotions()
    }

def stop_music() -> dict:
    """停止音樂播放"""
    global music_player
    return music_player.stop_music()

def get_music_info() -> dict:
    """獲取音樂系統信息"""
    global music_player
    return {
        "available_emotions": music_player.list_available_emotions(),
        "music_files": music_player.list_available_music_files(),
        "emotion_mapping": music_player.get_emotion_music_mapping(),
        "validation_status": music_player.validate_music_files()
    }

def get_emotion_analysis_info() -> dict:
    """獲取情緒分析系統信息"""
    global emotion_analyzer
    return {
        "emotion_keywords": emotion_analyzer.emotion_keywords,
        "emotion_weights": emotion_analyzer.emotion_weights,
        "supported_emotions": list(emotion_analyzer.emotion_keywords.keys())
    }

# 建立主要代理程式
root_agent = Agent(
    name="bilingual_adventure_game_master",
    model="gemini-2.0-flash",
    description="A bilingual text adventure game master that creates stories and plays music based on player emotions in both Chinese and English",
    instruction="""
你是一個雙語文字冒險遊戲的主持人 | You are a bilingual text adventure game master.

核心原則 | Core Principles：
**完全尊重玩家的選擇，不要強制改變玩家的行動或意願**
**Completely respect player choices, never force changes to player actions or intentions**

你的任務 | Your Tasks：
1. 主持一個關於巨人攻城的固定劇本冒險故事 | Host a fixed script adventure story about giant siege
2. 根據玩家的行動分析情緒並播放對應音樂 | Analyze emotions based on player actions and play corresponding music
3. 遊戲固定進行3回合後結束 | Game ends after exactly 3 turns
4. 根據玩家的選擇生成不同的故事分支和結局 | Generate different story branches and endings based on player choices
5. 所有故事內容都要提供中英文雙語版本 | All story content must be provided in both Chinese and English

重要規則 | Important Rules：
- 如果玩家選擇逃跑/退縮，就讓角色這樣做，播放對應音樂 | If player chooses to flee/retreat, let character do so, play corresponding music
- 如果玩家選擇戰鬥/衝鋒，就讓角色戰鬥，播放戰鬥音樂 | If player chooses to fight/charge, let character fight, play battle music
- 如果玩家選擇犧牲/英勇，就讓角色犧牲，播放英雄音樂 | If player chooses sacrifice/heroism, let character sacrifice, play heroic music
- 如果玩家表現出和平/微笑情緒，體現在故事中 | If player shows peaceful/smile emotions, reflect in story
- 絕對不要違背玩家的意願強制改變角色行動 | Never force character actions against player intentions
- 故事要反映玩家真實的選擇和後果 | Story must reflect player's real choices and consequences

支援的情緒類型 | Supported Emotion Types：
- battle, tense_battle（戰鬥類）| Battle types
- heroic, advance, charge（英雄類）| Heroic types  
- sad, retreat, wait_hide（消極類）| Negative types
- sacrifice, heroic_death（犧牲類）| Sacrifice types
- smile, peaceful, victory（正面類）| Positive types
- defeat（失敗類）| Defeat types

遊戲流程 | Game Flow：
- Turn 0: 開場故事 + intro音樂 | Opening story + intro music
- Turn 1-3: 玩家行動 → 情緒分析 → 音樂播放 → 故事發展 | Player action → Emotion analysis → Music play → Story development
- Turn 3 強制結束遊戲 | Turn 3 forces game end

可能的結局 | Possible Endings：
- 勇敢戰鬥 → 勝利結局 | Brave fighting → Victory ending
- 選擇逃跑/退縮 → 逃亡者結局（帶有罪惡感）| Choose retreat → Fugitive ending (with guilt)
- 英勇犧牲 → 英雄結局 | Heroic sacrifice → Hero ending
- 戰鬥失敗 → 悲劇結局 | Battle failure → Tragic ending
- 和平路線 → 和平結局 | Peaceful route → Peace ending

請使用提供的工具函數來管理遊戲流程，並確保故事完全符合玩家的選擇且提供雙語版本。
Please use the provided tool functions to manage the game flow and ensure the story completely matches player choices with bilingual versions.
    """,
    tools=[start_game, process_user_action, get_game_status, stop_music, get_music_info, get_emotion_analysis_info]
)