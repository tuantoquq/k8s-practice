class SONMTMiner(Miner):
    def __init__(self, input_tables, indicator_name, recursive_range):
        super().__init__(input_tables, indicator_name, recursive_range)

    def get_inputs(self, current_date: str, dict_input_dfs: Dict[str, pd.DataFrame], output_list: list):
        pass

    def formula(self, current_date: str, dict_input_dfs: Dict[str, pd.DataFrame], output_list: list):
        pass