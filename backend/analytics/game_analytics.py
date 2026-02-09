"""
Game Analytics Module
Tracks game-specific metrics and player behavior
"""

import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass, asdict


logger = logging.getLogger(__name__)


@dataclass
class CombatMetrics:
    """Combat analytics metrics"""
    total_combats: int = 0
    total_damage_dealt: int = 0
    total_damage_taken: int = 0
    total_kills: int = 0
    total_deaths: int = 0
    total_victories: int = 0
    total_defeats: int = 0
    avg_combat_duration: float = 0.0
    most_used_action: str = ""
    favorite_enemy: str = ""


@dataclass
class ProgressionMetrics:
    """Player progression metrics"""
    total_xp_gained: int = 0
    total_levels_gained: int = 0
    current_level: int = 1
    total_quests_completed: int = 0
    total_quests_failed: int = 0
    avg_quest_completion_time: float = 0.0
    achievements_unlocked: int = 0


@dataclass
class EconomyMetrics:
    """Economy analytics metrics"""
    total_gold_earned: int = 0
    total_gold_spent: int = 0
    current_gold: int = 0
    total_items_acquired: int = 0
    total_items_sold: int = 0
    total_items_used: int = 0
    most_valuable_item: str = ""
    total_trades: int = 0


@dataclass
class SocialMetrics:
    """Social interaction metrics"""
    total_chat_messages: int = 0
    total_party_joins: int = 0
    total_friends_added: int = 0
    total_gifts_sent: int = 0
    total_gifts_received: int = 0


