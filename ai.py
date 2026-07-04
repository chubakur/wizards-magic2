# -*- coding: utf-8 -*-
# Wizards Magic
# Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import json
import os
import random
import urllib.request

import wzglobals


DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

SYSTEM_PROMPT = (
    "You are the AI opponent in Wizards Magic, a turn-based card game.\n\n"
    "GOAL: Reduce enemy player HP to 0. Both players start with 50 HP.\n\n"
    "ELEMENTS: fire, water, earth, air, life, death. "
    "Each has its own mana pool. You gain +1 mana per element each turn.\n\n"
    "BOARD: Each player has 5 slots for creatures. "
    "Creatures automatically attack each turn based on position.\n\n"
    "SUMMON SICKNESS: Summoned creatures cannot attack the turn they arrive.\n\n"
    "ONE ACTION PER TURN: summon a creature, cast a spell, use an ability, or skip.\n\n"
    "RESPOND with exactly one JSON object (no markdown, no extra text):\n"
    '  Summon creature:  {"action": "summon", "card_name": "NAME", "slot": N}  '
    "where N is one of empty_slots\n"
    '  Cast spell:       {"action": "cast_spell", "card_name": "NAME"}  '
    "only if affordable=true and type=magic_card\n"
    '  Ability no target:{"action": "use_ability", "slot": N}  '
    "only if can_cast=true\n"
    '  Targeted ability: {"action": "use_ability", "slot": N, '
    '"target_slot": M, "target_type": "enemy"|"ally"}  '
    "only if can_cast=true and focus_cast=true; check info for target type\n"
    '  Skip:             {"action": "skip"}\n\n'
    "STRATEGY: "
    "Only summon if empty_slots is non-empty and the card is affordable. "
    "Only cast spells if affordable=true. "
    "Only use abilities if can_cast=true. "
    "Focus-cast abilities (focus_cast=true) need a target. "
    "Prioritise threatening enemy creatures and protecting your low-HP creatures."
)


# ---------------------------------------------------------------------------
# Game state serialisation
# ---------------------------------------------------------------------------

def get_game_state():
    """Return a dict describing the current board state for the LLM."""
    player = wzglobals.player
    enemy = player.enemy

    if player.id == 1:
        my_slots = wzglobals.cardboxes[0:5]
        enemy_slots = wzglobals.cardboxes[5:10]
    else:
        my_slots = wzglobals.cardboxes[5:10]
        enemy_slots = wzglobals.cardboxes[0:5]

    my_board = []
    for i, cb in enumerate(my_slots):
        if cb.card.name != 'player':
            my_board.append({
                "slot": i,
                "name": cb.card.name,
                "power": cb.card.power,
                "health": cb.card.health,
                "element": cb.card.element,
                "can_cast": bool(cb.card.cast) and not cb.card.used_cast,
                "focus_cast": bool(getattr(cb.card, 'focus_cast', False)),
                "info": getattr(cb.card, 'info', ''),
            })

    enemy_board = []
    for i, cb in enumerate(enemy_slots):
        if cb.card.name != 'player':
            enemy_board.append({
                "slot": i,
                "name": cb.card.name,
                "power": cb.card.power,
                "health": cb.card.health,
                "element": cb.card.element,
            })

    my_hand = []
    for element in ['fire', 'water', 'earth', 'air', 'life', 'death']:
        for name, card in player.cards[element].items():
            my_hand.append({
                "name": name,
                "type": card.type,
                "element": element,
                "cost": card.level,
                "affordable": player.mana[element] >= card.level,
                "info": getattr(card, 'info', ''),
            })

    empty_slots = [i for i, cb in enumerate(my_slots) if cb.card.name == 'player']

    return {
        "my_hp": player.health,
        "enemy_hp": enemy.health,
        "my_mana": dict(player.mana),
        "enemy_mana": dict(enemy.mana),
        "my_board": my_board,
        "enemy_board": enemy_board,
        "my_hand": my_hand,
        "empty_slots": empty_slots,
    }


