ADAPTIVE_CARD_CONTENT = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.2",
    "body": [
        {
            "type": "Container",
            "items": [
                {
                    "type": "TextBlock",
                    "text": "Match",
                    "weight": "Bolder",
                    "size": "ExtraLarge",
                    "spacing": "Large",
                    "horizontalAlignment": "Center",
                    "wrap": True,
                    "maxLines": 0,
                    "color": "Dark",
                    "isSubtle": True,
                    "fontType": "Default"
                },
                {
                    "type": "ColumnSet",
                    "style": "default",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "Input.Text",
                                    "placeholder": "Home Team",
                                    "id": "home"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "Input.Text",
                                    "placeholder": "Away Team",
                                    "id": "away"
                                }
                            ]
                        }
                    ],
                    "separator": True,
                    "bleed": True
                }
            ],
            "height": "stretch",
            "bleed": True
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Predici"
                }
            ],
            "separator": True
        }
    ]
}
