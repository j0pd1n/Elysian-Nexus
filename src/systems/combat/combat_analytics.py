from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import time
import logging
import math
from collections import defaultdict

class CombatEventType(Enum):
    DAMAGE_DEALT = "damage_dealt"
    DAMAGE_TAKEN = "damage_taken"
    ABILITY_USED = "ability_used"
    ITEM_USED = "item_used"
    STATUS_EFFECT = "status_effect"
    POSITION_CHANGE = "position_change"
    RESOURCE_CHANGE = "resource_change"

@dataclass
class CombatEvent:
    event_type: CombatEventType
    timestamp: float
    source_id: str
    target_id: str
    value: float
    details: Dict[str, Any]

class CombatPhase(Enum):
    OPENING = "opening"
    MIDGAME = "midgame"
    ENDGAME = "endgame"
    CRITICAL = "critical"

@dataclass
class CombatSession:
    session_id: str
    start_time: float
    end_time: float
    events: List[CombatEvent]
    victory: bool
    difficulty_level: str
    player_stats: Dict[str, Any]
    enemy_stats: Dict[str, Any]

class CombatAnalytics:
    def __init__(self):
        self.sessions: List[CombatSession] = []
        self.current_session: Optional[CombatSession] = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("CombatAnalytics")
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler("logs/combat_analytics.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(handler)
        return logger
        
    def start_session(
        self,
        player_stats: Dict[str, Any],
        enemy_stats: Dict[str, Any],
        difficulty_level: str
    ):
        """Start a new combat session"""
        if self.current_session:
            self.logger.warning("Previous session not properly ended")
            self.end_session(victory=False)
            
        session_id = f"combat_{int(time.time())}"
        self.current_session = CombatSession(
            session_id=session_id,
            start_time=time.time(),
            end_time=0,
            events=[],
            victory=False,
            difficulty_level=difficulty_level,
            player_stats=player_stats,
            enemy_stats=enemy_stats
        )
        
        self.logger.info(f"Started combat session: {session_id}")
        
    def end_session(self, victory: bool):
        """End current combat session"""
        if not self.current_session:
            self.logger.error("No active combat session to end")
            return
            
        self.current_session.end_time = time.time()
        self.current_session.victory = victory
        self.sessions.append(self.current_session)
        
        self.logger.info(
            f"Ended combat session: {self.current_session.session_id} "
            f"(Victory: {victory})"
        )
        
        self.current_session = None
        
    def record_event(
        self,
        event_type: CombatEventType,
        source_id: str,
        target_id: str,
        value: float,
        details: Dict[str, Any] = None
    ):
        """Record a combat event"""
        if not self.current_session:
            self.logger.error("No active combat session")
            return
            
        event = CombatEvent(
            event_type=event_type,
            timestamp=time.time(),
            source_id=source_id,
            target_id=target_id,
            value=value,
            details=details or {}
        )
        
        self.current_session.events.append(event)
        
    def analyze_session(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze a combat session"""
        duration = session.end_time - session.start_time
        
        analysis = {
            "session_id": session.session_id,
            "duration": duration,
            "victory": session.victory,
            "difficulty_level": session.difficulty_level,
            "damage_stats": self._analyze_damage(session),
            "ability_usage": self._analyze_abilities(session),
            "resource_efficiency": self._analyze_resources(session),
            "combat_phases": self._analyze_phases(session),
            "positioning": self._analyze_positioning(session),
            "status_effects": self._analyze_status_effects(session)
        }
        
        return analysis
        
    def _analyze_damage(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze damage dealt and taken"""
        damage_dealt = []
        damage_taken = []
        
        for event in session.events:
            if event.event_type == CombatEventType.DAMAGE_DEALT:
                damage_dealt.append(event.value)
            elif event.event_type == CombatEventType.DAMAGE_TAKEN:
                damage_taken.append(event.value)
                
        return {
            "total_dealt": sum(damage_dealt),
            "total_taken": sum(damage_taken),
            "dps": sum(damage_dealt) / session.end_time - session.start_time,
            "damage_taken_per_second": sum(damage_taken) / session.end_time - session.start_time,
            "highest_hit": max(damage_dealt) if damage_dealt else 0,
            "worst_hit_taken": max(damage_taken) if damage_taken else 0
        }
        
    def _analyze_abilities(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze ability usage patterns"""
        ability_usage = defaultdict(int)
        ability_damage = defaultdict(list)
        ability_timing = defaultdict(list)
        
        for event in session.events:
            if event.event_type == CombatEventType.ABILITY_USED:
                ability_name = event.details.get("ability_name", "unknown")
                ability_usage[ability_name] += 1
                ability_damage[ability_name].append(event.value)
                ability_timing[ability_name].append(event.timestamp - session.start_time)
                
        return {
            "usage_counts": dict(ability_usage),
            "average_damage": {
                name: sum(damages) / len(damages)
                for name, damages in ability_damage.items()
            },
            "timing_patterns": {
                name: self._analyze_timing_pattern(timings)
                for name, timings in ability_timing.items()
            }
        }
        
    def _analyze_resources(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze resource usage efficiency"""
        resource_changes = defaultdict(list)
        
        for event in session.events:
            if event.event_type == CombatEventType.RESOURCE_CHANGE:
                resource_type = event.details.get("resource_type", "unknown")
                resource_changes[resource_type].append(event.value)
                
        return {
            resource: {
                "total_consumed": abs(sum(changes)),
                "efficiency": self._calculate_efficiency(changes)
            }
            for resource, changes in resource_changes.items()
        }
        
    def _analyze_phases(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze different phases of combat"""
        duration = session.end_time - session.start_time
        phase_duration = duration / 3  # Simple division into three phases
        
        phases = {
            CombatPhase.OPENING: [],
            CombatPhase.MIDGAME: [],
            CombatPhase.ENDGAME: []
        }
        
        for event in session.events:
            relative_time = event.timestamp - session.start_time
            if relative_time < phase_duration:
                phases[CombatPhase.OPENING].append(event)
            elif relative_time < phase_duration * 2:
                phases[CombatPhase.MIDGAME].append(event)
            else:
                phases[CombatPhase.ENDGAME].append(event)
                
        return {
            phase.value: self._analyze_phase_events(events)
            for phase, events in phases.items()
        }
        
    def _analyze_positioning(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze combat positioning"""
        positions = []
        
        for event in session.events:
            if event.event_type == CombatEventType.POSITION_CHANGE:
                positions.append(event.details.get("position", {}))
                
        return {
            "movement_patterns": self._analyze_movement(positions),
            "positioning_effectiveness": self._calculate_positioning_effectiveness(session)
        }
        
    def _analyze_status_effects(self, session: CombatSession) -> Dict[str, Any]:
        """Analyze status effect patterns"""
        status_effects = defaultdict(list)
        
        for event in session.events:
            if event.event_type == CombatEventType.STATUS_EFFECT:
                effect_name = event.details.get("effect_name", "unknown")
                status_effects[effect_name].append({
                    "timestamp": event.timestamp,
                    "duration": event.details.get("duration", 0),
                    "strength": event.value
                })
                
        return {
            effect: {
                "total_duration": sum(e["duration"] for e in effects),
                "average_strength": sum(e["strength"] for e in effects) / len(effects),
                "frequency": len(effects)
            }
            for effect, effects in status_effects.items()
        }
        
    def _analyze_timing_pattern(self, timings: List[float]) -> Dict[str, float]:
        """Analyze timing patterns of events"""
        if len(timings) < 2:
            return {"pattern_strength": 0, "average_interval": 0}
            
        intervals = [t2 - t1 for t1, t2 in zip(timings[:-1], timings[1:])]
        avg_interval = sum(intervals) / len(intervals)
        variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals)
        
        return {
            "pattern_strength": 1 / (1 + math.sqrt(variance)),
            "average_interval": avg_interval
        }
        
    def _calculate_efficiency(self, changes: List[float]) -> float:
        """Calculate resource usage efficiency"""
        if not changes:
            return 0
            
        total_gain = sum(c for c in changes if c > 0)
        total_loss = abs(sum(c for c in changes if c < 0))
        
        if total_loss == 0:
            return 1.0
            
        return total_gain / total_loss
        
    def _analyze_phase_events(self, events: List[CombatEvent]) -> Dict[str, Any]:
        """Analyze events within a combat phase"""
        if not events:
            return {"intensity": 0, "effectiveness": 0}
            
        damage_dealt = sum(e.value for e in events 
                          if e.event_type == CombatEventType.DAMAGE_DEALT)
        damage_taken = sum(e.value for e in events 
                          if e.event_type == CombatEventType.DAMAGE_TAKEN)
        abilities_used = sum(1 for e in events 
                           if e.event_type == CombatEventType.ABILITY_USED)
                           
        duration = events[-1].timestamp - events[0].timestamp if len(events) > 1 else 1
        
        return {
            "intensity": (damage_dealt + damage_taken) / duration,
            "effectiveness": damage_dealt / (damage_taken + 1),
            "ability_frequency": abilities_used / duration
        }
        
    def _analyze_movement(self, positions: List[Dict[str, float]]) -> Dict[str, Any]:
        """Analyze movement patterns"""
        if len(positions) < 2:
            return {"total_distance": 0, "average_speed": 0}
            
        distances = []
        for p1, p2 in zip(positions[:-1], positions[1:]):
            dx = p2.get("x", 0) - p1.get("x", 0)
            dy = p2.get("y", 0) - p1.get("y", 0)
            distances.append(math.sqrt(dx*dx + dy*dy))
            
        return {
            "total_distance": sum(distances),
            "average_speed": sum(distances) / len(distances)
        }
        
    def _calculate_positioning_effectiveness(
        self,
        session: CombatSession
    ) -> Dict[str, float]:
        """Calculate effectiveness of positioning"""
        damage_events = [e for e in session.events 
                        if e.event_type in [CombatEventType.DAMAGE_DEALT,
                                          CombatEventType.DAMAGE_TAKEN]]
                                          
        if not damage_events:
            return {"effectiveness": 0}
            
        # Calculate damage ratio based on positioning
        positioned_damage = sum(e.value for e in damage_events
                              if e.details.get("positioned", False))
        total_damage = sum(e.value for e in damage_events)
        
        return {
            "effectiveness": positioned_damage / total_damage if total_damage > 0 else 0
        }
        
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a specific combat session"""
        session = next((s for s in self.sessions if s.session_id == session_id), None)
        if not session:
            return None
            
        return self.analyze_session(session)
        
    def get_performance_trends(
        self,
        num_sessions: Optional[int] = None
    ) -> Dict[str, Any]:
        """Analyze performance trends across sessions"""
        sessions = self.sessions[-num_sessions:] if num_sessions else self.sessions
        if not sessions:
            return {"status": "no_data"}
            
        trends = {
            "victory_rate": sum(1 for s in sessions if s.victory) / len(sessions),
            "average_duration": sum(s.end_time - s.start_time for s in sessions) / len(sessions),
            "damage_trends": self._analyze_damage_trends(sessions),
            "ability_trends": self._analyze_ability_trends(sessions),
            "improvement_rate": self._calculate_improvement_rate(sessions)
        }
        
        return trends
        
    def _analyze_damage_trends(
        self,
        sessions: List[CombatSession]
    ) -> Dict[str, List[float]]:
        """Analyze damage trends across sessions"""
        return {
            "damage_dealt": [
                sum(e.value for e in s.events 
                    if e.event_type == CombatEventType.DAMAGE_DEALT)
                for s in sessions
            ],
            "damage_taken": [
                sum(e.value for e in s.events 
                    if e.event_type == CombatEventType.DAMAGE_TAKEN)
                for s in sessions
            ]
        }
        
    def _analyze_ability_trends(
        self,
        sessions: List[CombatSession]
    ) -> Dict[str, Dict[str, List[int]]]:
        """Analyze ability usage trends across sessions"""
        ability_trends = defaultdict(lambda: defaultdict(list))
        
        for session in sessions:
            ability_counts = defaultdict(int)
            for event in session.events:
                if event.event_type == CombatEventType.ABILITY_USED:
                    ability_name = event.details.get("ability_name", "unknown")
                    ability_counts[ability_name] += 1
                    
            for ability, count in ability_counts.items():
                ability_trends[ability]["usage"].append(count)
                
        return dict(ability_trends)
        
    def _calculate_improvement_rate(
        self,
        sessions: List[CombatSession]
    ) -> Dict[str, float]:
        """Calculate rate of improvement across sessions"""
        if len(sessions) < 2:
            return {"rate": 0}
            
        # Calculate performance scores for each session
        scores = []
        for session in sessions:
            damage_dealt = sum(e.value for e in session.events 
                             if e.event_type == CombatEventType.DAMAGE_DEALT)
            damage_taken = sum(e.value for e in session.events 
                             if e.event_type == CombatEventType.DAMAGE_TAKEN)
            duration = session.end_time - session.start_time
            
            score = (damage_dealt / (damage_taken + 1)) * (1 + 0.1 * session.victory)
            scores.append(score)
            
        # Calculate improvement rate
        improvement_rates = [
            (s2 - s1) / s1 for s1, s2 in zip(scores[:-1], scores[1:])
        ]
        
        return {
            "rate": sum(improvement_rates) / len(improvement_rates)
            if improvement_rates else 0
        }
        
    def export_analytics(self, file_path: str):
        """Export analytics data"""
        data = {
            "sessions": [
                {
                    "session_id": session.session_id,
                    "start_time": session.start_time,
                    "end_time": session.end_time,
                    "victory": session.victory,
                    "difficulty_level": session.difficulty_level,
                    "events": [
                        {
                            "event_type": event.event_type.value,
                            "timestamp": event.timestamp,
                            "source_id": event.source_id,
                            "target_id": event.target_id,
                            "value": event.value,
                            "details": event.details
                        }
                        for event in session.events
                    ]
                }
                for session in self.sessions
            ]
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    def import_analytics(self, file_path: str):
        """Import analytics data"""
        with open(file_path, "r") as f:
            data = json.load(f)
            
        self.sessions = [
            CombatSession(
                session_id=s["session_id"],
                start_time=s["start_time"],
                end_time=s["end_time"],
                victory=s["victory"],
                difficulty_level=s["difficulty_level"],
                events=[
                    CombatEvent(
                        event_type=CombatEventType(e["event_type"]),
                        timestamp=e["timestamp"],
                        source_id=e["source_id"],
                        target_id=e["target_id"],
                        value=e["value"],
                        details=e["details"]
                    )
                    for e in s["events"]
                ],
                player_stats={},  # These would need to be stored in the export
                enemy_stats={}    # These would need to be stored in the export
            )
            for s in data["sessions"]
        ] 