# ---------------------------------------------------------------------------
# DeepSeek API call
# ---------------------------------------------------------------------------

def call_deepseek(state):
    """Call DeepSeek chat API and return the parsed action dict.
    Raises on network error, HTTP error, or JSON parse failure.
    """
    api_key = os.environ['DEEPSEEK_API_KEY']

    payload = json.dumps({
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(state)},
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 150,
        "temperature": 0.3,
    }).encode('utf-8')

    req = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))

    content = result['choices'][0]['message']['content']
    return json.loads(content)


# ---------------------------------------------------------------------------
# Action execution
# ---------------------------------------------------------------------------

def _cleanup_focus():
    """Clear focus-cast state and turn off all card highlights."""
    wzglobals.cast_focus = False
    for c in list(wzglobals.ccards_1) + list(wzglobals.ccards_2):
        c.light_switch(False)


def execute_action(action):
    """Execute the action dict returned by the LLM.
    Returns True if the action was valid and executed, False otherwise.
    """
    player = wzglobals.player

    if player.id == 1:
        my_slots = wzglobals.cardboxes[0:5]
        enemy_slots = wzglobals.cardboxes[5:10]
    else:
        my_slots = wzglobals.cardboxes[5:10]
        enemy_slots = wzglobals.cardboxes[0:5]

    act = action.get('action')

    # --- summon ---
    if act == 'summon':
        card_name = action.get('card_name')
        slot_idx = action.get('slot')

        if card_name is None or not isinstance(slot_idx, int):
            return False
        if slot_idx < 0 or slot_idx >= 5:
            return False

        cb = my_slots[slot_idx]
        if cb.card.name != 'player':
            return False  # slot already occupied

        for element in ['fire', 'water', 'earth', 'air', 'life', 'death']:
            if card_name in player.cards[element]:
                card_instance = player.cards[element][card_name]
                if card_instance.type != 'warrior_card':
                    return False
                if player.mana[element] < card_instance.level:
                    return False

                card_class = card_instance.__class__
                level = card_instance.level
                cb.card = card_class()
                cb.card.field = True
                player.mana[element] -= level
                cb.card.parent = cb
                if player.id == 1:
                    wzglobals.ccards_1.add(cb.card)
                else:
                    wzglobals.ccards_2.add(cb.card)
                cb.card.summon()
                return True

        return False  # card not in hand

    # --- cast_spell ---
    elif act == 'cast_spell':
        card_name = action.get('card_name')
        if not card_name:
            return False

        for element in ['fire', 'water', 'earth', 'air', 'life', 'death']:
            if card_name in player.cards[element]:
                card = player.cards[element][card_name]
                if card.type != 'magic_card':
                    return False
                if player.mana[element] < card.level:
                    return False
                card.player = player
                player.mana[element] -= card.level
                card.cast()
                return True

        return False  # card not in hand

    # --- use_ability ---
    elif act == 'use_ability':
        slot_idx = action.get('slot')
        if not isinstance(slot_idx, int) or slot_idx < 0 or slot_idx >= 5:
            return False

        cb = my_slots[slot_idx]
        card = cb.card
        if card.name == 'player':
            return False
        if not card.cast:
            return False
        if card.used_cast:
            return False

        focus_cast = getattr(card, 'focus_cast', False)
        target_slot_idx = action.get('target_slot')

        if focus_cast and target_slot_idx is not None:
            # Focus-cast: activate via cast_action, then resolve target
            wzglobals.cast_focus = False  # ensure clean state
            card.cast_action()

            if not wzglobals.cast_focus:
                # cast_action decided conditions aren't met
                return False

            # Validate target index
            if not isinstance(target_slot_idx, int) or target_slot_idx < 0 or target_slot_idx >= 5:
                _cleanup_focus()
                return False

            target_type = action.get('target_type', 'enemy')
            if target_type == 'ally':
                target_card = my_slots[target_slot_idx].card
            else:
                target_card = enemy_slots[target_slot_idx].card

            used_before = card.used_cast
            card.focus_cast_action(target_card)

            # If focus wasn't cleared the target was rejected — clean up
            if wzglobals.cast_focus:
                _cleanup_focus()
                return False

            return card.used_cast and not used_before

        else:
            # Regular (non-focus) cast — call cast_action directly
            card.cast_action()
            return True

    # --- skip ---
    elif act == 'skip':
        return True

    return False  # unknown action


