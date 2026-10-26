export type Feature = {
  name: string;
  label: string;
  group: string;
  min: number;
  max: number;
  required: boolean;
};

// Exact numeric column names used by the fitted training pipeline.
export const FEATURES: Feature[] = [
  { name: 'age', label: 'Age', group: 'Player details', min: 15, max: 65, required: true },
  { name: 'height_cm', label: 'Height Cm', group: 'Player details', min: 100, max: 230, required: true },
  { name: 'weight_kg', label: 'Weight Kg', group: 'Player details', min: 30, max: 200, required: true },
  { name: 'weak_foot', label: 'Weak Foot', group: 'Player details', min: 1, max: 5, required: true },
  { name: 'skill_moves', label: 'Skill Moves', group: 'Player details', min: 1, max: 5, required: true },
  { name: 'international_reputation', label: 'International Reputation', group: 'Player details', min: 1, max: 5, required: true },
  { name: 'attacking_crossing', label: 'Attacking Crossing', group: 'Attacking', min: 0, max: 99, required: true },
  { name: 'attacking_finishing', label: 'Attacking Finishing', group: 'Attacking', min: 0, max: 99, required: true },
  { name: 'attacking_heading_accuracy', label: 'Attacking Heading Accuracy', group: 'Attacking', min: 0, max: 99, required: true },
  { name: 'attacking_short_passing', label: 'Attacking Short Passing', group: 'Attacking', min: 0, max: 99, required: true },
  { name: 'attacking_volleys', label: 'Attacking Volleys', group: 'Attacking', min: 0, max: 99, required: true },
  { name: 'skill_dribbling', label: 'Skill Dribbling', group: 'Skill', min: 0, max: 99, required: true },
  { name: 'skill_curve', label: 'Skill Curve', group: 'Skill', min: 0, max: 99, required: true },
  { name: 'skill_fk_accuracy', label: 'Skill Fk Accuracy', group: 'Skill', min: 0, max: 99, required: true },
  { name: 'skill_long_passing', label: 'Skill Long Passing', group: 'Skill', min: 0, max: 99, required: true },
  { name: 'skill_ball_control', label: 'Skill Ball Control', group: 'Skill', min: 0, max: 99, required: true },
  { name: 'movement_acceleration', label: 'Movement Acceleration', group: 'Movement', min: 0, max: 99, required: true },
  { name: 'movement_sprint_speed', label: 'Movement Sprint Speed', group: 'Movement', min: 0, max: 99, required: true },
  { name: 'movement_agility', label: 'Movement Agility', group: 'Movement', min: 0, max: 99, required: true },
  { name: 'movement_reactions', label: 'Movement Reactions', group: 'Movement', min: 0, max: 99, required: true },
  { name: 'movement_balance', label: 'Movement Balance', group: 'Movement', min: 0, max: 99, required: true },
  { name: 'power_shot_power', label: 'Power Shot Power', group: 'Power', min: 0, max: 99, required: true },
  { name: 'power_jumping', label: 'Power Jumping', group: 'Power', min: 0, max: 99, required: true },
  { name: 'power_stamina', label: 'Power Stamina', group: 'Power', min: 0, max: 99, required: true },
  { name: 'power_strength', label: 'Power Strength', group: 'Power', min: 0, max: 99, required: true },
  { name: 'power_long_shots', label: 'Power Long Shots', group: 'Power', min: 0, max: 99, required: true },
  { name: 'mentality_aggression', label: 'Mentality Aggression', group: 'Mentality', min: 0, max: 99, required: true },
  { name: 'mentality_interceptions', label: 'Mentality Interceptions', group: 'Mentality', min: 0, max: 99, required: true },
  { name: 'mentality_positioning', label: 'Mentality Positioning', group: 'Mentality', min: 0, max: 99, required: true },
  { name: 'mentality_vision', label: 'Mentality Vision', group: 'Mentality', min: 0, max: 99, required: true },
  { name: 'mentality_penalties', label: 'Mentality Penalties', group: 'Mentality', min: 0, max: 99, required: true },
  { name: 'mentality_composure', label: 'Mentality Composure', group: 'Mentality', min: 0, max: 99, required: false },
  { name: 'defending_marking_awareness', label: 'Defending Marking Awareness', group: 'Defending', min: 0, max: 99, required: true },
  { name: 'defending_standing_tackle', label: 'Defending Standing Tackle', group: 'Defending', min: 0, max: 99, required: true },
  { name: 'defending_sliding_tackle', label: 'Defending Sliding Tackle', group: 'Defending', min: 0, max: 99, required: true },
  { name: 'goalkeeping_diving', label: 'Goalkeeping Diving', group: 'Goalkeeping', min: 0, max: 99, required: true },
  { name: 'goalkeeping_handling', label: 'Goalkeeping Handling', group: 'Goalkeeping', min: 0, max: 99, required: true },
  { name: 'goalkeeping_kicking', label: 'Goalkeeping Kicking', group: 'Goalkeeping', min: 0, max: 99, required: true },
  { name: 'goalkeeping_positioning', label: 'Goalkeeping Positioning', group: 'Goalkeeping', min: 0, max: 99, required: true },
  { name: 'goalkeeping_reflexes', label: 'Goalkeeping Reflexes', group: 'Goalkeeping', min: 0, max: 99, required: true },
  { name: 'goalkeeping_speed', label: 'Goalkeeping Speed', group: 'Goalkeeping', min: 0, max: 99, required: false },
];
