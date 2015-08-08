class TitlePaginator:
    BULK_COUNT = 5

    def __init__(self, title_candidates):
        self.title_candidates = title_candidates
        self.current_index = 0

    def __len__(self):
        return len(self.title_candidates)

    def __getitem__(self, key):
        return self.title_candidates[key]

    def current_titles(self):
        start = self.current_index * TitlePaginator.BULK_COUNT
        end = start + TitlePaginator.BULK_COUNT
        return enumerate(self.title_candidates[start:end], (self.current_index * TitlePaginator.BULK_COUNT))

    def back(self):
        self.current_index = max(0, self.current_index - 1)

    def forwards(self):
        next_bulk = self.current_index + 1
        if len(self) >= next_bulk * TitlePaginator.BULK_COUNT:
            self.current_index = next_bulk
