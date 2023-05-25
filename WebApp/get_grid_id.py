from calc_distance import calculate_distance
import pandas as pd

def get_grid_id(location, df_grid_items: pd.DataFrame):
    lat = location["lat"]
    lng = location["lng"]
    distance_checker = {}

    df_grid_items["min_distance"] = df_grid_items.apply(
        lambda x: min(
            [
                calculate_distance(
                    lat, 
                    lng, 
                    r[1],
                    r[0]
                )
                for r in x["coordinates"]
            ]
        ),
        axis=1
    )
    return df_grid_items[df_grid_items["min_distance"] == df_grid_items["min_distance"].min()].to_dict('records')[0]
    
    # for row in grid_items_list:
    #     distance = min([calculate_distance(lat, lng, r[1], r[0]) for r in row["coordinates"]])
    #     # st.write(distance)
    #     distance_checker[distance] = row["id"]
    
    # return distance_checker[min(distance_checker)]