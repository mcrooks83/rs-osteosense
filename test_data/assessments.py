

#Assessment
#id autogen
from datetime import datetime, timedelta
from test_data import protocols as p

assessments=  [
    {
        "order" :0,
        "flow_id" : "ABC",
        "tag" : "4th Week Recovery",
        "tests" : [
            
            {
                "order": 0,
                "test_type" : "WEIGHT_BEARING",
                "protocol" : p.protocols[0],
                "results" : {},  # should be class TestResults
                "execution_date" : 0,
                "tag" : "walking test",
                "is_complete" : False
            }

        ],
        "execution_date" : int(datetime.now().timestamp()),
    },

]