class GameAnalytics:
    """
    Game analytics tracker
    """

    def __init__(self):
        """Initialize game analytics"""
        self.combat_metrics: Dict[int, CombatMetrics] = defaultdict(CombatMetrics)
        self.progression_metrics: Dict[int, ProgressionMetrics] = defaultdict(ProgressionMetrics)
        self.economy_metrics: Dict[int, EconomyMetrics] = defaultdict(EconomyMetrics)
        self.social_metrics: Dict[int, SocialMetrics] = defaultdict(SocialMetrics)

        # Detailed tracking
        self.combat_history: List[Dict[str, Any]] = []
        self.quest_history: List[Dict[str, Any]] = []
        self.item_history: List[Dict[str, Any]] = []

        # Global statistics
        self.global_stats = {
            'total_players': 0,
            'total_combats': 0,
            'total_quests_completed': 0,
            'total_gold_circulated': 0,
            'total_items_created': 0
        }

    # ============================================================================
    # COMBAT ANALYTICS
    # ============================================================================

    def track_combat_start(
        self,
        user_id: int,
        enemy_id: str,
        enemy_level: int,
        player_level: int
    ):
        """
        Track combat start

        Args:
            user_id: User identifier
            enemy_id: Enemy identifier
            enemy_level: Enemy level
            player_level: Player level
        """
        combat_data = {
            'user_id': user_id,
            'enemy_id': enemy_id,
            'enemy_level': enemy_level,
            'player_level': player_level,
            'start_time': time.time(),
            'end_time': None,
            'duration': 0,
            'result': None,
            'damage_dealt': 0,
            'damage_taken': 0,
            'actions': []
        }

        self.combat_history.append(combat_data)
        self.global_stats['total_combats'] += 1

        logger.info(f"Combat started: user {user_id} vs {enemy_id}")

    def track_combat_action(
        self,
        user_id: int,
        action: str,
        damage: int = 0
    ):
        """
        Track combat action

        Args:
            user_id: User identifier
            action: Action type
            damage: Damage dealt/taken
        """
        # Find active combat
        for combat in reversed(self.combat_history):
            if combat['user_id'] == user_id and combat['end_time'] is None:
                combat['actions'].append({
                    'action': action,
                    'damage': damage,
                    'timestamp': time.time()
                })
                break

    def track_combat_end(
        self,
        user_id: int,
        result: str,
        damage_dealt: int,
        damage_taken: int,
        xp_gained: int = 0,
        loot: Optional[List[str]] = None
    ):
        """
        Track combat end

        Args:
            user_id: User identifier
            result: Combat result ('victory' or 'defeat')
            damage_dealt: Total damage dealt
            damage_taken: Total damage taken
            xp_gained: XP gained
            loot: Loot items
        """
        metrics = self.combat_metrics[user_id]
        metrics.total_combats += 1
        metrics.total_damage_dealt += damage_dealt
        metrics.total_damage_taken += damage_taken

        if result == 'victory':
            metrics.total_victories += 1
            metrics.total_kills += 1
        else:
            metrics.total_defeats += 1
            metrics.total_deaths += 1

        # Find and update combat record
        for combat in reversed(self.combat_history):
            if combat['user_id'] == user_id and combat['end_time'] is None:
                combat['end_time'] = time.time()
                combat['duration'] = combat['end_time'] - combat['start_time']
                combat['result'] = result
                combat['damage_dealt'] = damage_dealt
                combat['damage_taken'] = damage_taken
                combat['xp_gained'] = xp_gained
                combat['loot'] = loot or []

                # Update average combat duration
                all_durations = [
                    c['duration'] for c in self.combat_history
                    if c['user_id'] == user_id and c['duration'] > 0
                ]
                if all_durations:
                    metrics.avg_combat_duration = sum(all_durations) / len(all_durations)

                break

        logger.info(f"Combat ended: user {user_id} - {result}")

    def get_combat_analytics(
        self,
        user_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get combat analytics

        Args:
            user_id: User identifier (None for all users)
            start_date: Start date
            end_date: End date

        Returns:
            Combat analytics data
        """
        if user_id:
            metrics = self.combat_metrics[user_id]

            # Filter combat history
            combats = [
                c for c in self.combat_history
                if c['user_id'] == user_id
            ]

            # Apply date filter
            if start_date or end_date:
                start_time = start_date.timestamp() if start_date else 0
                end_time = end_date.timestamp() if end_date else time.time()
                combats = [
                    c for c in combats
                    if start_time <= c['start_time'] <= end_time
                ]

            # Calculate win rate
            win_rate = (
                (metrics.total_victories / metrics.total_combats * 100)
                if metrics.total_combats > 0 else 0
            )

            # Most used action
            action_counts = defaultdict(int)
            for combat in combats:
                for action in combat['actions']:
                    action_counts[action['action']] += 1

            most_used_action = max(action_counts.items(), key=lambda x: x[1])[0] if action_counts else "none"

            return {
                'total_combats': metrics.total_combats,
                'total_victories': metrics.total_victories,
                'total_defeats': metrics.total_defeats,
                'win_rate': win_rate,
                'total_damage_dealt': metrics.total_damage_dealt,
                'total_damage_taken': metrics.total_damage_taken,
                'avg_combat_duration': metrics.avg_combat_duration,
                'most_used_action': most_used_action,
                'recent_combats': combats[-10:]
            }
        else:
            # Global combat analytics
            total_combats = sum(m.total_combats for m in self.combat_metrics.values())
            total_victories = sum(m.total_victories for m in self.combat_metrics.values())

            return {
                'total_combats': total_combats,
                'total_victories': total_victories,
                'global_win_rate': (total_victories / total_combats * 100) if total_combats > 0 else 0,
                'total_players': len(self.combat_metrics),
                'avg_combats_per_player': total_combats / len(self.combat_metrics) if self.combat_metrics else 0
            }

    # ============================================================================
    # PROGRESSION ANALYTICS
    # ============================================================================

    def track_xp_gained(self, user_id: int, xp: int):
        """Track XP gained"""
        metrics = self.progression_metrics[user_id]
        metrics.total_xp_gained += xp

    def track_level_up(self, user_id: int, new_level: int):
        """Track level up"""
        metrics = self.progression_metrics[user_id]
        metrics.total_levels_gained += 1
        metrics.current_level = new_level

        logger.info(f"User {user_id} leveled up to {new_level}")

    def track_quest_started(
        self,
        user_id: int,
        quest_id: int,
        quest_type: str,
        quest_name: str
    ):
        """Track quest started"""
        quest_data = {
            'user_id': user_id,
            'quest_id': quest_id,
            'quest_type': quest_type,
            'quest_name': quest_name,
            'start_time': time.time(),
            'end_time': None,
            'duration': 0,
            'result': None,
            'rewards': None
        }

        self.quest_history.append(quest_data)

    def track_quest_completed(
        self,
        user_id: int,
        quest_id: int,
        xp_reward: int,
        gold_reward: int,
        items_reward: Optional[List[str]] = None
    ):
        """Track quest completed"""
        metrics = self.progression_metrics[user_id]
        metrics.total_quests_completed += 1

        # Find and update quest record
        for quest in reversed(self.quest_history):
            if quest['user_id'] == user_id and quest['quest_id'] == quest_id and quest['end_time'] is None:
                quest['end_time'] = time.time()
                quest['duration'] = quest['end_time'] - quest['start_time']
                quest['result'] = 'completed'
                quest['rewards'] = {
                    'xp': xp_reward,
                    'gold': gold_reward,
                    'items': items_reward or []
                }

                # Update average completion time
                completed_quests = [
                    q for q in self.quest_history
                    if q['user_id'] == user_id and q['result'] == 'completed'
                ]
                if completed_quests:
                    metrics.avg_quest_completion_time = sum(q['duration'] for q in completed_quests) / len(completed_quests)

                break

        self.global_stats['total_quests_completed'] += 1
        logger.info(f"Quest {quest_id} completed by user {user_id}")

    def track_quest_failed(self, user_id: int, quest_id: int):
        """Track quest failed"""
        metrics = self.progression_metrics[user_id]
        metrics.total_quests_failed += 1

        # Update quest record
        for quest in reversed(self.quest_history):
            if quest['user_id'] == user_id and quest['quest_id'] == quest_id and quest['end_time'] is None:
                quest['end_time'] = time.time()
                quest['duration'] = quest['end_time'] - quest['start_time']
                quest['result'] = 'failed'
                break

    def track_achievement(self, user_id: int, achievement_id: str):
        """Track achievement unlocked"""
        metrics = self.progression_metrics[user_id]
        metrics.achievements_unlocked += 1

        logger.info(f"Achievement {achievement_id} unlocked by user {user_id}")

    def get_progression_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get progression analytics for user"""
        metrics = self.progression_metrics[user_id]

        # Get quest completion rate
        total_quests = metrics.total_quests_completed + metrics.total_quests_failed
        completion_rate = (
            (metrics.total_quests_completed / total_quests * 100)
            if total_quests > 0 else 0
        )

        return {
            'current_level': metrics.current_level,
            'total_xp_gained': metrics.total_xp_gained,
            'total_levels_gained': metrics.total_levels_gained,
            'total_quests_completed': metrics.total_quests_completed,
            'total_quests_failed': metrics.total_quests_failed,
            'quest_completion_rate': completion_rate,
            'avg_quest_completion_time': metrics.avg_quest_completion_time,
            'achievements_unlocked': metrics.achievements_unlocked
        }

    # ============================================================================
    # ECONOMY ANALYTICS
    # ============================================================================

    def track_gold_earned(self, user_id: int, amount: int, source: str):
        """Track gold earned"""
        metrics = self.economy_metrics[user_id]
        metrics.total_gold_earned += amount
        metrics.current_gold += amount

        self.global_stats['total_gold_circulated'] += amount

    def track_gold_spent(self, user_id: int, amount: int, category: str):
        """Track gold spent"""
        metrics = self.economy_metrics[user_id]
        metrics.total_gold_spent += amount
        metrics.current_gold -= amount

    def track_item_acquired(
        self,
        user_id: int,
        item_id: str,
        item_name: str,
        source: str,
        value: int = 0
    ):
        """Track item acquired"""
        metrics = self.economy_metrics[user_id]
        metrics.total_items_acquired += 1

        item_data = {
            'user_id': user_id,
            'item_id': item_id,
            'item_name': item_name,
            'source': source,
            'value': value,
            'timestamp': time.time(),
            'action': 'acquired'
        }

        self.item_history.append(item_data)
        self.global_stats['total_items_created'] += 1

    def track_item_sold(
        self,
        user_id: int,
        item_id: str,
        sell_price: int
    ):
        """Track item sold"""
        metrics = self.economy_metrics[user_id]
        metrics.total_items_sold += 1
        metrics.total_gold_earned += sell_price
        metrics.current_gold += sell_price

    def track_item_used(
        self,
        user_id: int,
        item_id: str,
        item_name: str
    ):
        """Track item used"""
        metrics = self.economy_metrics[user_id]
        metrics.total_items_used += 1

        item_data = {
            'user_id': user_id,
            'item_id': item_id,
            'item_name': item_name,
            'timestamp': time.time(),
            'action': 'used'
        }

        self.item_history.append(item_data)

    def get_economy_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get economy analytics for user"""
        metrics = self.economy_metrics[user_id]

        # Calculate net worth
        net_worth = metrics.current_gold

        # Get most acquired items
        user_items = [i for i in self.item_history if i['user_id'] == user_id and i['action'] == 'acquired']
        item_counts = defaultdict(int)
        for item in user_items:
            item_counts[item['item_name']] += 1

        most_acquired = max(item_counts.items(), key=lambda x: x[1]) if item_counts else ("none", 0)

        return {
            'current_gold': metrics.current_gold,
            'total_gold_earned': metrics.total_gold_earned,
            'total_gold_spent': metrics.total_gold_spent,
            'net_worth': net_worth,
            'total_items_acquired': metrics.total_items_acquired,
            'total_items_sold': metrics.total_items_sold,
            'total_items_used': metrics.total_items_used,
            'most_acquired_item': most_acquired[0],
            'most_acquired_count': most_acquired[1]
        }

    # ============================================================================
    # SOCIAL ANALYTICS
    # ============================================================================

    def track_chat_message(self, user_id: int):
        """Track chat message"""
        metrics = self.social_metrics[user_id]
        metrics.total_chat_messages += 1

    def track_party_join(self, user_id: int):
        """Track party join"""
        metrics = self.social_metrics[user_id]
        metrics.total_party_joins += 1

    def track_friend_added(self, user_id: int):
        """Track friend added"""
        metrics = self.social_metrics[user_id]
        metrics.total_friends_added += 1

    def track_gift(self, sender_id: int, recipient_id: int):
        """Track gift sent/received"""
        self.social_metrics[sender_id].total_gifts_sent += 1
        self.social_metrics[recipient_id].total_gifts_received += 1

    def get_social_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get social analytics for user"""
        metrics = self.social_metrics[user_id]

        return {
            'total_chat_messages': metrics.total_chat_messages,
            'total_party_joins': metrics.total_party_joins,
            'total_friends_added': metrics.total_friends_added,
            'total_gifts_sent': metrics.total_gifts_sent,
            'total_gifts_received': metrics.total_gifts_received
        }

    # ============================================================================
    # GLOBAL ANALYTICS
    # ============================================================================

    def get_global_analytics(self) -> Dict[str, Any]:
        """Get global game analytics"""
        return {
            'total_players': len(self.combat_metrics),
            'total_combats': self.global_stats['total_combats'],
            'total_quests_completed': self.global_stats['total_quests_completed'],
            'total_gold_circulated': self.global_stats['total_gold_circulated'],
            'total_items_created': self.global_stats['total_items_created'],
            'avg_level': sum(m.current_level for m in self.progression_metrics.values()) / len(self.progression_metrics) if self.progression_metrics else 0,
            'total_achievements': sum(m.achievements_unlocked for m in self.progression_metrics.values())
        }

    def get_player_profile(self, user_id: int) -> Dict[str, Any]:
        """Get complete player profile analytics"""
        return {
            'combat': self.get_combat_analytics(user_id),
            'progression': self.get_progression_analytics(user_id),
            'economy': self.get_economy_analytics(user_id),
            'social': self.get_social_analytics(user_id)
        }


# Global game analytics instance
_game_analytics = None


def get_game_analytics() -> GameAnalytics:
    """Get global game analytics instance"""
    global _game_analytics
    if _game_analytics is None:
        _game_analytics = GameAnalytics()
    return _game_analytics
