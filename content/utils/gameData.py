
CONTENT_EVENT_TYPES = (
    ('MODIFY_MONEY', 'Add/Subtract Player Money'), # add or subtract from player currency by integerParam amount
    ('MODIFY_ITEM', 'Give/Take Item from Player'), # add or subtract an inventory item by id and integerParam amount
    ('GAME_OVER', 'Game Over screen'), # kills the player, proceeds to gameover
)

CONTENT_CONDITION_TYPES = (
    ('EVALUATE_MONEY', 'Compare Player Money'), #needs an operator and number
    ('EVALUATE_ITEM', 'Compare Item in Player Inventory'), #needs an item id, operator, and number
    ('SKILL_CHECK', 'Compare Player Attribute') #needs a player skill id, operator, and number
)

CONTENT_PARAMS_OPERATORS = (
    ('===', 'Equals'),
    ('>=', 'Greater than or equal to'),
    ('<=', 'Less than or equal to'),
    ('>', 'Greater than'),
    ('<', 'Less than'),
    ('!=', 'Not equal to')
)