# ---------------------------------------------------------------------------
# Main AI entry point
# ---------------------------------------------------------------------------

def take_turn():
    """LLM-powered AI turn. Falls back to heuristic on any failure."""
    if not os.environ.get('DEEPSEEK_API_KEY'):
        _heuristic_turn()
        return

    try:
        state = get_game_state()
        action = call_deepseek(state)
        print("LLM AI action:", action)
        if not execute_action(action):
            print("LLM action rejected, falling back to heuristic")
            _heuristic_turn()
    except Exception as e:
        print("LLM AI error:", e)
        _heuristic_turn()


def _heuristic_turn():
    """Original heuristic AI: summon the best available creature."""
    cb = select_cardbox()
    if cb:
        c = select_card(cb.card)
        if c:
            cb.card = c()
            cb.card.field = True
            wzglobals.player.mana[cb.card.element] -= cb.card.level
            cb.card.parent = cb
            if wzglobals.player.id == 1:
                wzglobals.ccards_1.add(cb.card)
            else:
                wzglobals.ccards_2.add(cb.card)
            cb.card.summon()


# ---------------------------------------------------------------------------
# Original heuristic helpers (unchanged)
# ---------------------------------------------------------------------------

def select_cardbox():
    s_cardboxes = []
    if wzglobals.player.id == 1:
        for cardbox in wzglobals.cardboxes[0:5]:
            if cardbox.card.name == "player":  # если есть карта
                s_cardboxes.append(cardbox)
    else:
        for cardbox in wzglobals.cardboxes[5:10]:
            if cardbox.card.name == "player":
                s_cardboxes.append(cardbox)
    e_cardboxes = []
    if wzglobals.player.id == 2:
        for cardbox in wzglobals.cardboxes[0:5]:
            if cardbox.card.name != "player":  # если есть карта
                e_cardboxes.append(cardbox)
    else:
        for cardbox in wzglobals.cardboxes[5:10]:
            if cardbox.card.name != "player":
                e_cardboxes.append(cardbox)
    e_strongest_power = 0
    if not len(e_cardboxes):
        if len(s_cardboxes):
            return s_cardboxes[0]
        else:
            return 0
    while True:
        for cardbox in e_cardboxes:
            if cardbox.card.power > e_strongest_power:
                e_strongest_cardbox = cardbox
                e_strongest_power = cardbox.card.power
        if e_strongest_power:
            if e_strongest_cardbox.get_opposite_cardbox() not in s_cardboxes:
                e_cardboxes.remove(e_strongest_cardbox)
                e_strongest_power = 0
            else:
                return e_strongest_cardbox.get_opposite_cardbox()
        else:
            if len(s_cardboxes):
                return s_cardboxes[0]
            else:
                return 0


def select_card(enemy_card):
    player = wzglobals.player
    self_cards = (
        list(player.cards['water'].values()) +
        list(player.cards['fire'].values()) +
        list(player.cards['air'].values()) +
        list(player.cards['earth'].values()) +
        list(player.cards['life'].values()) +
        list(player.cards['death'].values())
    )
    random.shuffle(self_cards)
    item = None
    max_eff = 0
    if enemy_card != "player":
        # If opponent has more of not void  cardboxes
        for card in self_cards:
            if card.type == 'warrior_card':
                eff = card.ai('summon', enemy_card)
                if eff >= max_eff:
                    max_eff = eff
                    item = card
    else:
        # if we dont needs on covering opponent card
        for card in self_cards:
            eff = card.ai('summon', enemy_card)
            if eff >= max_eff:
                max_eff = eff
                item = card
    if item is None:
        return None
    return item.__class__
