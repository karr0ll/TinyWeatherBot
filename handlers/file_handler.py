import json


class FileHandler:

    def save_chat_data_to_json(self, user_id, lat, lon, city_type, city_name):
        with open("chat_data.json", "w", encoding="UTF-8") as file:
            data = [
                {
                    "user_id": user_id,
                    "lat": lat,
                    "lon": lon,
                    "city_type": city_type,
                    "city_name": city_name
                }
            ]
            json.dump(data, file, indent=2, ensure_ascii=False)

    def load_data_from_json(self):
        with open("chat_data.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
            return data


    def update_chat_data_in_json(self, user_id, lat, lon, city_type, city_name):
        data = self.load_data_from_json()
        with open("chat_data.json", "w", encoding="UTF-8") as file:
            for item in data:
                if item["user_id"] == user_id and item["lat"] == lat and item["lon"] == lon:
                    pass
                else:
                    data.append(
                        {
                            "user_id": user_id,
                            "lat": lat,
                            "lon": lon,
                            "city_type": city_type,
                            "city_name": city_name
                        }
                    )
                json.dump(data, file, indent=2, ensure_ascii=False)
