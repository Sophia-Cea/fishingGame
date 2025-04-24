import json


class GameData:
    money = 100
    aquariumLocked = True
    unlockAquariumCost = 2000
    holdingCellInventory = []
    scaleFactor = 1
    savePath = None
    boatInventory = []

    frequencyOfBite = 100

    inventoryCapacity = 20
    aquariumRoomsUnlocked = []
    upgradesAcquired = []
    watersUnlocked = ["Crystal Glade Lake", "Silverfin Lake"]

    lines = [
        {
            "locked": False,
            "bait" : "corn",
            "hook" : 1
        },
        {
            "locked": False,
            "bait" : None,
            "hook" : None
        },
        {
            "locked": False,
            "bait" : None,
            "hook" : None
        },
        {
            "locked": False,
            "bait" : None,
            "hook" : None
        },
    ]
    
    itemsBought = {
        "bait" : [
            "bug",
            "worm",
            "goldfish"
        ],

        "hooks" : [
            1,
            1,
            2,
            20
        ]
    }

    upgradeData = {
        "unlockables" : {
            "Net" : {
                "name" : "Net",
                "unlocked" : False,
                "level" : 0,
                "max level" : 5,
                "cost" : 2000,
                "image" : "net_1.png"
            },
            "Idle Catch" : {
                "name" : "Idle Catch",
                "unlocked" : False,
                "level" : 0,
                "max level" : 5,
                "cost" : 2000,
                "image" : "logo.png"
            },
            "Line 1" : {
                "name" : "Line 1",
                "unlocked" : True,
                "level" : 1,
                "max level" : 5,
                "cost" : 2000,
                "image" : "line.png"
            },
            "Line 2" : {
                "name" : "Line 2",
                "unlocked" : False,
                "level" : 0,
                "max level" : 5,
                "cost" : 2000,
                "image" : "line.png"
            },
            "Line 3" : {
                "name" : "Line 3",
                "unlocked" : False,
                "level" : 0,
                "max level" : 5,
                "cost" : 2000,
                "image" : "line.png"
            },
            "Line 4" : {
                "name" : "Line 4",
                "unlocked" : False,
                "level" : 0,
                "max level" : 5,
                "cost" : 2000,
                "image" : "line.png"
            },
            "Radar" : {
                "name" : "Radar",
                "unlocked" : False,
                "level" : 0,
                "max level" : 5,
                "cost" : 2000,
                "image" : "radar1.png"
            }
        },
        "upgradables" : {
            "inventory capacity" : {
                "name" : "Inventory Capacity",
                "current value" : 20,
                "current level" : 0,
                "max" : 2000,
                "upgrade tree" : { # first cost then upgrade value
                    500: 25, 
                    1000: 35, 
                    1500: 70, 
                    3000: 100, 
                    5000: 200, 
                    10000: 500,
                    20000: 1000,
                    50000: 1500,
                    100000: 2000
                }
            },
            "holding pen capacity fresh" : {
                "name" : "Fresh Pen Capacity",
                "current value" : 5,
                "current level" : 0,
                "max" : 500,
                "upgrade tree" : { # first cost then upgrade value
                    500: 10, 
                    1000: 20, 
                    1500: 35, 
                    3000: 55, 
                    5000: 90, 
                    10000: 150,
                    20000: 250,
                    50000: 350,
                    100000: 500
                }
            },
            "holding pen capacity salt" : {
                "name" : "Salt Pen Capacity",
                "current value" : 5,
                "current level" : 0,
                "max" : 500,
                "upgrade tree" : { # first cost then upgrade value
                    500: 10, 
                    1000: 20, 
                    1500: 35, 
                    3000: 55, 
                    5000: 90, 
                    10000: 150,
                    20000: 250,
                    50000: 350,
                    100000: 500
                }
            },
            "holding pen capacity brackish" : {
                "name" : "Brackish Pen Capacity",
                "current value" : 5,
                "current level" : 0,
                "max" : 500,
                "upgrade tree" : { # first cost then upgrade value
                    500: 10, 
                    1000: 20, 
                    1500: 35, 
                    3000: 55, 
                    5000: 90, 
                    10000: 150,
                    20000: 250,
                    50000: 350,
                    100000: 500
                }
            },
            "luck" : {
                "name" : "Luckiness",
                "current value" : .01,
                "current level" : 0,
                "max" : .1,
                "upgrade tree" : { # first cost then upgrade value
                    1000: .015, 
                    2000: .02, 
                    5000: .025, 
                    8000: .03, 
                    12000: .04, 
                    20000: .05,
                    80000: .06,
                    100000: .08,
                    200000: .1
                }
            }
            
        },
        "items" : {
            "Worm" : {
                "num owned" : 1,
                "price" : 3,
                "image" : "worm"
            },
            "Bug" : {
                "num owned" : 0,
                "price" : 5,
                "image" : "bug"
            },
            "Corn" : {
                "num owned" : 0,
                "price" : 1,
                "image" : "corn"
            },
            "Goldfish" : {
                "num owned" : 0,
                "price" : 10,
                "image" : "goldfish"
            },
            "Chum Bucket" : {
                "num owned" : 0,
                "price" : 25,
                "image" : "chum_bucket"
            },
            "Size 1 Hook" : {
                "num owned" : 1,
                "price" : 5,
                "image" : "hook_1"
            },
            "Size 2 Hook" : {
                "num owned" : 0,
                "price" : 10,
                "image" : "hook_2"
            },
            "Size 3 Hook" : {
                "num owned" : 0,
                "price" : 15,
                "image" : "hook_3"
            },
            "Size 5 Hook" : {
                "num owned" : 0,
                "price" : 20,
                "image" : "hook_5"
            },
            "Size 7 Hook" : {
                "num owned" : 0,
                "price" : 30,
                "image" : "hook_7"
            },
            "Size 10 Hook" : {
                "num owned" : 0,
                "price" : 50,
                "image" : "hook_10"
            },
            "Size 15 Hook" : {
                "num owned" : 0,
                "price" : 100,
                "image" : "hook_15"
            },
            "Size 20 Hook" : {
                "num owned" : 0,
                "price" : 1000,
                "image" : "hook_20"
            },
        }
    }