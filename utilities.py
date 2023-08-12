import yaml
import os


# creating files and IO from cache


class Utilities:
    def __init__(self):
        self.session_cache = ".treditor_cache.yml"
        self.initialise_cache()

    def save_session(self, session_data, segment_data, session_name):
        data = {
            "segment_data": segment_data.to_dict(),
            "session_data": session_data.to_dict(),
        }
        with open(session_name, "w") as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    def get_session_name(self):
        with open(self.session_cache, "r") as f:
            cache_data = yaml.safe_load(f)
            session_name = cache_data.get("curr_session_name", "")
            if (
                session_name
                and isinstance(session_name, str)
                and session_name.endswith(".yml")
                and os.path.exists(session_name)
            ):
                return session_name
            else:
                return ""

    def set_session_name(self, session_name):
        with open(self.session_cache, "r") as f:
            cache_data = yaml.safe_load(f)
        cache_data["curr_session_name"] = session_name
        with open(self.session_cache, "w") as f:
            yaml.dump(cache_data, f)

    def initialise_cache(self):
        initial_data = {"curr_session_name": None}

        if os.path.exists(self.session_cache):
            with open(self.session_cache, "r") as f:
                existing_data = yaml.safe_load(f)
                if (
                    existing_data is None
                    or not all(key in existing_data for key in initial_data.keys())
                ):
                    remake_file = True
                else:
                    remake_file = False

            if remake_file:
                with open(self.session_cache, "w") as f:
                    yaml.dump(
                        initial_data, f, default_flow_style=False, sort_keys=False
                    )
        else:
            with open(self.session_cache, "w") as f:
                yaml.dump(initial_data, f, default_flow_style=False, sort_keys=False)


    def is_data_correct_format(self, data):
        keys = data.keys()
        if "session_data" not in keys:
            return False
        elif "segment_data" not in keys:
            return False
        return True
