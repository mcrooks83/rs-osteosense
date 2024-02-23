#name = StringField()
#description = StringField()
#instructions = StringField()
#repetitions = IntField()
#distance = IntField()

protocols =[

    {
        "name":"Repeated 10M Walk",
        "description": "A walk at self regulated pace for 30 seconds",
        "time_per_rep": 5,
        "repetitions": 2,
        "distance": 10,  # ignore as time based
        "instructions": "Write some instuctions for the subject to understand what is going on",
        

    },
    {
        "name":"20M Walk",
        "description": "a 20m self regualated walk",
        "time_per_rep": 0,
        "repetitions": 2,
        "distance": 20,  # ignore as time based
        "instructions": "Write some instuctions for the subject to understand what is going on",
        

    }

]