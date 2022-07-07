class GameStats:
    """跟踪游戏的统计信息。"""
    def __init__(self, ai_game):
        """初始化统计信息。"""
        self.score = None
        self.ships_left = None
        self.settings = ai_game.settings
        # 任何情况下都不应重置最高得分。
        self.high_score = 0

        # 每当玩家开始新游戏时，需要重置一些统计信息。
        # 为此，在方法reset_stats()中初始化大部分统计信息，而不是在__init__() 中直接初始化。
        # 我们在__init__() 中调用这个方法，这样创建GameStats 实例时将妥善地设置这些统计信息，在玩家开始新游戏时也能调用reset_stats()
        self.reset_stats()

        # 游戏刚启动时处于活动状态。
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息。"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


